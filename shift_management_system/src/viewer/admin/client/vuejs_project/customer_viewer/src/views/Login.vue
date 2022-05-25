<template>
  <v-app>
    <v-container>
      <v-card class="mt-6">
        <v-card-title :class='appColor + " white--text headline text-left"'>
          {{ appName }}
        </v-card-title>
      </v-card>
      <v-divider/>
      <v-card width="400px" class="mx-auto mt-5">
        <v-card-title>
          <h1 class="display-1">ログイン</h1>
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              prepend-icon="mdi-account-circle"
              label="ユーザ名"
              v-model="username"
              v-on:keyup.enter="login"
            />
            <v-text-field
              v-bind:type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
              prepend-icon="mdi-lock"
              v-bind:append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              label="パスワード"
              v-model="password"
              v-on:keyup.enter="login"
            />
            <v-card-actions>
              <v-btn class="info" @click="login">ログイン</v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
    <Loading v-show="loading"></Loading>

    <v-snackbar
      v-model="showError"
      color="red"
    >
      <div
        v-for="message in errorMessage"
        :key="message"
        >
        {{ message }}
      </div>
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          outlined
          v-bind="attrs"
          @click="showError = false"
        >
          閉じる
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import Amplify, { Auth } from 'aws-amplify'
import Loading from '@/components/Loading'
const awsExports = require('@/aws-exports').default
Amplify.configure(awsExports)
export default {
  name: 'Login',
  components: {
    Loading,
  },
  data () {
    return {
      appName: ``,
      appColor: ``,
      showPassword : false,
      loading: false,
      username:'',
      password:'',
      showError: false,
      errorMessage: [],
    }
  },
  created () {
    this.appName = process.env.VUE_APP_NAME
    this.appColor = process.env.VUE_APP_COLOR
  },
  methods: {
    login () {
      this.loading = true
      const self = this
      Auth.signIn(this.username.trim(), this.password.trim())
        .then(async (data) => { // eslint-disable-line no-unused-vars
          this.$router.replace('/')
        })
        .catch((err) => {
          console.error(err)
          setTimeout(() => {
            self.loading = false
            self.showError = true
            self.errorMessage = [ `ログインできませんでした` ]
          }, 1000)
        })
    }
  }
}
</script>
<style scoped>
.class-login-page {
  margin-top: 50px;
}
.login-form {
  list-style: none;
}
</style>
