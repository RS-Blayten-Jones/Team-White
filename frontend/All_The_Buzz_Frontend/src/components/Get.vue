
<template>
  <div class="get-component">
    <h2>{{ resourceType }} Actions</h2>

    <!-- Error Message -->
    <div v-if="msg" class="error">{{ msg }}</div>

    <div class="filters">
      <button class="fetch-button" @click="getAllPub">
        Get All {{ resourceType }}
      </button>

      <div>
        <input type="number" v-model.number="randAmt" min="1" placeholder="Amount" />
        <button class="fetch-button" @click="GetRand(randAmt)">
          Get Random {{ resourceType }}
        </button>
      </div>

      <button
        v-if="isManager"
        class="fetch-button"
        @click="getAllPend"
      >
        Get All Pending {{ resourceType }}
      </button>

      <div>
        <select v-model.number="difficulty">
          <option disabled value="">Select Difficulty</option>
          <option :value="1">difficulty 1</option>
          <option :value="2">difficulty 2</option>
          <option :value="3">difficulty 3</option>
        </select>
        <button class="fetch-button" @click="GetByDiff(difficulty)">
          Get by Difficulty
        </button>
      </div>

      <div v-if="resourceType === 'quotes'">
        <!-- Daily Quote -->
        <button class="fetch-button" @click="GetDailyQuote">
          Get Daily Quote
        </button>

        <!-- Short Quotes with amt -->
        <div>
          <input type="number" v-model.number="shortAmt" min="1" placeholder="Amount" />
          <button class="fetch-button" @click="GetShortQuote(shortAmt)">
            Get Short Quotes
          </button>
        </div>
      </div>
    </div>

    <!-- Results -->
    <div class="results" v-if="rows.length">
      <h3>Results:</h3>

      
      <DataTable
        :data="rows"
        :columns="preferredColumns"
        :headerMap="headers"
        :hiddenColumns="hidden"
        :getRowKey="getRowKey"
      >
        <template #cell="{ row, column, value }">
          <template v-if="resourceType === 'jokes' && column === 'content'">
            <!-- Defensive guards in case content is missing -->
            <template v-if="row && row.content && row.content.type">
              <!-- ONE-LINER -->
              <div v-if="row.content.type === 'one_liner'" class="one-liner-content">
                {{ row.content.text }}
              </div>

              <!-- Q & A -->
              <div
                v-else-if="row.content.type === 'qa'"
                class="qa-content"
                tabindex="0"
                aria-live="polite"
              >
                <div class="question">
                  <strong>Q:</strong> {{ row.content.question }}
                  <small v-if="row.language" class="muted"> ({{ row.language }})</small>
                  <small class="hint">Hover or focus to reveal answer</small>
                </div>

                <div class="answer" aria-hidden="true">
                  <strong>A:</strong> {{ row.content.answer }}
                </div>
              </div>

              <!-- Fallback for unknown type -->
              <div v-else>
                {{ value }}
              </div>
            </template>

            <!-- If content is missing -->
            <template v-else>
              {{ value }}
            </template>
          </template>

          <!-- Actions column with delete button -->
          <template v-else-if="column === 'actions'">
            <DeleteButton
              :id="getItemId(row)"
              :category="resourceType"
              :jwt="jwt"
              :isManager="isManager"
              @deleted="handleDeleted"
              @error="handleDeleteError"
            />
          </template>

          <!-- Default rendering for other columns -->
          <template v-else>
            {{ value }}
          </template>
        </template>
      </DataTable>

    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'
import DataTable from '@/components/DataTable.vue' // keep if alias is configured; else use './DataTable.vue'
import DeleteButton from '@/components/Delete.vue'

