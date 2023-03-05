import { createRouter, createWebHistory } from 'vue-router'

import AboutView from '@/views/AboutView.vue'
import PlaceView from '@/views/PlaceView.vue'
import AfishaView from '@/views/AfishaView.vue'
import AuthView from '@/views/AuthView.vue'
import FilmView from '@/views/FilmView.vue'

const routes = [
  {
    path: '/',
    name: 'afisha',
    component: AfishaView
  },
  {
    path: '/film/:id',
    name: 'Film',
    component: FilmView
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
