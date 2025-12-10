<!-- <template>
  <div class="trivias-page page-container">
    <AppHeader />

    <div class="primary-content">
    <main class="content-wrapper" role="main">
      <div class="page-header">
        <div class="page-title-wrapper">
          <div class="icon-wrapper">
            <img src="/trivia-icon.png" alt="Trivia" class="resource-icon" />
          </div>
          <div>
            <h1 class="page-title">Trivia Management</h1>
            <p class="page-subtitle">Bees ace trivia because they're always buzzing with facts</p>
          </div>
        </div>
      </div>
      
    <div class="main-content-layout">
      <div style="width:100%" >
          <button @click="toggleVisibility">
            Toggle View ({{ toggleComponent ? 'Get' : 'Create' }})
          </button>

        <div class="content-area">
          <CreateComponent v-show="!toggleComponent" resourceType="trivias"/> 
          <GetButton v-show="toggleComponent" :isManager="true" jwt="joajlgja" resourceType="trivias"/> comment out 
          <GetButton v-show="toggleComponent" :isManager="isManager" :jwt="jwt" resourceType="trivias"/>
        </div>
          <GetButton :isManager="true" jwt="joajlgja" resourceType="trivias"/> comment out 
      </div>
       
        <div class="mini-resource-cards">
          <div class="mini-card" @click="navigateTo('jokes')" tabindex="0" role="button">
            <img src="/joke-icon.png" alt="Jokes" />
            <span>Jokes</span>
          </div>
          <div class="mini-card" @click="navigateTo('quotes')" tabindex="0" role="button">
            <img src="/quote-icon.png" alt="Quotes" />
            <span>Quotes</span>
          </div>
          <div class="mini-card" @click="navigateTo('bios')" tabindex="0" role="button">
            <img src="/bio-icon.png" alt="Bios" />
            <span>Bios</span>
          </div>
        </div>
        </div>
      </div>
      
    <div class="main-content-layout">
      <div style="width:100%" >
          <button @click="toggleVisibility">
            Toggle View ({{ toggleComponent ? 'Get' : 'Create' }})
          </button>

        <div class="content-area card">
          <CreateComponent v-show="!toggleComponent" resourceType="trivias"/> 
          <GetButton v-show="toggleComponent" :isManager="true" jwt="joajlgja" resourceType="trivias"/>
          <GetButton v-show="toggleComponent" :isManager="isManager" :jwt="jwt" resourceType="trivias"/> comment out 
        </div>
          <GetButton :isManager="true" jwt="joajlgja" resourceType="trivias"/> comment out 
      </div>
      </div>
      </main>

      <div class ="right-hand-side">
        <img src="/tree.png" alt="tree" class="tree"/>
      <div class="fixed-right-image">
        <img src="/Bee-Hive.png" alt="Bee Hive" class="bee-hive" @click="releaseBee" />
      </div>
      </div>
      </div>


    <img 
      v-for="bee in flyingBees" 
      :key="bee.id"
      src="/favicon.ico" 
      alt="Flying Bee" 
      class="flying-bee"
      :style="{ left: bee.x + 'px', top: bee.y + 'px' }"
    />

    <img 
      src="/cute-bee.png" 
      alt="Cute Bee" 
      class="cute-bee"
      :style="{ left: cuteBeeX + 'px', top: cuteBeeY + 'px' }"
    />
  </div>
</template> -->

<template>
  <div class="trivias-page page-container">
    <AppHeader />
   
    <main class="content-wrapper" role="main">
      <div class="page-header">
        <div class="page-title-wrapper">
          <div class="icon-wrapper">
            <img src="/trivia-icon.png" alt="Trivia" class="resource-icon" />
          </div>
          <div>
            <h1 class="page-title">Trivia Management</h1>
            <p class="page-subtitle">Bees ace trivia because they’re always buzzing with facts</p>
          </div>
        </div>
      </div>
     
    <div class="main-content-layout">
      <div style="width:100%" >
          <button @click="toggleVisibility">
            Toggle View ({{ toggleComponent ? 'Get' : 'Create' }})
          </button>
 
        <div class="content-area">
          <CreateComponent v-show="!toggleComponent" resourceType="trivias"/>
          <!-- <GetButton v-show="toggleComponent" :isManager="true" jwt="joajlgja" resourceType="trivias"/> -->
          <GetButton 
            v-show="toggleComponent" 
            :isManager="isManager" 
            :jwt="jwt" 
            resourceType="trivias"
            :filterOptions="triviaFilterOptions"
          />
        </div>
          <!-- <GetButton :isManager="true" jwt="joajlgja" resourceType="trivias"/> -->
      </div>
        <!-- Mini Resource Cards -->
        <div class="mini-resource-cards">
          <div class="mini-card" @click="navigateTo('jokes')" tabindex="0" role="button">
            <img src="/joke-icon.png" alt="Jokes" />
            <span>Jokes</span>
          </div>
          <div class="mini-card" @click="navigateTo('quotes')" tabindex="0" role="button">
            <img src="/quote-icon.png" alt="Quotes" />
            <span>Quotes</span>
          </div>
          <div class="mini-card" @click="navigateTo('bios')" tabindex="0" role="button">
            <img src="/bio-icon.png" alt="Bios" />
            <span>Bios</span>
          </div>
        </div>
      </div>
    </main>
   
    <!-- Bee hive decoration (behind all content) -->
    <img src="/Bee-Hive.png" alt="Bee Hive" class="bee-hive" @click="releaseBee" />
       
    <!-- Flying bees -->
    <img
      v-for="bee in flyingBees"
      :key="bee.id"
      src="/favicon.ico"
      alt="Flying Bee"
      class="flying-bee"
      :style="{ left: bee.x + 'px', top: bee.y + 'px' }"
    />
   
    <!-- Randomly flying cute bee -->
    <img
      src="/cute-bee.png"
      alt="Cute Bee"
      class="cute-bee"
      :style="{ left: cuteBeeX + 'px', top: cuteBeeY + 'px' }"
    />
  </div>
