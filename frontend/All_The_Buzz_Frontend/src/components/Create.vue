<template>
  <div class="create-component">
    <h2>Create New {{ resourceType }}</h2>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="type-dropdown" v-if="resourceType === 'jokes'">Select a joke type</label>
        <select id="type-dropdown" v-if="resourceType === 'jokes'" v-model="formData.content.type" required>
          <option value="one_liner">One Liner</option>
          <option value="qa">Question and Answer</option>
        </select>
        <label for="difficulty-dropdown" v-if="resourceType === 'jokes'" >Select Difficulty Level</label>
        <select id="difficulty-dropdown" v-if="resourceType === 'jokes'" v-model="formData.level" required>
          <option value="1">Level 1</option>
          <option value="2">Level 2</option>
          <option value="3">Level 3</option>
        </select>
        <textarea v-if="resourceType === 'jokes' && formData.level == '3'" 
          v-model="formData.explanation"
          rows="4"
          placeholder="Enter explanation for difficult joke..."
        ></textarea>

        <textarea
          id="content"
          v-if="formData.content.type == 'one_liner'"
          v-model="formData.content.text"
          rows="4"
          :placeholder="`Enter ${getSingularResourceName(resourceType)}...`"
          required
        ></textarea>

        <div v-if="formData.content.type == 'qa'">
          <input
            v-model="formData.question"
            type="text"
            placeholder="Enter question..."
            required
          />
          <input
            v-model="formData.answer"
            type="text"
            placeholder="Enter answer..."
            required
          />
        </div>
      </div>

      <div class="form-group" v-if="resourceType === 'quotes'">
        <label for="content">Quote:</label>
        <textarea
          id="content"
          v-model="formData.content.text"
          type="text"
          placeholder="Enter quote"
          rows="4"
          required
        ></textarea>
      </div>
      <div class="form-group" v-if="resourceType === 'quotes'">
        <label for="author">Author:</label>
        <input
          id="author"
          v-model="formData.author"
          type="text"
          placeholder="Enter author name"
          required
        />
      </div>
      
      <div v-if="resourceType === 'trivias'" class="form-group">
        <label for="question">Question:</label>
        <input
          id="question"
          v-model="formData.question"
          type="text"
          placeholder="Enter question"
        />
      </div>
      <div v-if="resourceType === 'trivias'" class="form-group">
        <label for="answer">Answer:</label>
        <input
          id="answer"
          v-model="formData.answer"
          type="text"
          placeholder="Enter answer"
        />
      </div>
      <div v-if="resourceType === 'bios'" class="form-group" >
        <label for="birthyear">Birth Year:</label>
        <input
        id="birthyear"
        v-model="formData.birthYear"
        type="number" placeholder="YYYY" min="1000" max="2026" required
        />
      </div>
      <div v-if="resourceType === 'bios'" class="form-group" >
        <label for="deathyear">Death Year:</label>
        <input
        id="deathyear"
        v-model="formData.deathYear"
        type="number" placeholder="YYYY" min="1000" max="2026"
        />
      </div>
      <div v-if="resourceType === 'bios'" class="form-group" >
        <label for="bioName">Subject Name:</label>
        <input
        id="bioName"
        v-model="formData.name"
        type="text"
        required
        />
      </div>
      <div class="form-group" v-if="resourceType === 'quotes'">
        <label for="content">Quote:</label>
        <textarea
          id="content"
          v-model="formData.content.text"
          type="text"
          placeholder="Enter quote"
          rows="4"
          required
        ></textarea>
      </div>
      <div v-if="resourceType === 'bios'" class="form-group" >
        <label for="website_url">Enter your website URL:</label>
        <input type="url" id="website_url" name="website_url" placeholder="https://example.com" required>
      </div>
      <div class="form-group">
        <input
          v-model="formData.language"
          type="text"
          placeholder="Enter language"
          required
        >
        </input>
      </div>
      
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
      
      <div class="button-group">
        <button type="submit" class="submit-button" :disabled="loading">
          {{ loading ? 'Creating...' : 'Create' }}
        </button>
        <button type="button" class="reset-button" @click="resetForm">
          Reset
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'
import { getCookie } from '@/utils/cookies'

