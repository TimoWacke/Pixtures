
import { createRouter, createWebHistory } from 'vue-router'

import Map from '@/views/Map'
import Landing from '@/views/Landing'
import ArtPiece from '@/views/ArtPiece.vue'

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
  },
  {
    path: "/art-piece/:id",
    name: "ArtPiece",
    component: ArtPiece,
  }
]

const router = createRouter({
  mode: 'history',
  history: createWebHistory(""),
  routes: baseRoutes
})


export default router
