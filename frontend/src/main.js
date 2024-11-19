import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

import VueGoogleMaps from '@fawmi/vue-google-maps'
import './registerServiceWorker'

const app = createApp(App)

window.$ = window.jQuery = require('jquery')

app.use(VueGoogleMaps, {
  load: {
    key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY,
  }
})
app.use(router)
app.mount('#app')