export default defineComponent({
  name: 'GetButton',
  components: { DataTable, DeleteButton },
  props: {
    isManager: { type: Boolean, required: true },
    jwt: { type: String, required: true },
    resourceType: { type: String, required: true }
  },
  data() {
    return {
      msg: "",
      apiData: {},
      shortAmt: 1,
      amt: 1,
      randAmt: 1,
      difficulty: '' as number | ''
    }
  },
  computed: {
    // Normalize apiData into an array for the table
    rows(): any[] {
      const d = this.apiData
      let arr: any[] = []
      if (Array.isArray(d)) arr = d
      else if (d && Array.isArray((d as any).items)) arr = (d as any).items
      else if (d && Array.isArray((d as any).data)) arr = (d as any).data
      else if (d && typeof d === 'object' && Object.keys(d).length) arr = [d]
      else return []

      // Minimal normalization for jokes to avoid duplicate difficulty + keep native fields for slot
      if (this.resourceType === 'jokes') {
        return arr.map((row: any) => {
          const copy: any = { ...row }
          // prefer 'difficulty'; derive from 'level' if needed
          if (copy.level != null && copy.difficulty == null) copy.difficulty = copy.level
          // language normalization
          if (!copy.language && copy.lang) copy.language = copy.lang
          // do NOT delete question/answer/text — we need them in the slot
          // BUT prevent extra visible 'level' column
          delete copy.level
          return copy
        })
      }

      return arr
    },

    preferredColumns(): string[] {
      switch (this.resourceType) {
        case 'jokes':
          // Use 'level' (your payload), not 'difficulty'.
          // Keep 'content' and 'explanation' as you requested.
          return ['difficulty', 'language', 'content', 'explanation', 'actions']
        case 'quotes':
          return ['text', 'author', 'length', 'createdAt', 'actions']
        default:
          return ['actions']
      }
    },

    headers(): Record<string, string> {
      return {
        // For jokes: remap 'level' to a friendly header
        language: 'Language',
        content: 'Content',
        explanation: 'Explanation',

        // Quotes
        text: this.resourceType === 'quotes' ? 'Quote' : 'Text',
        status: 'Status',
        author: 'Author',
        length: 'Length',
        createdAt: 'Created',
        
        // Actions column
        actions: 'Actions'
      }
    },

    hidden(): string[] {
      // Hide _id (nested id), keep content visible (we render it via slot).
      const base = ['_id']
      return base
    }
  },

  

  methods: {
    getAllPub() {
      axios.get(`http://localhost:8080/${this.resourceType}`, {
        headers: {
          'Bearer': `${this.jwt}`
        }
      })
      .then(response => {
        this.apiData = response.data
        this.msg = ''
      })
      .catch(error => {
        this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown')
      })
    },

    
    getRowKey(row: any, index: number) {
      // Prefer Mongo-style OID if present
      const oid = row?._id?.$oid
      if (oid) return oid
      return row.id ?? `${this.resourceType}-${index}`
    },

    getItemId(row: any): string {
      // Extract the ID from the row - handle both _id.$oid and direct id
      if (row?._id?.$oid) {
        return row._id.$oid
      }
      if (row?.id) {
        return String(row.id)
      }
      if (row?._id) {
        return String(row._id)
      }
      return ''
    },

    handleDeleted(payload: { id: string }) {
      // Remove the deleted item from the current data
      if (Array.isArray(this.apiData)) {
        this.apiData = this.apiData.filter((item: any) => {
          const itemId = this.getItemId(item)
          return itemId !== payload.id
        })
      } else if (this.apiData && Array.isArray((this.apiData as any).items)) {
        (this.apiData as any).items = (this.apiData as any).items.filter((item: any) => {
          const itemId = this.getItemId(item)
          return itemId !== payload.id
        })
      } else if (this.apiData && Array.isArray((this.apiData as any).data)) {
        (this.apiData as any).data = (this.apiData as any).data.filter((item: any) => {
          const itemId = this.getItemId(item)
          return itemId !== payload.id
        })
      }
      // Optionally show success message
      this.msg = ''
    },

    handleDeleteError(message: string) {
      this.msg = message
    },


    getAllPend() {
      axios.get(`http://localhost:8080/pending-${this.resourceType}`, {
        headers: {
          'Bearer': `${this.jwt}`
        }
      })
      .then(response => {
        this.apiData = response.data
        this.msg = ''
      })
      .catch(error => {
        this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown')
      })
    },

    GetRand(amt: string | number) {
      const n = Number(amt)
      axios.get(`http://localhost:8080/random-${this.resourceType}/${n}`, {
        headers: {
          'Bearer': `${this.jwt}`
        }
      })
      .then(response => {
        this.apiData = response.data
        this.msg = ''
      })
      .catch(error => {
        this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown')
      })
    },

    GetByDiff(difficulty: string | number) {
      if (this.resourceType !== 'jokes') {
        this.msg = 'GetByDiff is only available for resourceType "jokes".'
        return
      }
      const n = Number(difficulty)
      axios.get(`http://localhost:8080/${this.resourceType}`, {
        params: { difficulty: n },
        headers: {
          'Bearer': `${this.jwt}`
        }
      })
      .then(response => {
        this.apiData = response.data
        this.msg = ''
      })
      .catch(error => {
        this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown')
      })
    },

    GetDailyQuote() {
      if (this.resourceType !== 'quotes') {
        this.msg = 'Daily Quote is only available for resourceType "quotes".'
        return
      }
      axios.get(`http://localhost:8080/daily-quotes`, {
        headers: {
          'Bearer': `${this.jwt}`
        }
      })
      .then(response => {
        this.apiData = response.data
        this.msg = ''
      })
      .catch(error => {
        this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown')
      })
    },

    GetShortQuote(amt: string | number) {
      if (this.resourceType !== 'quotes') {
        this.msg = 'Short Quote is only available for resourceType "quotes".'
        return
      }
      const n = Number(amt)
      axios.get(`http://localhost:8080/short-quotes/${n}`, {
        headers: {
          'Bearer': `${this.jwt}`
        }
      })
      .then(response => {
        this.apiData = response.data
        this.msg = ''
      })
      .catch(error => {
        this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown')
      })
    }
  }
})
</script>


