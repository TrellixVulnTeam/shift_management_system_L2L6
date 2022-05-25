import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/Index'
import Login from '@/views/Login'
import Amplify, { Auth } from 'aws-amplify'
import { root } from '@/main.js' // eslint-disable-line no-unused-vars
import moment from 'moment'; // eslint-disable-line no-unused-vars

const awsExports = require('@/aws-exports').default
Amplify.configure(awsExports)

Vue.use(Router)

const requireAuth = (to, from, next) => {
  Auth.currentSession()
    .then(() => {
      next()
    })
    .catch(err => {
      console.log(err)
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    })
}

const checkLogin = (to, from, next) => {
  Auth.currentSession()
    .then(() => {
      next({
        path: '/',
        query: { redirect: to.fullPath }
      })
    })
    .catch(err => {
      console.log(err)
      next()
    })
}

const logout = (to, from, next) => {
  Auth.signOut()
    .then(() => {
      // remove login uername
      /*
      const key = 'username'
      const obj = root.$localStorage.get(process.env.VUE_APP_LS_KEY)
      obj[key] = undefined
      root.$localStorage.set(process.env.VUE_APP_LS_KEY, obj)
      */
      // jump to login page
      next('/login')
    })
    .catch(err => {
      console.log(err)
    })
}

export default new Router({
  mode: 'history',
  base: process.env.NODE_ENV.endsWith('-prod')
    ? `${process.env.BASE_URL}`
    : `/`,
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      beforeEnter: requireAuth
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: checkLogin
    },
    {
      path: '/logout',
      beforeEnter: logout
    }
  ]
})