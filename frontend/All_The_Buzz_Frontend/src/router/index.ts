import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import ResourceMenu from '../views/ResourceMenu.vue'
import Jokes from '../views/Jokes.vue'
import Quotes from '../views/Quotes.vue'
import Bios from '../views/Bios.vue'
import Trivias from '../views/Trivias.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login,
    },
    {
      path: '/menu',
      name: 'resource-menu',
      component: ResourceMenu,
    },
    {
      path: '/jokes',
      name: 'jokes',
      component: Jokes,
    },
    {
      path: '/quotes',
      name: 'quotes',
      component: Quotes,
    },
    {
      path: '/bios',
      name: 'bios',
      component: Bios,
    },
    {
      path: '/trivia',
      name: 'trivia',
      component: Trivias,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutUs.vue'),
    }
  ],
})

export default router
