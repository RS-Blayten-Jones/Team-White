<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import UserInfo from '@/components/UserInfo.vue'
import DailyQuote from '@/components/DailyQuote.vue'

const router = useRouter()

const navigateTo = (resource: string) => {
  router.push({ name: resource })
}

const logout = () => {
  // TODO: Implement logout logic
  router.push({ name: 'login' })
}
</script>
<template> 
  <AppHeader title="Buzzword Software - Media Feed" />
  <div class ="resource-menu-page">
  <div id="main-content">
    <div id="primary-content">
      <div class="image-container">
      <div class ="overlay-text"> 
      <div class = "welcome-blurb">
      <p id="welcome">Welcome to the hive, </p>
      <p id="name"> Barbara!</p>
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
      <DailyQuote jwt="eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBdXRoIFNlcnZpY2UiLCJsYXN0X25hbWUiOiJTdGVubmluZ3MiLCJsb2NhdGlvbiI6IlVuaXRlZCBTdGF0ZXMiLCJpZCI6OCwiZGVwYXJ0bWVudCI6IkluZm9ybWF0aW9uIFRlY2hub2xvZ3kiLCJ0aXRsZSI6IkRldmVsb3BlciIsImZpcnN0X25hbWUiOiJCYXNpbCIsInN1YiI6IkJhc2lsIFN0ZW5uaW5ncyIsImlhdCI6MTc2NDg4MTIxOSwiZXhwIjoxNzY0ODg0ODE5fQ.B4lvQBM3vyWmFhEov9VDH8A4bZuj-FIm-1j1tzubs-o" />
      <div class="item-card">
      <p> funny joke here </p>
      </div>
      </div>
    </div>
    <UserInfo id="side-bar"
            image="/person.jpg"
            text="Welcome to the Hive!"
            name="Karl Jones"
            position="Manager"/>
            
    
  </div>
  </div>
  <div class="menu-footer"> 
  copyright 2025</div>
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
  display:flex;
  flex-direction:row;
  align-items:center;

}
#welcome {
  flex:1.2;
  font-size: 1.5em;
  text-align:right;
  padding:.25em;
  font-family: 'Baguet Script', cursive !important;
}
#name {
  flex:1;
  font-size:2em;
  text-align:left;
  padding:.25em;
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
}

#topical {
  display:flex;
}

.item-card {
  background-color:white;
  padding:1em;
  margin:2em;
  text-align:center;
  flex:1;
  font-style: italic;
}


</style>