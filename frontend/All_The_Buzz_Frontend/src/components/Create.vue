<template>
  <div class="create-component">
    <h2>Create New {{ resourceType }}</h2>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea
          id="content"
          v-model="formData.content"
          rows="4"
          placeholder="Enter content..."
          required
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="author">Author:</label>
        <input
          id="author"
          v-model="formData.author"
          type="text"
          placeholder="Enter author name"
          required
        />
      </div>
      
      <div v-if="resourceType === 'trivia'" class="form-group">
        <label for="question">Question:</label>
        <input
          id="question"
          v-model="formData.question"
          type="text"
          placeholder="Enter question"
        />
      </div>
      
      <div v-if="resourceType === 'trivia'" class="form-group">
        <label for="answer">Answer:</label>
        <input
          id="answer"
          v-model="formData.answer"
          type="text"
          placeholder="Enter answer"
        />
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
        content: '',
        author: '',
        question: '',
        answer: ''
      },
      loading: false,
      error: '',
      success: '',
      jwt: 'eyJhbGciOiJIUzI1NiJ9.eyJsYXN0X25hbWUiOiJQYXRpZW5jZSIsImxvY2F0aW9uIjoiVW5pdGVkIFN0YXRlcyIsImlkIjo4NDksImRlcGFydG1lbnQiOiJJbmZvcm1hdGlvbiBUZWNobm9sb2d5IiwidGl0bGUiOiJNYW5hZ2VyIiwiZmlyc3RfbmFtZSI6IldhbGxpdyIsInN1YiI6IldhbGxpdyBQYXRpZW5jZSIsImlhdCI6MTc2NDc5NTkwMywiZXhwIjoxNzY0Nzk5NTAzfQ.IzQYNNtuSJmHr5fGbZ_2iKke11zZ6WjhALo9oYP72gs'
    }
  },
  
  methods: {
    resetForm() {
      this.formData.content = ''
      this.formData.author = ''
      this.formData.question = ''
      this.formData.answer = ''
      this.error = ''
      this.success = ''
    },
    
    handleSubmit(){
      const formData = {
        level: 2,
        content: {
          type: "one liner",
          text: "stupid joke inside create.vue at 3:07 pm"
        },
        language: "english"
      }

      axios.post(`http://localhost:8080/${this.resourceType}`, formData, { //changed to http but havent tested it as of 10:40am
        headers: {
          'Bearer': `${this.jwt}`,
          'Content-Type': 'application/json'
        }
      }).then(response => {
        if (response.status === 200) {
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
