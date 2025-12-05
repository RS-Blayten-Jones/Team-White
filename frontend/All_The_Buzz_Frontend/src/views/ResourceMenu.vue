<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import UserInfo from '@/components/UserInfo.vue'
import DailyQuote from '@/components/DailyQuote.vue'
import GetRandomJoke from '@/components/GetRandomJoke.vue'

const router = useRouter()

// Cute bee mouse following
const cuteBeeX = ref(Math.random() * window.innerWidth)
const cuteBeeY = ref(Math.random() * window.innerHeight)
let cuteBeeAnimationId: number | null = null
const mouseX = ref(0)
const mouseY = ref(0)

const navigateTo = (resource: string) => {
  router.push({ name: resource })
}

const logout = () => {
  // TODO: Implement logout logic
  router.push({ name: 'login' })
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

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
  animateCuteBee()
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
      <p id="name"> Welcome to the hive, Karl!</p>
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
      <DailyQuote jwt="eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBdXRoIFNlcnZpY2UiLCJsYXN0X25hbWUiOiJTdGVubmluZ3MiLCJsb2NhdGlvbiI6IlVuaXRlZCBTdGF0ZXMiLCJpZCI6OCwiZGVwYXJ0bWVudCI6IkluZm9ybWF0aW9uIFRlY2hub2xvZ3kiLCJ0aXRsZSI6IkRldmVsb3BlciIsImZpcnN0X25hbWUiOiJCYXNpbCIsInN1YiI6IkJhc2lsIFN0ZW5uaW5ncyIsImlhdCI6MTc2NDk1MTA4OSwiZXhwIjoxNzY0OTU0Njg5fQ.vRJppBl2jugKtbn6CHc7kkhkx4DBW2RX-k-SdwKAoc8" />
      <div class="item-card">
      <GetRandomJoke jwt="eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBdXRoIFNlcnZpY2UiLCJsYXN0X25hbWUiOiJTdGVubmluZ3MiLCJsb2NhdGlvbiI6IlVuaXRlZCBTdGF0ZXMiLCJpZCI6OCwiZGVwYXJ0bWVudCI6IkluZm9ybWF0aW9uIFRlY2hub2xvZ3kiLCJ0aXRsZSI6IkRldmVsb3BlciIsImZpcnN0X25hbWUiOiJCYXNpbCIsInN1YiI6IkJhc2lsIFN0ZW5uaW5ncyIsImlhdCI6MTc2NDk1MTA4OSwiZXhwIjoxNzY0OTU0Njg5fQ.vRJppBl2jugKtbn6CHc7kkhkx4DBW2RX-k-SdwKAoc8" />
      </div>
      </div>
    </div>
    <UserInfo id="side-bar"
            image="/person.jpg"
            text="Hi there!"
            name="Karl Jones"
            position="Manager"/>
            
    
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
  background: #FBE6C2;
  border-radius: 10px;
  padding: 2em;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  flex-direction:column;
  margin: 2em;
}
#side-bar {
  flex: 1;
  flex-direction: column;

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
  background: var(--color-primary-orange);
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

.resource-card:hover {
  background-color: var(--color-gray-400);
}
.image-container {
  position:relative;
  display: inline-block;
  align: center;
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