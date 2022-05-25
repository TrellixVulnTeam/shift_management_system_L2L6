<template>
  <div
    v-touch="{
      left: () => swipe('Left'),
      right: () => swipe('Right'),
      up: () => swipe('Up'),
      down: () => swipe('Down')
    }"
    class="white"
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

    <Calendar :show-shift="showShift" :user-info="userInfo" :common-events="events" :is-locked="isLocked" :debug="debug" />

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

    <v-sheet tile width="100vw" height="5vh" color="white" class=""></v-sheet>

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
      class="bottom-btn no-print"
    >
      <template v-slot:activator>
        <v-btn
          fab
          color="pink"
          dark
          :disabled="showOverlayLoading"
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
        @click="onClickClose"
      >
        <v-icon>mdi-close</v-icon>
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
        v-if="isLocked.value"
        fab
        dark
        small
        color="#1AED1A"
        @click="onClickUnLock1"
      >
        <v-icon>mdi-lock-open-variant</v-icon>
      </v-btn>
      <v-btn
        v-else
        fab
        dark
        small
        color="red"
        @click="onClickLock1"
      >
        <v-icon>mdi-lock</v-icon>
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
  </div>
</template>
<script>
import { API } from 'aws-amplify'
import Calendar from '@/components/Calendar';
import Meisai from '@/components/Meisai';
import moment from 'moment';
export default {
  name: 'Shift',
  props: [ 'showShift', 'userInfo', 'debug' ],
  components: {
    Calendar, Meisai
  },
  data () {
    return {
      isLocked: { value: false },

      logInfo: [],
      showProgress: false,
      showInfo: false,
      showError: false,
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
    }
  },
  async created () {
    this.eventBusOn('show-progress', show => { // eslint-disable-line no-unused-vars
      this.showProgress = show
    })
    this.eventBusOn('show-overlay-loading', obj => { // eslint-disable-line no-unused-vars
      setTimeout(() => {
        this.showOverlayLoading = obj.show
        this.overlayMessage = obj.message != undefined ? obj.message : ``
      }, obj.delay != undefined ? obj.delay : 0);
    })
    this.eventBusOn('show-info-shift', obj => { // eslint-disable-line no-unused-vars
      this.showInfo = obj.show
      this.infoMessage = obj.message != undefined ? obj.message : this.infoMessage
      this.onInfoClick = obj.data != undefined && obj.data.click != undefined ? obj.data.click : this.onInfoClick
    })
    this.eventBusOn('show-error-shift', obj => { // eslint-disable-line no-unused-vars
      this.showError = obj.show
      this.errorMessage = obj.message
    })
    this.eventBusOn('put-log', log => { // eslint-disable-line no-unused-vars
      if (this.logInfo.length >= 1000) {
        this.logInfo.pop()
      }
      this.logInfo.unshift(JSON.stringify({
        timestamp: new Date().getTime(),
        message: log,
      }))
    })
    this.eventBusOn('data-changed', data => { // eslint-disable-line no-unused-vars
      let newCalendarInfo = data.calendarInfo
      this.searchYYYYMM = moment(newCalendarInfo.start.date).format('yyyy-MM')
    })
    this.eventBusOn('click-search', () => { // eslint-disable-line no-unused-vars
      this.showSearch = true
    })
    this.eventBusOn('close-shift', userInfo => { // eslint-disable-line no-unused-vars
    })
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
    onClickLock1 () {
      this.eventBusEmit('show-alert-danger', {
        show: true, message: [ `このシフトをロックします。`, `（${this.userInfo.username}さんはこのシフトを編集できなくなります）` ], ok: this.onClickLock2
      })
    },
    async onClickLock2 () {
      this.showProgress = true
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userId: this.userInfo.userId,
          yyyymm: this.searchYYYYMM,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/lock_shift`, params).then(response => { // eslint-disable-line no-unused-vars
        this.isLocked.value = true
        this.showProgress = false
        this.eventBusEmit('show-alert-danger', { show: false })
        this.eventBusEmit('shift-locked', { userId: this.userInfo.userId, yyyymm: this.searchYYYYMM })
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.eventBusEmit('show-error-shift', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    onClickUnLock1 () {
      this.eventBusEmit('show-alert-info', {
        show: true, message: [ `このシフトのロックを解除します。`, `（${this.userInfo.username}さんはこのシフトを編集できるようになります）` ], ok: this.onClickUnLock2
      })
    },
    async onClickUnLock2 () {
      this.showProgress = true
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userId: this.userInfo.userId,
          yyyymm: this.searchYYYYMM,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/unlock_shift`, params).then(response => { // eslint-disable-line no-unused-vars
        this.isLocked.value = false
        this.showProgress = false
        this.eventBusEmit('show-alert-info', { show: false })
        this.eventBusEmit('shift-unlocked', { userId: this.userInfo.userId, yyyymm: this.searchYYYYMM })
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.eventBusEmit('show-error-shift', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    onClickClose () {
      this.eventBusEmit('close-shift')
    },
    onClickRefresh () {
      this.eventBusEmit('reload-shift', { userInfo: this.userInfo })
    },
    search1 () {
      this.showSearch = true
    },
    search2 (yyyymm) {
      this.showSearch = false
      this.eventBusEmit('change-month', yyyymm)
    },
  },
  mounted () {
  },
  beforeDestroy () {
  },
  watch: {
  },
}
</script>
<style scoped>
.fixed-top {
  position: fixed;
  top: 0px;
  z-index: 20002;
}
.fixed-bottom {
  position: fixed;
  bottom: 0px;
  z-index: 20002;
}
.bottom-btn {
  position: fixed;
  bottom: 0px;
  right: 16px;
  margin: 0 0 16px 16px;
}
.bottom-btn-left {
  position: fixed;
  margin: 0 0 0px 0px;
}
</style>