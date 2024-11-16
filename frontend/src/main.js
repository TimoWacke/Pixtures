import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

import VueGoogleMaps from '@fawmi/vue-google-maps'
import './registerServiceWorker'

const app = createApp(App)

window.$ = window.jQuery = require('jquery')

app.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyBWAWOLCKqRM9kuvOueScx8F0Uzw5tMjrM",
  }
})
app.use(router)
app.mount('#app')