<style scoped>
.get-component {
  padding: var(--spacing-md);
}

h2 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  text-transform: capitalize;
  font-size: var(--font-size-2xl);
}

.filters {
  display: flex;
  gap: var(--spacing-md);
  align-items: flex-end;
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
}

.filters select,
.filters input {
  padding: 0.5rem 0.75rem;
}

.fetch-button {
  background-color: var(--color-success);
  color: var(--text-on-primary);
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-base);
  white-space: nowrap;
}

.fetch-button:hover {
  background-color: #047857;
  transform: translateY(-1px);
}

.fetch-button:focus {
  outline: 3px solid var(--color-primary-orange);
  outline-offset: 2px;
}

.error {
  background-color: var(--color-error-light);
  color: var(--color-error);
  border: 1px solid var(--color-error);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  margin-bottom: var(--spacing-md);
  font-weight: var(--font-weight-medium);
}

.results h3 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-xl);
}

.items-grid {
  display: grid;
  gap: var(--spacing-md);
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.item-card {
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  transition: box-shadow var(--transition-base), background-color var(--transition-base);
}

.item-card:hover {
  box-shadow: var(--shadow-md);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid var(--border-color);
}

.item-id {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  font-weight: var(--font-weight-semibold);
}

.item-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
}

.item-status.approved {
  background-color: var(--color-success-light);
  color: var(--color-success);
}

.item-status.pending {
  background-color: var(--color-warning-light);
  color: var(--color-warning);
}

.item-content p {
  margin: var(--spacing-sm) 0;
  color: var(--text-primary);
  line-height: 1.6;
}

/* optional polish */
.muted {
  color: var(--text-secondary);
  margin-left: 0.25rem;
  font-size: 0.85em;
}
.question {
  margin-bottom: 0.25rem;
}

.qa-content .answer {
  opacity: 0;
  filter: blur(4px);
  transition: opacity 180ms ease, filter 180ms ease;
  user-select: none;
}
.qa-content:hover .answer,
.qa-content:focus-within .answer {
  opacity: 1;
  filter: blur(0);
  user-select: text;
}

.muted {
  color: var(--text-secondary);
  margin-left: 0.25rem;
  font-size: 0.85em;
}
.hint {
  margin-left: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.8em;
}

</style>