import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

const opts = {
  theme: {
    light: {
      primary: '#3AABD2',
    },
  },
}

export default new Vuetify(opts)