export default defineComponent({
  name: 'CreateComponent',
  
  props: {
    resourceType: {
      type: String,
      required: true
    }
  },
  
  data() {
    return {
      formData: {
        content: {
          type: "",
          text: ""
        },
        author: '',
        question: '',
        answer: '',
        level: '',
        explanation: '',
        language: '',
        birthYear: '',
        deathYear:'',
        name: '',
        paragraph: '',
        summary: '',
        sourceURL: ''
      },
      loading: false,
      error: '',
      success: '',
      jwt: ''
    }
  },
  
  methods: {
    resetForm() {
      this.formData.content = {
        type: "",
        text: ""
      }
      this.formData.author = ''
      this.formData.question = ''
      this.formData.answer = ''
      this.error = ''
      this.success = ''
    },
    getSingularResourceName(resourceType: string): string {
      if (resourceType.endsWith('ies')) {
        return resourceType.slice(0, -3) + 'y';
      } else if (resourceType.endsWith('s')) {
        return resourceType.slice(0, -1);
      }
      return resourceType;
    },
    handleSubmit(){
      let formattedData = this.formatDataByResourceType(this.resourceType);
      console.log('Formatted Data:', formattedData);
      
      const role = getCookie('role')
      const token = getCookie('jwt')
      console.log('cookies before request:', { role, token })

      // return;
      axios.post(`http://localhost:8080/${this.resourceType}`, formattedData, {
        headers: {
          'Bearer': `${token}`,
          'Content-Type': 'application/json'
        }
      }).then(response => {
        if (response.status === 201) {
          this.success = `${this.resourceType} created successfully!`;
          this.resetForm();
        } else {
          this.error = `Failed to create ${this.resourceType}. Status: ${response.status}: ${response.statusText}`;
        }
        console.log('Response:', response.data);
      }).catch(error => {
        console.error('Error:', error);
        this.error = error.status + ' ' + error.message || 'Failed to create item';
      });
    },
    formatDataByResourceType(resourceType: string) {
      if (resourceType === 'jokes' && this.formData.content.type === 'one_liner') {
        return {
          level: parseInt(this.formData.level),
          content: {
            type: this.formData.content.type,
            text: this.formData.content.text
          },
          language: this.formData.language
        }
      }
      else if (resourceType === 'jokes' && this.formData.content.type === 'qa') {
        return {
          level: parseInt(this.formData.level),
          content: {
            type: this.formData.content.type,
            question: this.formData.question,
            answer: this.formData.answer
          },
          language: this.formData.language,
          explanation: this.formData.level == '3' ? this.formData.explanation : ""
        }
      }
      else if (resourceType === 'quotes') {
        return {
          content: this.formData.content.text,
          author: this.formData.author,
          language: this.formData.language
        }
      }
      else if (resourceType === 'trivias'){
        return {
          question: this.formData.question,
          answer: this.formData.answer,
          language: this.formData.language
        }
      }
      else if (resourceType === 'bios'){
        return {
          birth_year: this.formData.birthYear,
          death_year: this.formData.deathYear,
          name: this.formData.name
        }
      }
    }
  }
})
</script>

<style scoped>
.create-component {
  padding: 1rem;
}

h2 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  text-transform: capitalize;
  font-size: var(--font-size-2xl);
}

form {
  max-width: 600px;
}

.form-group {
  /* color: red; */
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

.success {
  background-color: var(--color-success-light);
  color: var(--color-success);
  border: 1px solid var(--color-success);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  margin-bottom: var(--spacing-md);
  font-weight: var(--font-weight-medium);
}

.button-group {
  display: flex;
  gap: 1rem;
}

.submit-button {
  background-color: var(--color-success);
  color: var(--text-on-primary);
  padding: 0.75rem 2rem;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-base);
}

.submit-button:hover:not(:disabled) {
  background-color: #047857;
  transform: translateY(-1px);
}

.submit-button:focus {
  outline: 3px solid var(--color-primary-orange);
  outline-offset: 2px;
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.reset-button {
  background-color: var(--color-gray-600);
  color: var(--text-on-primary);
  padding: 0.75rem 2rem;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-base);
}

.reset-button:hover {
  background-color: var(--color-primary-orange);
}

.reset-button:focus {
  outline: 3px solid var(--color-primary-orange);
  outline-offset: 2px;
}
</style>
