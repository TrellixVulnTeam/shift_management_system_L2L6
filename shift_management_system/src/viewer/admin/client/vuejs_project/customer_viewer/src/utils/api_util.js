import { Auth } from 'aws-amplify'
import { root } from '@/main.js' // eslint-disable-line no-unused-vars
import EventBus from '@/EventBus.js'
export default {
  methods: {
    async apiNameForLoginUser () { // eslint-disable-line no-unused-vars
      try {
        await Auth.currentSession()
      } catch (e) {
        console.log(e)
        root.$router.replace('/logout')
        return undefined
      }
      const { attributes } = await Auth.currentAuthenticatedUser()
      let env = attributes['custom:ENV']
      return env === 'stg' ? process.env.VUE_APP_API_NAME_STAGING : process.env.VUE_APP_API_NAME
    },
    async getUsername () {
      const { username } = await Auth.currentAuthenticatedUser()
      return username
    },
    async getUserEnv () {
      const { attributes } = await Auth.currentAuthenticatedUser()
      return attributes['custom:ENV']
    },
    async getAuthHeader () {
      return {
        Authorization: (await Auth.currentAuthenticatedUser()).signInUserSession.idToken.jwtToken,
      }
    },
    async isDev () {
      return (await this.getUserEnv()) === 'stg'
    },
    eventBusOn (event, callback) {
      EventBus.$on(event, callback)
      this.$once("hook:beforeDestroy", () => {
        EventBus.$off(event, callback)
      })
    },
    eventBusEmit (event, obj) {
      EventBus.$emit(event, obj)
    },
    lsget (key, defaultt) {
      const obj = root.$localStorage.get(process.env.VUE_APP_LS_KEY)
      return obj[key] != undefined ? obj[key] : defaultt
    },
    lsset (key, value) {
      const obj = root.$localStorage.get(process.env.VUE_APP_LS_KEY)
      obj[key] = value
      root.$localStorage.set(process.env.VUE_APP_LS_KEY, obj)
    },
    lsremove (key) {
      const obj = root.$localStorage.get(process.env.VUE_APP_LS_KEY)
      obj[key] = undefined
      root.$localStorage.set(process.env.VUE_APP_LS_KEY, obj)
    },
  }
}