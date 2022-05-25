import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import '@mdi/font/css/materialdesignicons.css'
import apiUtil from './utils/api_util.js'
import VueLocalStorage from 'vue-localstorage'

Vue.config.productionTip = false
Vue.use(VueLocalStorage)

window.LOG_LEVEL = process.env.VUE_APP_WINDOW_LOG_LEVEL

Vue.mixin(apiUtil)
const ls_key = process.env.VUE_APP_LS_KEY
const obj = {}
obj[`${ls_key}`] = {
  type: Object,
  default: {},
}
export let root = new Vue({
  router,
  vuetify,
  render: h => h(App),
  localStorage: obj,
}).$mount('#app')