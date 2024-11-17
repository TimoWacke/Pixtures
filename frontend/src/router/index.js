
import { createRouter, createWebHistory } from 'vue-router'

import Map from '@/views/Map'
import Landing from '@/views/Landing'


let baseRoutes = [
  {
    path: '/',
    name: 'Landing-Site',
    component: Landing
  },
  {
    path: '/create',
    name: 'Map-Site',
    component: Map
  }
]

const router = createRouter({
  mode: 'history',
  history: createWebHistory(""),
  routes: baseRoutes
})


export default router
