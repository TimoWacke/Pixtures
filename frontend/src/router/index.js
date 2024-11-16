
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home'
import Admin from '@/views/Admin'
import Login from '@/views/Login'
import SignUp from '../views/SignUp.vue'
import Site from '@/views/Site'
import Paper from '@/views/Blog'
import Map from '@/views/Map'
import Journal from '@/components/Journal'
import Reset from '@/views/Reset'
import Flyby from '@/views/Flyby'
import axios from 'axios'
import vars from '../assets/vars'
import VueCookie from 'vue-cookies'
import App from '@/App'


let baseRoutes = [
  {
    path: '/profile',
    name: 'Home',
    component: Home
  },
  {
    path: '/website',
    name: 'Website',
    component: Site
  }, {
    path: '/',
    name: 'Paper',
    component: Paper
  }
  , {
    path: '/journal',
    name: 'Journal',
    component: Journal
  },
  {
    path: '/documents',
    name: 'Documents',
    component: Site
  }, {
    path: '/social%20pictures',
    name: 'Social Pictures',
    component: Site
  },
  {
    path: '/fotoshootings',
    name: 'Fotoshootings',
    component: Site
  }, {
    path: '/videoproduktionen',
    name: 'Videoproduktionen',
    component: Site
  }, {
    path: '/picturepoints',
    name: 'PicturePoints',
    component: Site
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  }, {
    path: '/login',
    name: 'Login',
    component: Login
  }, {
    path: '/signup',
    name: 'SignUp',
    component: SignUp
  }, {
    path: '/reset_id',
    name: 'Reset',
    component: Reset
  }, {
    path: '/link',
    name: 'Flyby',
    component: Flyby
  }, {
    path: '/pictures-map',
    name: 'Pictures-Map',
    component: Map
  }
]

const router = createRouter({
  mode: 'history',
  history: createWebHistory(""),
  routes: baseRoutes
})

router.beforeEach(async (to, from, next) => {
  if (to.name == "Flyby" || to.name == "Reset" || to.name == 'Journal') {
    next()
  } else {
    await axios.post(vars.url + '/token', { token: VueCookie.get('session_token') })
      .then((response) => {
        if (response.data && (to.name === 'Login' || to.name === 'Register' || (!response.data.features.includes(to.name) && to.name != 'Home'))) {
          App.store['user'] = response.data
          if (response.data.features.includes("Admin")) {
            next({ name: 'Admin' })
          } else {
            if (response.data.edit.address.street.length > 4 && response.data.edit.address.postcode.length > 3 && response.data.edit.address.city.length > 2) {
              console.log("try paper")
              next({ name: 'Paper' })
            } else {
              next({ name: 'Home' })
            }
          }
        } else if (!response.data && to.name !== 'Login' && to.name !== 'Flyby' && to.name !== 'SignUp') {
          VueCookie.remove("session_token")
          next({ name: 'Login' })
        } else {
          App.store['user'] = response.data
          next()
        }
      })
  }

})
export default router
