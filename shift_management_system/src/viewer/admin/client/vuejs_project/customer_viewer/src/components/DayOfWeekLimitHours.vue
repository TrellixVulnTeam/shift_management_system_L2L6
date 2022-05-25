<template>
  <v-card>
    <v-progress-linear
      indeterminate
      color="primary"
      v-show="showProgress"
      dense
      height="8"
      class="fixed-super-top"
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
    <v-sheet tile width="100vw" height="6vh" color="cyan lighten-3" class="d-flex align-center fixed-top">
      <v-btn icon @click="onClickClose" class="no-print">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-card-text class="fw-bold">曜日別固定上限時間設定</v-card-text>
    </v-sheet>

    <v-form ref="form" id="urunForm" lazy-validation p4 class="mt-8" style="width: 100%;">
      <v-card-text p4>
        <v-select
          v-model="mon"
          label="月曜日"
          :items="items"
          v-on:change="changeSelectBox($event, 'mon')"
          item-text="label"
          item-value="id">
        </v-select>
        <v-select
          v-model="tue"
          label="火曜日"
          :items="items"
          v-on:change="changeSelectBox($event, 'tue')"
          item-text="label"
          item-value="id">
        </v-select>
        <v-select
          v-model="wed"
          label="水曜日"
          :items="items"
          v-on:change="changeSelectBox($event, 'wed')"
          item-text="label"
          item-value="id">
        </v-select>
        <v-select
          v-model="thu"
          label="木曜日"
          :items="items"
          v-on:change="changeSelectBox($event, 'thu')"
          item-text="label"
          item-value="id">
        </v-select>
        <v-select
          v-model="fri"
          label="金曜日"
          :items="items"
          v-on:change="changeSelectBox($event, 'fri')"
          item-text="label"
          item-value="id">
        </v-select>
        <v-select
          v-model="sat"
          label="土曜日"
          :items="items"
          v-on:change="changeSelectBox($event, 'sat')"
          item-text="label"
          item-value="id">
        </v-select>
        <v-select
          v-model="sun"
          label="日曜日"
          :items="items"
          v-on:change="changeSelectBox($event, 'sun')"
          item-text="label"
          item-value="id">
        </v-select>
      </v-card-text>
    </v-form>

    <v-progress-linear
      indeterminate
      color="primary"
      v-show="showProgress"
      dense
      height="8"
      class="fixed-bottom"
    ></v-progress-linear>

    <v-speed-dial
      direction="top"
      transition="slide-y-transition"
      class="bottom-btn no-print"
    >
      <template v-slot:activator>
        <v-btn
          fab
          color="cyan"
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
    </v-speed-dial>
  </v-card>
