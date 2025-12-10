<template>
  <div class="login-page">
    <div class="login-card card">
      <h1 class="login-title">All The Buzz</h1>
      <h2 class="login-subtitle">Login</h2>
      <UserCreds @login="handleLogin" />
      
      <!-- DEV BYPASS BUTTON - Comment out for production -->
      <button class="dev-bypass-btn" @click="devBypass">
        🐝 DEV BYPASS (No Auth)
      </button>
      <!-- END DEV BYPASS -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import UserCreds from '@/components/UserCreds.vue'
import { exchangeTokenForCredentials, type Credentials } from '@/authClient'
import axios from 'axios'

const AUTH_URI = "http://172.16.0.51:8080/auth_service/api/auth/verify"
const LOGIN_URI ="http://172.16.0.51:42068/login"
const router = useRouter()

function setCookie(name: string, value: string, maxAgeSeconds?: number){
  const parts = [`${name}=${encodeURIComponent(value)}`, 'path=/']
  if (maxAgeSeconds) {
    parts.push(`max-age=${maxAgeSeconds}`) //max age is how long it takes the cookie to expire
  }
  document.cookie = parts.join('; ')
}


async function handleLogin(credentials: { username: string; password: string }) {
  // TODO: Implement actual authentication logic
  console.log('Login attempt:', credentials)
  
  try {
    // --- Step 1: (Simulated) obtain token from login server ---
    // Normally you would call loginUri with credentials and get back a token:
    // const loginRes = await axios.post(LOGIN_URI, credentials)
    // const token = loginRes.data.token

    // For now, use hardcoded token as requested:
    const hardcodedJwt = 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBdXRoIFNlcnZpY2UiLCJsYXN0X25hbWUiOiJTdGVubmluZ3MiLCJsb2NhdGlvbiI6IlVuaXRlZCBTdGF0ZXMiLCJpZCI6OCwiZGVwYXJ0bWVudCI6IkluZm9ybWF0aW9uIFRlY2hub2xvZ3kiLCJ0aXRsZSI6IkRldmVsb3BlciIsImZpcnN0X25hbWUiOiJCYXNpbCIsInN1YiI6IkJhc2lsIFN0ZW5uaW5ncyIsImlhdCI6MTc2NTM4Njg2OCwiZXhwIjoxNzY1MzkwNDY4fQ.Wtwsii3GhSj4w4PD-WHZ9hxAq8ih8DUqT9rka2tzYNI' //PUT TOKEN HERE!
    const token = hardcodedJwt

    // --- Step 2: Exchange token for Credentials using your auth server ---
    const authRes = await exchangeTokenForCredentials(token)
    // Handle the ResponseCode cases your Python could return

    if ('code' in authRes) {
        // These match your Python ResponseCode returns
      switch (authRes.code) {
        case 'InvalidToken':
          throw new Error('Invalid token format')
        case 'ConfigLoadError':
          throw new Error('Failed to load auth config')
        case 'ServerConnectionError':
          throw new Error('Authentication server unreachable')
        case 'AuthServerError':
          throw new Error('Authentication server error')
        case 'UnauthorizedToken':
          throw new Error('Unauthorized token')
        default:
          throw new Error('Unknown authentication error')
      }
    }
    // --- Step 3: We have valid Credentials ---
    const creds = authRes as Credentials
    console.log(authRes)
    // For now we only need role + persist the JWT
    // Persist for 1 hour; adjust as needed.
    setCookie('jwt', token, 3600)
    setCookie('role', authRes.title , 3600)
    setCookie('f_name', authRes.fName, 3600)
    setCookie('l_name', authRes.lName, 3600)
  } catch (error: any) {
    console.error('Login failed:', error)
    alert(`Login failed: ${error.message}`)
  }
  router.push({ name: 'resource-menu' })
}

// DEV BYPASS FUNCTION - Comment out for production
function devBypass() {
  console.log('🐝 DEV BYPASS: Skipping authentication')
  // Set dummy cookies for development
  setCookie('jwt', 'dev-bypass-token', 3600)
  setCookie('role', 'Manager', 3600)
  router.push({ name: 'resource-menu' })
}
// END DEV BYPASS

</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: url('login.png') center center/cover no-repeat, var(--color-primary-purple);
  padding: var(--spacing-md);
}

.login-card {
  min-width: 400px;
  max-width: 450px;
  width: 100%;
  text-align: center;
  background: rgba(255, 255, 255);
}

.login-title {
  color: var(--color-primary-purple);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-4xl);
}

.login-subtitle {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
}

/* DEV BYPASS BUTTON - Comment out for production */
.dev-bypass-btn {
  width: 100%;
  margin-top: var(--spacing-lg);
  padding: 0.75rem;
  background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
  color: #000;
  border: 2px dashed #ff6f00;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dev-bypass-btn:hover {
  background: linear-gradient(135deg, #ffca28 0%, #ffa726 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.4);
}

.dev-bypass-btn:active {
  transform: translateY(0);
}
/* END DEV BYPASS BUTTON */

@media (max-width: 768px) {
  .login-card {
    min-width: unset;
  }
  
  .login-title {
    font-size: var(--font-size-3xl);
  }
  
  .login-subtitle {
    font-size: var(--font-size-xl);
  }
}
</style>
