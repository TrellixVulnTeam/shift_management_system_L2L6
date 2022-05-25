<template>
  <v-app>
    <notifications group="notifications" position="top right" classes="notification-style"></notifications>
    <v-main
      v-touch="{
        left: () => swipe('Left'),
        right: () => swipe('Right'),
        up: () => swipe('Up'),
        down: () => swipe('Down')
      }"
    >
      <v-progress-linear
        indeterminate
        color="primary"
        v-show="showProgress"
        dense
        height="8"
        class="fixed-top"
      ></v-progress-linear>
      <v-overlay :value="showOverlayLoading">
        <v-progress-circular
          indeterminate
          size="64"
        ></v-progress-circular>
        <span class="font-weight-bold display-1 ml-2">
          {{ overlayMessage }}
        </span>
      </v-overlay>

      <Calendar :common-events="events" :debug="debug" />

      <v-progress-linear
        indeterminate
        color="primary"
        v-show="showProgress"
        dense
        height="8"
        class="fixed-bottom"
      ></v-progress-linear>

      <v-expansion-panels v-if="debug.value" class="mt-8">
        <v-expansion-panel>
          <v-expansion-panel-header>
            Log
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div class='preview mt-8 mb-2'>
              <div class="w-60 p-3 mb-1 text-left">
                <p>ログ</p>
                <v-row>
                  <v-col>
                    <json-viewer
                      :value="logInfo"
                      :expand-depth=99
                      copyable></json-viewer>
                  </v-col>
                </v-row>
              </div>
            </div>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <Meisai class="mt-10" :user-info="userInfo" :debug="debug" />

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

      <v-snackbar
        v-model="showInfo"
        color="blue"
      >
        <div
          v-for="message in infoMessage"
          :key="message"
          >
          {{ message }}
        </div>
        <template v-slot:action="{ attrs }">
          <v-btn
            text
            outlined
            v-bind="attrs"
            @click="onInfoClick"
          >
            リロード
          </v-btn>
        </template>
      </v-snackbar>

      <v-snackbar
        v-model="showDebug"
        color="rgba(255, 255, 0, 0.5)"
        timeout=3000
        top
        right
      >
        <div
          v-for="message in debugMessage"
          :key="message"
          class="black--text"
          >
          {{ message }}
        </div>
        <template v-slot:action="{ attrs }">
          <v-btn
            text
            outlined
            v-bind="attrs"
            @click="showDebug = false"
            class="black--text"
          >
            閉じる
          </v-btn>
        </template>
      </v-snackbar>

      <v-dialog
        v-model="showSearch"
        max-width="400px"
        @keydown.esc="showSearch = false"
      >
        <v-card>
          <v-card-text>
            <v-date-picker
              v-model="searchYYYYMM"
              type="month"
              min="2021-03"
              locale="ja-jp"
              color="green"
              @click:month="search2"
            ></v-date-picker>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
              text
              @click="showSearch = false"
            >閉じる</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="showAlertDanger"
        max-width="290"
      >
        <v-card color="red lighten-5">
          <v-card-title class="">
            <div
              class="red--text"
              v-for="message in alertMessage"
              :key="message"
              >
              {{ message }}
            </div>
          </v-card-title>
          <v-card-text>よろしいですか？</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="green darken-1"
              text
              :disabled="showProgress"
              @click="onClickDangerOK()"
            >
              はい
            </v-btn>
            <v-btn
              color="grey--text"
              text
              @click="showAlertDanger = false"
            >
              いいえ
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="showAlertWarn"
        max-width="290"
      >
        <v-card color="orange lighten-5">
          <v-card-title class="">
            <div
              class="orange--text"
              v-for="message in alertMessage"
              :key="message"
              >
              {{ message }}
            </div>
          </v-card-title>
          <v-card-text>よろしいですか？</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="green darken-1"
              text
              :disabled="showProgress"
              @click="onClickWarnOK()"
            >
              はい
            </v-btn>
            <v-btn
              color="grey--text"
              text
              @click="showAlertWarn = false"
            >
              いいえ
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="showAlertInfo"
        max-width="290"
      >
        <v-card color="white">
          <v-card-title class="">
            <div
              class="green--text"
              v-for="message in alertMessage"
              :key="message"
              >
              {{ message }}
            </div>
          </v-card-title>
          <v-card-text>よろしいですか？</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="green darken-1"
              text
              :disabled="showProgress"
              @click="onClickInfoOK()"
            >
              はい
            </v-btn>
            <v-btn
              color="grey--text"
              text
              @click="showAlertInfo = false"
            >
              いいえ
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>


      <v-speed-dial
        direction="top"
        transition="slide-y-transition"
        class="bottom-btn"
        :disabled="showOverlayLoading"
      >
        <template v-slot:activator>
          <v-btn
            fab
            color="pink"
            dark
          >
            <v-icon>
              mdi-menu
            </v-icon>
          </v-btn>
        </template>
        <v-btn
          fab
          dark
          small
          color="grey"
          @click="logout1"
        >
          <v-icon>mdi-exit-to-app</v-icon>
        </v-btn>
        <v-btn
          fab
          small
          color="grey lighten-4"
          @click="onClickRefresh"
        >
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
        <v-btn
          fab
          dark
          small
          color="green"
          @click="search1"
        >
          <v-icon>mdi-calendar-search</v-icon>
        </v-btn>
      </v-speed-dial>
    </v-main>
  </v-app>