</template>



<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import GetButton from '@/components/Get.vue'
import CreateComponent from '@/components/Create.vue'
import Edit from '@/components/Edit.vue'
import Delete from '@/components/Delete.vue'
import ApproveAndDeny from '@/components/ApproveAndDeny.vue'
import { getCookie } from '@/utils/cookies'

const router = useRouter()

interface Bee {
  id: number
  x: number
  y: number
}

const activeComponent = ref('get')
const flyingBees = ref<Bee[]>([])
let beeIdCounter = 0

// Cute bee random flying
const cuteBeeX = ref(Math.random() * window.innerWidth)
const cuteBeeY = ref(Math.random() * window.innerHeight)
let cuteBeeAnimationId: number | null = null
const mouseX = ref(0)
const mouseY = ref(0)

// Audio for bee buzzing
const beeSound = new Audio('/bee-buzz.mp3')
beeSound.loop = false

// Get JWT and role from cookies
const jwt = ref<string>('')
const role = ref<string>('')
const isManager = ref<boolean>(false)

// Define filter options for trivias (can add filters if needed)
const triviaFilterOptions: any[] = []

onMounted(() => {
  // Get cookies on mount
  jwt.value = getCookie('jwt') || ''
  role.value = getCookie('role') || ''
  
  // Determine if user is manager based on role
  isManager.value = role.value.toLowerCase() === 'manager'
  
  // If no JWT, redirect to login
  if (!jwt.value) {
    router.push({ name: 'login' })
    return
  }
  
  window.addEventListener('mousemove', handleMouseMove)
  animateCuteBee()
})

const navigateTo = (resource: string) => {
  router.push({ name: resource })
}

const releaseBee = () => {
  // Calculate center of beehive (300px width, positioned at right: -30px, top: 10px)
  const hiveWidth = 300
  const hiveHeight = 300 // approximate height
  const hiveCenterX = window.innerWidth + 30 - (hiveWidth / 2)
  const hiveCenterY = 10 + (hiveHeight / 2)
  
  const bee: Bee = {
    id: beeIdCounter++,
    x: hiveCenterX,
    y: hiveCenterY
  }
  
  flyingBees.value.push(bee)
  
  // Play bee sound with increasing volume based on number of bees
  const baseVolume = 0.6
  const volumeIncrease = 0.1
  const newVolume = Math.min(1.0, baseVolume + (flyingBees.value.length - 1) * volumeIncrease)
  
  const buzzSound = beeSound.cloneNode() as HTMLAudioElement
  buzzSound.volume = newVolume
  buzzSound.play().catch(err => console.log('Audio play failed:', err))
  
  animateBee(bee, hiveCenterX, hiveCenterY)
}

const animateBee = (bee: Bee, startX: number, startY: number) => {
  const duration = 4000
  const startTime = Date.now()
  
  // Randomize flight path parameters for each bee
  const amplitude1 = 200 + Math.random() * 300
  const amplitude2 = 150 + Math.random() * 250
  const frequency1 = 2 + Math.random() * 3
  const frequency2 = 2 + Math.random() * 3
  const directionX = Math.random() > 0.5 ? 1 : -1
  const directionY = Math.random() > 0.5 ? 1 : -1
  
  const animate = () => {
    const elapsed = Date.now() - startTime
    const progress = elapsed / duration
    
    if (progress < 1) {
      // Create a randomized swooping flight path starting from the hive center
      const offsetX = Math.sin(progress * Math.PI * frequency1) * amplitude1 * directionX
      const offsetY = Math.cos(progress * Math.PI * frequency2) * amplitude2 * directionY
      
      // Find and update the bee in the array (Vue reactivity)
      const index = flyingBees.value.findIndex(b => b.id === bee.id)
      if (index > -1) {
        flyingBees.value[index] = {
          id: bee.id,
          x: startX + offsetX,
          y: startY + offsetY
        }
      }
      
      requestAnimationFrame(animate)
    } else {
      // Remove bee from array when animation completes
      const index = flyingBees.value.findIndex(b => b.id === bee.id)
      if (index > -1) {
        flyingBees.value.splice(index, 1)
      }
    }
  }
  
  requestAnimationFrame(animate)
}


