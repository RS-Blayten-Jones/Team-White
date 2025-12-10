<template>
  <div class="about-us-page">
    <AppHeader />
    
    <div class="about-content">
      <h1>About Us</h1>
      
      <div v-if="loading" class="loading">
        Loading company information...
      </div>
      
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      
      <div v-else class="info-sections">
        <!-- Mission Statement Section -->
        <section class="info-card mission">
          <h2>Our Mission</h2>
          <p>{{ aboutData.missionStatement || 'Loading mission statement...' }}</p>
        </section>
        
        <!-- Development Team Section -->
        <section class="info-card team">
          <h2>Development Team</h2>
          <div v-if="aboutData.developmentTeam && aboutData.developmentTeam.length > 0">
            <ul class="team-list">
              <li v-for="(member, index) in aboutData.developmentTeam" :key="index">
                {{ member }}
              </li>
            </ul>
          </div>
          <p v-else>Loading team information...</p>
        </section>
        
        <!-- Copyright Section -->
        <section class="info-card copyright">
          <h2>Copyright</h2>
          <p>{{ aboutData.copyright || 'Loading copyright information...' }}</p>
        </section>
      </div>
      
      <button class="back-button" @click="goBack">
        Back to Menu
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import { getCookie } from '@/utils/cookies'

interface AboutData {
  missionStatement: string
  developmentTeam: string[]
  copyright: string
}

export default defineComponent({
  name: 'AboutUs',
  
  components: {
    AppHeader
  },
  
  data() {
    return {
      aboutData: {
        missionStatement: '',
        developmentTeam: [] as string[],
        copyright: ''
      } as AboutData,
      loading: true,
      error: '',
      jwt: ''
    }
  },
  
  mounted() {
    this.jwt = getCookie('jwt') || ''
    this.fetchAboutData()
  },
  
  methods: {
    async fetchAboutData() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await axios.get('http://localhost:8080/about')

        this.aboutData = response.data
        
      } catch (err: any) {
        this.error = err.message || 'Failed to load company information'
      } finally {
        this.loading = false
      }
    },
    
    goBack() {
      this.$router.push({ name: 'resource-menu' })
    }
  }
})
</script>

<style scoped>
.about-us-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary-yellow) 0%, var(--color-primary-orange) 100%);
}

.about-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: var(--text-primary);
  text-align: center;
  font-size: var(--font-size-3xl);
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  font-size: var(--font-size-lg);
}

.error {
  background-color: var(--color-error-light);
  color: var(--color-error);
  border: 1px solid var(--color-error);
  border-radius: var(--border-radius-md);
  max-width: 600px;
  margin: 2rem auto;
}

.info-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 2rem;
}

.info-card {
  background: white;
  padding: 2rem;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.info-card h2 {
  color: var(--color-primary-orange);
  font-size: var(--font-size-2xl);
  margin-bottom: 1rem;
  border-bottom: 3px solid var(--color-primary-yellow);
  padding-bottom: 0.5rem;
}

.info-card p {
  color: var(--text-primary);
  font-size: var(--font-size-base);
  line-height: 1.6;
}

.team-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.team-list li {
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  background: var(--color-gray-100);
  border-radius: var(--border-radius-md);
  color: var(--text-primary);
  font-weight: var(--font-weight-medium);
  transition: background var(--transition-base);
}

.team-list li:hover {
  background: var(--color-primary-yellow);
}

.mission p {
  font-size: var(--font-size-lg);
  font-style: italic;
  text-align: center;
}

.copyright p {
  text-align: center;
  color: var(--text-secondary);
  font-weight: var(--font-weight-semibold);
}

.back-button {
  display: block;
  margin: 2rem auto;
  padding: 0.75rem 2rem;
  background-color: var(--color-primary-orange);
  color: white;
  border: none;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
}

.back-button:hover {
  background-color: #d97706;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.back-button:focus {
  outline: 3px solid var(--color-primary-yellow);
  outline-offset: 2px;
}

@media (max-width: 768px) {
  .about-content {
    padding: 1rem;
  }
  
  h1 {
    font-size: var(--font-size-2xl);
  }
  
  .info-card {
    padding: 1.5rem;
  }
}
</style>
