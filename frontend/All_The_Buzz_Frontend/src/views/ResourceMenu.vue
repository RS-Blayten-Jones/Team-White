<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import UserInfo from '@/components/UserInfo.vue'
import DailyQuote from '@/components/DailyQuote.vue'
import GetRandomJoke from '@/components/GetRandomJoke.vue'
import { getCookie } from '@/utils/cookies'

const router = useRouter()

// Cute bee mouse following
const cuteBeeX = ref(Math.random() * window.innerWidth)
const cuteBeeY = ref(Math.random() * window.innerHeight)
let cuteBeeAnimationId: number | null = null
const mouseX = ref(0)
const mouseY = ref(0)

// Get JWT and role from cookies
const jwt = ref<string>('')
const role = ref<string>('')

onMounted(() => {
  // Get cookies on mount
  jwt.value = getCookie('jwt') || ''
  role.value = getCookie('role') || ''
  
  // If no JWT, redirect to login
  if (!jwt.value) {
    router.push({ name: 'login' })
    return
  }
  
  window.addEventListener('mousemove', handleMouseMove)
  animateCuteBee()
})

const navigateTo = (resource: string) => {
  // Just navigate to the resource - the view will get cookies itself
  router.push({ name: resource })
}


// Mouse tracking
const handleMouseMove = (e: MouseEvent) => {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
}

// Cute bee follows mouse with smooth delay
const animateCuteBee = () => {
  // Smooth follow with easing
  const dx = mouseX.value - cuteBeeX.value
  const dy = mouseY.value - cuteBeeY.value
  
  // Adjust speed (0.05 = slower follow, 0.2 = faster follow)
  cuteBeeX.value += dx * 0.08
  cuteBeeY.value += dy * 0.08
  
  cuteBeeAnimationId = requestAnimationFrame(animateCuteBee)
}
const welcomeText=ref("")
const fName=getCookie("f_name")
const lName=getCookie("l_name")
const sideBarName=ref("")
const sideBarRole=ref("")
const position=getCookie("role")

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
  animateCuteBee()
  welcomeText.value = `Welcome to the hive, ${fName} ${lName}!`
  sideBarName.value = `${fName} ${lName}`
  sideBarRole.value= `${position}`

})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  if (cuteBeeAnimationId !== null) {
    cancelAnimationFrame(cuteBeeAnimationId)
  }
})

</script>
<template> 
  <AppHeader title="Buzzword Software - Media Feed" />
  <div class ="resource-menu-page">
  <div id="main-content">
    <div id="primary-content">
      <div class="image-container">
      <div class ="overlay-text"> 
      <div class = "welcome-blurb">
      <p id="name">{{ welcomeText }}</p>
      </div>
      <p> This is your landing page for All The Buzz! Here you can access, add,
      and edit jokes, bios, quotes, and trivia. </p>
      </div>
      </div>
        <div id="resource-menu">
          <div class="resource-card" id="joke"
          @click="navigateTo('jokes')"
              tabindex="0"
              role="button"
              @keydown.enter="navigateTo('jokes')"
              @keydown.space.prevent="navigateTo('jokes')">
          <img src="/joke-icon.png" alt="joke icon"></img>
          Jokes
          </div>
          <div class="resource-card" id="trivia"
          @click="navigateTo('trivia')"
              tabindex="0"
              role="button"
              @keydown.enter="navigateTo('trivia')"
              @keydown.space.prevent="navigateTo('trivia')">
          <img src="/trivia-icon.png" alt="trivia icon"></img>
          Trivia
          </div>
          <div class="resource-card" id="quotes"
          @click="navigateTo('quotes')"
              tabindex="0"
              role="button"
              @keydown.enter="navigateTo('quotes')"
              @keydown.space.prevent="navigateTo('quotes')">
          <img src="/quote-icon.png" alt="quote icon"></img>
          Quotes
          </div>
          <div class="resource-card" id="bios"
          @click="navigateTo('bios')"
              tabindex="0"
              role="button"
              @keydown.enter="navigateTo('bios')"
              @keydown.space.prevent="navigateTo('bios')">
          <img src="/bio-icon.png" alt="bio icon"></img>
          Bios
          </div>
        </div>
      <div id="topical">
      <DailyQuote :jwt="jwt" />
      <div class="item-card">
      <GetRandomJoke :jwt="jwt" />
      </div>
      </div>
    </div>
    <UserInfo id="side-bar"
            image="/person.jpg"
            text="Hi there!"
            :name="sideBarName"
            :position="sideBarRole" />
            
    
  </div>
  </div>
  <div class="menu-footer"> 
  copyright 2025</div>
  
  <!-- Randomly flying cute bee -->
  <img 
    src="/cute-bee.png" 
    alt="Cute Bee" 
    class="cute-bee"
    :style="{ left: cuteBeeX + 'px', top: cuteBeeY + 'px' }"
  />
</template>

<style scoped>
.resource-menu-page {
  display:flex;
  flex-direction: column;
  min-height:100vh;
}
#main-content {
  display: flex;
  height: 100vh;
  flex:1;
  align-items: stretch;
}
.menu-footer {
  background-color: var(--color-primary-purple);
  text-align: center;
}
#primary-content {
  flex: 3;
  background: var(--bg-yellow);
  border-radius: 10px;
  padding: 2em;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  flex-direction:column;
  margin: 2em;
}
#side-bar {
  flex: 1;
  flex-direction: column;
  margin-top: 4rem;
}
#resource-menu {
  display: flex
}
.overlay-text{
  background-color: white;
  border-radius:5px;
  padding: 1em 2em;
  margin: 1em;
  
  
}
.welcome-blurb {
  flex-direction:row;
  align-items:center;
  padding:.25em;
  font-size:2em;
  text-align:center;

}


.resource-card {
  text-align: center;
  flex: 1;
  padding: 1em 0em;
  margin: 1em;
  box-shadow: 0 2px 12px rgba(0,0,0,0.12);
  border-radius: 5px;
  position: relative;
  
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.2em;
}

.resource-card img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 1em;
}
#joke.resource-card {
  background: linear-gradient(135deg, var(--color-primary-orange) 0%, var(--color-primary-coral) 100%);
}
#bios.resource-card {
  background: linear-gradient(135deg, var(--color-primary-purple) 0%, var(--color-primary-magenta) 100%);
}
#trivia.resource-card {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary-purple) 100%);
}
#quotes.resource-card {
  background: linear-gradient(135deg, var(--color-primary-magenta) 0%, var(--color-primary-coral) 100%);
}
.resource-card:hover {
  background-color: var(--color-gray-400);
}
.image-container {
  position:relative;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--bg-primary);
  margin-top: 4rem;
}
.overlay-text{
  background-color: var(--bg-primary);
}
#topical {
  display:flex;
}

.item-card {
  background: #e3f2fd;           /* Light blue background */
  padding:1em;
  margin:2em;
  text-align:center;
  flex:1;
  font-style: italic;
}

/* Cute bee - mouse following */
.cute-bee {
  position: fixed;
  width: 60px;
  height: 60px;
  pointer-events: none;
  z-index: 99;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.3));
  transition: all 0.1s linear;
}

</style>