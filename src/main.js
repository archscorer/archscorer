/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Composables
import { createApp } from 'vue'
import router from './router'
import store from './store'

// Components
import App from './App.vue'

// Plugins
import { registerPlugins } from '@/plugins'

const app = createApp(App)

registerPlugins(app)

app.use(router)
app.use(store)

app.mount('#app')


// import Vue from 'vue'
// import App from './App.vue'
// import vuetify from './plugins/vuetify'
// import router from './router'
// import store from './store'

// Vue.config.productionTip = false

// new Vue({
//   vuetify,
//   router,
//   store,
//   render: h => h(App)
// }).$mount('#app')