</template>
<script>
import Vue from 'vue' // eslint-disable-line no-unused-vars
import Amplify, { API, Auth } from 'aws-amplify' // eslint-disable-line no-unused-vars
import $ from 'jquery' // eslint-disable-line no-unused-vars
const awsExports = require('@/aws-exports').default
Amplify.configure(awsExports)
import moment from 'moment'; // eslint-disable-line no-unused-vars
import JsonViewer from 'vue-json-viewer' // eslint-disable-line no-unused-vars
Vue.use(JsonViewer)
export default {
  name: 'DayOfWeekLimitHours',
  props: [ 'showDayOfWeekLimitHours', 'debug' ],
  data: () => ({
    showProgress: false,
    showOverlayLoading: false,
    overlayMessage: ``,
    mon: 0,
    tue: 0,
    wed: 0,
    thu: 0,
    fri: 0,
    sat: 0,
    sun: 0,
    items: [
      { id: 0, label: '上限なし' },
      { id: 1, label: '1時間' },
      { id: 1.5, label: '1.5時間' },
      { id: 2, label: '2時間' },
      { id: 2.5, label: '2.5時間' },
      { id: 3, label: '3時間' },
      { id: 3.5, label: '3.5時間' },
      { id: 4, label: '4時間' },
      { id: 4.5, label: '4.5時間' },
      { id: 5, label: '5時間' },
      { id: 5.5, label: '5.5時間' },
      { id: 6, label: '6時間' },
      { id: 6.5, label: '6.5時間' },
      { id: 7, label: '7時間' },
      { id: 7.5, label: '7.5時間' },
      { id: 8, label: '8時間' },
      { id: 8.5, label: '8.5時間' },
      { id: 9, label: '9時間' },
      { id: 9.5, label: '9.5時間' },
      { id: 10, label: '10時間' },
      { id: 10.5, label: '10.5時間' },
      { id: 11, label: '11時間' },
      { id: 11.5, label: '11.5時間' },
      { id: 12, label: '12時間' },
      { id: 12.5, label: '12.5時間' },
      { id: 13, label: '13時間' },
      { id: 13.5, label: '13.5時間' },
      { id: 14, label: '14時間' },
      { id: 14.5, label: '14.5時間' },
      { id: 15, label: '15時間' },
      { id: 15.5, label: '15.5時間' },
      { id: 16, label: '16時間' },
      { id: 16.5, label: '16.5時間' },
      { id: 17, label: '17時間' },
      { id: 17.5, label: '17.5時間' },
      { id: 18, label: '18時間' },
      { id: 18.5, label: '18.5時間' },
      { id: 19, label: '19時間' },
      { id: 19.5, label: '19.5時間' },
      { id: 20, label: '20時間' },
      { id: 20.5, label: '20.5時間' },
      { id: 21, label: '21時間' },
      { id: 21.5, label: '21.5時間' },
      { id: 22, label: '22時間' },
      { id: 22.5, label: '22.5時間' },
      { id: 23, label: '23時間' },
      { id: 23.5, label: '23.5時間' },
      { id: 24, label: '24時間' },
    ],
  }),
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
    this.eventBusOn('reload-day-of-week-limit-hours', () => {
      this.fetchData(this.onFetchDataSucceeded, this.onFetchDataFailed, true)
    })
    this.fetchData(this.onFetchDataSucceeded, this.onFetchDataFailed, true)
  },
  beforeDestroy: function () {
  },
  mounted () {
  },
  computed: {
  },
  methods: {
    onClickClose () {
      this.eventBusEmit('close-day-of-week-limit-hours')
    },
    changeSelectBox (hours, day) { // eslint-disable-line no-unused-vars
      this.register(day, hours)
    },
    onClickRefresh () {
      this.eventBusEmit('reload-day-of-week-limit-hours', {})
    },
    async fetchData (onSucceeded, onFailed, showLoading) {
      if (showLoading) this.eventBusEmit('show-overlay-loading', { show: true, message: `ロード中...` })
      API.get((await this.apiNameForLoginUser()), `/fetch_day_of_week_limit_hours_data`, { headers: (await this.getAuthHeader()) }).then(response => { // eslint-disable-line no-unused-vars
        if (showLoading) this.eventBusEmit('show-overlay-loading', { show: false, delay: 1000 })

        response.data.forEach(d => {
          let key = Object.keys(d)[0]
          this[key] = d[key];
        })

        if (onSucceeded)
          onSucceeded(response)

      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-overlay-loading', { show: false, delay: 1000 })
        this.eventBusEmit('show-error', { show: true, message: [ `検索に失敗しました！!`, `リロードしてしてください。` ] } )
        console.log('error', error)

        if (onFailed)
          onFailed(error)
      })
    },
    async register (day, hours) {
      this.showProgress = true
      this.eventBusEmit('show-progress', true)
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          day: day,
          hours: hours,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/register_day_of_week_limit_hours`, params).then(response => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.eventBusEmit('show-error', { show: true, message: [ `登録に失敗しました！!`, `しばらく経ってからやり直してください。` ] } )
        console.log('error', error)
      })
    },
    onFetchDataSucceeded (response) { // eslint-disable-line no-unused-vars
    },
    onFetchDataFailed (response) { // eslint-disable-line no-unused-vars
    },
  },
  watch: {
  },
}
</script>
<style lang="scss">
</style>
<style scoped>
.fixed-super-top {
  position: fixed;
  top: 0px;
  z-index: 20003;
}
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