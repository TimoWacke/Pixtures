
import { createRouter, createWebHistory } from 'vue-router'

import Map from '@/views/Map'


let baseRoutes = [
  {
    path: '/',
    name: 'Pixtures',
    component: Map
  }
]

const router = createRouter({
  mode: 'history',
  history: createWebHistory(""),
  routes: baseRoutes
})

router.beforeEach(async (to, from, next) => {
  to
  from
  next()
  // nothing yet
  }
)

export default router
