import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import PlaceView from '@/views/PlaceView.vue'
import AfishaView from '@/views/AfishaView.vue'
import AuthView from '@/views/AuthView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/place',
    name: 'place',
    component: PlaceView
  },
  {
    path: '/afisha',
    name: 'afisha',
    component: AfishaView
  },
  {
    path: '/auth',
    name: 'auth',
    component: AuthView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