</template>
<script>
import Vue from 'vue'
import { Auth } from 'aws-amplify'
import Calendar from '@/components/Calendar';
import Meisai from '@/components/Meisai';
import moment from 'moment';
import Notifications from 'vue-notification'
Vue.use(Notifications)
var id = 0
function generateId() { return id++ }
export default {
  name: 'Index',
  components: {
    Calendar, Meisai
  },
  data () {
    return {
      uniqueId: generateId(),
      logInfo: [],
      showProgress: false,
      showError: false,
      showDebug: false,
      showInfo: false,
      showOverlayLoading: false,
      showSearch: false,
      searchYYYYMM: moment().format('yyyy-MM'),
      overlayMessage: ``,
      infoMessage: [],
      errorMessage: [],
      debugMessage: [],
      alertMessage: [],
      events: [],
      calendarInfo: {},
      onInfoClick: (() => {}),

      showAlertDanger: false,
      showAlertWarn: false,
      showAlertInfo: false,
      onClickDangerOK: undefined,
      onClickWarnOK: undefined,
      onClickInfoOK: undefined,

      debug: { value: false },

      focusListener: undefined,
    }
  },
  async created () {
    this.debug.value = (await this.isDev())
    const self = this
    if (true) { // eslint-disable-line no-constant-condition
      var hidden, visibilityState, visibilityChange; // eslint-disable-line no-unused-vars

      if (typeof document.hidden !== "undefined") {
        hidden = "hidden", visibilityChange = "visibilitychange", visibilityState = "visibilityState";
      } else if (typeof document.msHidden !== "undefined") {
        hidden = "msHidden", visibilityChange = "msvisibilitychange", visibilityState = "msVisibilityState";
      }

      var document_hidden = document[hidden];

      this.focusListener = function () {
        if (document_hidden != document[hidden]) {
          if (document[hidden]) {
            // Document hidden
          } else {
            // Document shown
            self.eventBusEmit('show-debug', { show: true, message: [ `focus 3 ${new Date().getTime()} / uniqueId: ${self.uniqueId}` ] })
            // self.$eventBus.$emit('show-debug', { show: true, message: [ `focus 3 ${new Date().getTime()} / uniqueId: ${self.uniqueId}` ] })
          }
          document_hidden = document[hidden];
        }
      }
      document.addEventListener(visibilityChange, this.focusListener)
    }
    this.eventBusOn('show-progress', show => { // eslint-disable-line no-unused-vars
      this.showProgress = show
    })
    console.log(`show-overlay-loading: on`);
    this.eventBusOn('show-overlay-loading', obj => { // eslint-disable-line no-unused-vars
      console.log(`show-overlay-loading: ${obj.show}`);
      setTimeout(() => {
        this.showOverlayLoading = obj.show
        this.overlayMessage = obj.message != undefined ? obj.message : ``
      }, obj.delay != undefined ? obj.delay : 0);
    })
    this.eventBusOn('show-error', obj => { // eslint-disable-line no-unused-vars
      this.showError = obj.show
      this.errorMessage = obj.message
    })
    this.eventBusOn('show-info', obj => { // eslint-disable-line no-unused-vars
      this.showInfo = obj.show
      this.infoMessage = obj.message != undefined ? obj.message : this.infoMessage
      this.onInfoClick = obj.data != undefined && obj.data.click != undefined ? obj.data.click : this.onInfoClick
    })
    this.eventBusOn('put-log', log => { // eslint-disable-line no-unused-vars
      if (this.logInfo.length >= 1000) {
        this.logInfo.pop()
        // this.logInfo.shift()
      }
      this.logInfo.unshift(JSON.stringify({
        timestamp: new Date().getTime(),
        message: log,
      }))
    })
    this.eventBusOn('show-debug', async obj => { // eslint-disable-line no-unused-vars
      if (this.debug.value === false) return
      if (obj.show) {
        if (obj.message) {
          for (let messe of obj.message) {
            this.$notify({
              title: `${messe} / ${(await this.getUserEnv())}`,
              text: ``,
              duration: 3000,
              group: 'notifications',
              type: `warn`,
              closeOnClick: true,
            })
          }
        }
      }
    })
    this.eventBusOn('show-alert-danger', obj => { // eslint-disable-line no-unused-vars
      this.showAlertDanger = obj.show
      this.alertMessage = obj.message
      this.onClickDangerOK = obj.ok
    })
    this.eventBusOn('show-alert-warn', obj => { // eslint-disable-line no-unused-vars
      this.showAlertWarn = obj.show
      this.alertMessage = obj.message
      this.onClickWarnOK = obj.ok
    })
    this.eventBusOn('show-alert-info', obj => { // eslint-disable-line no-unused-vars
      this.showAlertInfo = obj.show
      this.alertMessage = obj.message
      this.onClickInfoOK = obj.ok
    })
    this.eventBusOn('data-changed', data => { // eslint-disable-line no-unused-vars
      let newCalendarInfo = data.calendarInfo
      this.searchYYYYMM = moment(newCalendarInfo.start.date).format('yyyy-MM')
    })
    this.eventBusOn('click-search', () => { // eslint-disable-line no-unused-vars
      this.showSearch = true
    })
    setTimeout(() => {
      self.eventBusEmit('check-app-was-updated')
    }, 1000)
  },
  beforeDestroy: function () {
    var hidden, visibilityState, visibilityChange; // eslint-disable-line no-unused-vars
    if (typeof document.hidden !== "undefined") {
      hidden = "hidden", visibilityChange = "visibilitychange", visibilityState = "visibilityState";
    } else if (typeof document.msHidden !== "undefined") {
      hidden = "msHidden", visibilityChange = "msvisibilitychange", visibilityState = "msVisibilityState";
    }
    document.removeEventListener(visibilityChange, this.focusListener)
  },
  computed: {
  },
  methods: {
   swipe (direction) {
      this.eventBusEmit('swipe-detected', direction)
      switch (direction) {
        case `Left`:
          break;
        case `Right`:
          break;
        case `Up`:
          break;
        case `Down`:
          break;
        default:
          break;
      }
    },
    logout1 () {
      this.eventBusEmit('show-alert-info', {
        show: true, message: [ `ログアウトします。` ], ok: this.logout2
      })
    },
    logout2 () {
      Auth.signOut()
        .then(() => {
          this.$router.replace('/login')
        })
        .catch((err) => {
          console.log('error', err)
        })
    },
    search1 () {
      this.showSearch = true
    },
    search2 (yyyymm) {
      this.showSearch = false
      this.eventBusEmit('change-month', yyyymm)
    },
    onClickRefresh () {
      this.eventBusEmit('reload-shift')
    },
  },
  mounted () {
  },
  watch: {
  },
}
</script>
<style scoped>
.fixed-top {
  position: fixed;
  top: 0px;
  z-index: 2001;
}
.fixed-bottom {
  position: fixed;
  bottom: 0px;
  z-index: 2001;
}
.bottom-btn {
  position: fixed;
  bottom: 0px;
  right: 16px;
  margin: 0 0 16px 16px;
}
</style>
<style lang="scss" scoped>
.notification-style {
  padding: 10px;
  margin: 0 5px 5px;

  font-size: 12px;

  color: #ffffff;
  &.info {
    background: #44A4FC99;
    border-left-color: #075cb199;
  }
  &.warn {
    background: #ffb64899;
    border-left-color: #f48a0699;
  }
  &.error {
    background: #E54D4299;
    border-left-color: #B82E2499;
  }
  &.success {
    background: #68CD8699;
    border-left-color: #42A85F99;
  }
}
</style>