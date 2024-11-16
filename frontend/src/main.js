import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import ChartKick from 'vue-chartkick'
import 'chartkick/chart.js'
import VueInputAutowidth from 'vue-input-autowidth'
import contenteditable from 'vue-contenteditable'

import GAuth from 'vue3-google-oauth2'
import VueGoogleMaps from '@fawmi/vue-google-maps'
import './registerServiceWorker'
const gauthOption = {
  clientId: '74290392518-v3cmcdkfr7cq1frvuf13f4q1rnq19s2n.apps.googleusercontent.com',
  scope: 'profile email',
  prompt: 'select_account'
}


const app = createApp(App)

window.$ = window.jQuery = require('jquery')

app.use(contenteditable)
app.use(GAuth, gauthOption)
app.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyBWAWOLCKqRM9kuvOueScx8F0Uzw5tMjrM",
  }
})
app.use(VueInputAutowidth)
app.use(router)
app.use(ChartKick)
app.mount('#app')




