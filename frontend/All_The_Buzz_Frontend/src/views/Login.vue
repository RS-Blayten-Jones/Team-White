<template>
  <div class="login-page">
    <div class="login-card card">
      <h1 class="login-title">All The Buzz</h1>
      <h2 class="login-subtitle">Login</h2>
      <UserCreds @login="handleLogin" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import UserCreds from '@/components/UserCreds.vue'
import { exchangeTokenForCredentials, type Credentials } from '@/authClient'

const AUTH_URI = "http://172.16.0.51:8080/auth_service/api/auth/verify"

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
    const hardcodedJwt = '826s398719asd12jsdhf4'
    const token = hardcodedJwt

    // --- Step 2: Exchange token for Credentials using your auth server ---
    const authRes = await exchangeTokenForCredentials(AUTH_URI, token)
    // Handle the ResponseCode cases your Python could retur

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
    // For now we only need role + persist the JWT
    // Persist for 1 hour; adjust as needed.
    setCookie('jwt', token, 3600)
    setCookie('role', creds.role, 3600)
  } catch (error: any) {
    console.error('Login failed:', error)
    alert(`Login failed: ${error.message}`)
  }
  router.push({ name: 'resource-menu' })
}

  //if authentication is successful, set the cookie here 
  //const hardcodedJwt = '826s398719asd12jsdhf4'
  //const hardcodedRole = 'Manager' // or 'Employee
  //setCookie('jwt', hardcodedJwt, 3600) //sets cookie to expire in 1 hour (3600 seconds)
  //setCookie('role', hardcodedRole, 3600) //sets cookie to expire in 1 hour (3600 seconds)
  //setCookie('jwt', hardcodedJwt)
  //setCookie('role', hardcodedRole)


  // router.push({ name: 'resource-menu' })
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
