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
        <input type="number" v-model="randAmt" min="1" placeholder="Amount" />
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
        <select v-model="difficulty">
          <option disabled value="">Select Difficulty</option>
          <option value="1">Level 1</option>
          <option value="2">Level 2</option>
          <option value="3">Level 3</option>
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
          <input type="number" v-model="shortAmt" min="1" placeholder="Amount" />
          <button class="fetch-button" @click="GetShortQuote(shortAmt)">
            Get Short Quotes
          </button>
        </div>
      </div>
    </div>

    <!-- Results -->
    <div class="results" v-if="apiData && Object.keys(apiData).length">
      <h3>Results:</h3>
      <pre>{{ apiData }}</pre>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'GetButton',
		props: {
			isManager: {
        type: Boolean,
        required: true
      },
			jwt: {
				type: String,
				required: true
			},
			resourceType: {
				type: String,
				required: true
			}
		},
	data() {
		return {
			msg: "",
			apiData: {},
      shortAmt: 0,
      amt: 0,
      randAmt: 0,
      difficulty: ''
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
      this.apiData = response.data;
      this.msg = '';
    })
    .catch(error => {
      this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
    });
  },

  getAllPend() {
    axios.get(`http://localhost:8080/pending-${this.resourceType}`, {
      headers: {
        'Bearer': `${this.jwt}`
      }
    })
    .then(response => {
      this.apiData = response.data;
      this.msg = '';
    })
    .catch(error => {
      this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
    });
  },

  GetRand(amt: string | number) {
    axios.get(`http://localhost:8080/random-${this.resourceType}/${amt}`, {
      headers: {
        'Bearer': `${this.jwt}`
      }
    })
    .then(response => {
      this.apiData = response.data;
      this.msg = '';
    })
    .catch(error => {
      this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
    });
  },

  GetByDiff(level: string | number) {
    if (this.resourceType !== 'jokes') {
      this.msg = 'GetByDiff is only available for resourceType "jokes".';
      return;
    }
    axios.get(`http://localhost:8080/${this.resourceType}`, {
      params: { level: level },
      headers: {
        'Bearer': `${this.jwt}`
      }
    })
    .then(response => {
      this.apiData = response.data;
      this.msg = '';
    })
    .catch(error => {
      this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
    });
  },

  GetDailyQuote() {
    if (this.resourceType !== 'quotes') {
      this.msg = 'Daily Quote is only available for resourceType "quotes".';
      return;
    }
    axios.get(`http://localhost:8080/daily-quotes`, {
      headers: {
        'Bearer': `${this.jwt}`
      }
    })
    .then(response => {
      this.apiData = response.data;
      this.msg = '';
    })
    .catch(error => {
      this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
    });
  },

  GetShortQuote(amt: string | number) {
    if (this.resourceType !== 'quotes') {
      this.msg = 'Short Quote is only available for resourceType "quotes".';
      return;
    }
    axios.get(`http://localhost:8080/short-quotes/${amt}`, {
      headers: {
        'Bearer': `${this.jwt}`
      }
    })
    .then(response => {
      this.apiData = response.data;
      this.msg = '';
    })
    .catch(error => {
      this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
    });
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
</style>