// === Toggle flag for Create/Get ===
const toggleComponent = ref(false) // false => show Create, true => show Get
const toggleVisibility = () => {
  toggleComponent.value = !toggleComponent.value
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

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  if (cuteBeeAnimationId !== null) {
    cancelAnimationFrame(cuteBeeAnimationId)
  }
})
</script>

<style scoped>
.trivias-page {
  background-color: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.page-header {
  margin-bottom: var(--spacing-xl);
  animation: slideDown 0.5s ease-out;
}

.page-title-wrapper {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.icon-wrapper {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary-purple) 100%);
  border-radius: var(--border-radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: var(--shadow-md);
  animation: pulse 2s ease-in-out infinite;
}

.resource-icon {
  width: 3rem;
  height: 3rem;
  color: var(--text-on-dark);
}

.page-title {
  color: var(--text-primary);
  font-size: var(--font-size-3xl);
  margin: 0;
  font-weight: var(--font-weight-bold);
  line-height: 1.2;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin: 0;
  margin-top: var(--spacing-xs);
}

.content-area {
  display: flex;
  position: relative;
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
}
.primary-content {
  display:flex;
}
.main-content-layout {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

/* Toggle View Button */
.main-content-layout button {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] .main-content-layout button {
  background-color: #2d2d2d;
  color: white;
  border-color: #404040;
}

[data-theme="light"] .main-content-layout button {
  background-color: white;
  color: #1a1a1a;
  border-color: #e0e0e0;
}

.main-content-layout button:hover {
  background-color: #ffd966;
  color: #1a1a1a;
  border-color: #ffd966;
  box-shadow: 0 0 20px rgba(255, 217, 102, 0.7), 0 0 40px rgba(255, 217, 102, 0.5);
  transform: translateY(-2px);
}

.main-content-layout button:active {
  transform: translateY(0);
}

/* Mini Resource Cards */
.mini-resource-cards {
  display: flex;
  flex-direction: row;
  gap: 0.75rem;
  margin-top: 0;
  margin-left: 1.5rem;
  z-index: 10;
  position: relative;
}

.mini-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.2rem 2rem;
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary-purple) 100%);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  height: 5rem;
  width: 5rem;
}

.mini-card:hover {
  transform: translateX(-8px) scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.mini-card:focus {
  outline: 2px solid var(--color-primary-dark);
  outline-offset: 2px;
}

.mini-card img {
  width: 3rem;
  height: 3rem;
  object-fit: contain;
}

.mini-card span {
  font-size: 1rem;
  font-weight: 600;
  color: white;
  text-align: center;
}



/* Animations */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* Fade slide transition for component switching */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Bee hive decoration */
.bee-hive {
  position: fixed;
  top: 2rem;
  right: 2rem;
  width: 13rem;
  height: auto;
  z-index: 6;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
  cursor: pointer;
  transition: transform 0.3s ease;
}

.bee-hive:hover {
  transform: scale(1.05);
}

.bee-hive:active {
  transform: scale(0.95);
}

/* Flying bee */
.flying-bee {
  position: fixed;
  width: 50px;
  height: 50px;
  pointer-events: none;
  z-index: 100;
}

/* Dark mode: white bees */
[data-theme="dark"] .flying-bee {
  filter: brightness(0) invert(1) drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

/* Light mode: black bees */
[data-theme="light"] .flying-bee,
:root:not([data-theme="dark"]) .flying-bee {
  filter: brightness(0) drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

/* Cute bee - random flying */
.cute-bee {
  position: fixed;
  width: 60px;
  height: 60px;
  pointer-events: none;
  z-index: 99;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.3));
  transition: all 0.1s linear;
}

@media (max-width: 768px) {
  .page-title-wrapper {
    gap: var(--spacing-md);
  }
  
  .icon-wrapper {
    width: 48px;
    height: 48px;
  }
  
  .resource-icon {
    width: 28px;
    height: 28px;
  }
  
  .page-title {
    font-size: var(--font-size-2xl);
  }
  
  .bee-hive {
    top: 80px;
    right: 60px;
    width: 180px;
  }
}

.fixed-right-image {
  position: fixed;
  top: 2rem;      /* distance from top */
  right: 4rem;    /* distance from right */
  width: 100%;   /* or use rem/vw for responsive */
  height: auto;
  z-index: 99;   /* above most elements */
}

.right-hand-side {
  position: fixed;
  top: 2rem;
  right: 0;
  width: auto;
  height: auto;
  z-index: 5;
}

.tree {
  position: fixed;
  top: 2rem;
  right: 0;
  width: 400px;
  height: auto;
  z-index: 5;
}


</style>
