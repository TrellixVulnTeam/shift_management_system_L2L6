<template>
  <div
    class="white limit-hours-dialog"
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

    <v-sheet tile width="100vw" height="6vh" color="purple lighten-3" class="d-flex align-center fixed-top">
      <v-btn icon @click="onClickClose" class="no-print">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-btn outlined small class="text-h6">
        上限時間設定
      </v-btn>
      <div class="show-on-print">&nbsp;&nbsp;</div>
      <v-btn icon small @click="$refs.calendar.prev()" class="no-print">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-btn icon small @click="$refs.calendar.next()" class="no-print">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-btn icon small @click="onClickSearch" class="no-print">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-sheet>
    <v-sheet tile min-height="6vh" color="grey lighten-3" class="text--transparent">
      &nbsp;&nbsp;
    </v-sheet>
    <v-sheet width="97vw" height="94vh" class="">
      <v-calendar
        v-show="showCalendar"
        ref="calendar"
        :now="now"
        :value="today"
        color="purple lighten-2"
        v-model="today"
        :events="events"
        :event-color="getEventColor"
        locale="ja-jp"
        :day-format="(timestamp) => new Date(timestamp.date).getDate()"
        :month-format="(timestamp) => new Date(timestamp.date).getMonth() + 1 + ' /'"
        @change="onChange"
        @click:event="showEvent"
        @click:day="clickDay"
        @click:date="clickDay"
        >
      </v-calendar>
    </v-sheet>

    <div class="no-print">
      <v-expansion-panels v-if="debug.value">
        <v-expansion-panel>
          <v-expansion-panel-header>
            Debug
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div class='preview mt-8 mb-2'>
              <div class="w-60 p-3 mb-1 text-left">
                <p>プレビュー</p>
                <v-row>
                  <v-col>
                    <json-viewer
                      :value="limitHours"
                      :expand-depth=99
                      copyable></json-viewer>
                  </v-col>
                </v-row>
              </div>
            </div>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>

    <v-progress-linear
      indeterminate
      color="primary"
      v-show="showProgress"
      dense
      height="8"
      class="fixed-bottom"
    ></v-progress-linear>

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

    <v-row justify="center">
      <v-dialog
        v-model="showForm"
        max-width="600px"
        @keydown.esc="showForm = false"
      >
        <v-card>
          <v-card-title>
            <span class="headline">{{ selectedDateFormatted }}</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                  sm="6"
                >
                  <v-select
                    v-model="selectedHours"
                    :items="hourList"
                    label="上限時間*"
                    item-text="label"
                    item-value="value">
                  ></v-select>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="blue darken-1"
              text
              @click="showForm = false"
            >
              閉じる
            </v-btn>
            <v-btn
              color="blue darken-1"
              text
              @click="register()"
            >
              保存
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>

    <v-speed-dial
      direction="top"
      transition="slide-y-transition"
      class="bottom-btn no-print"
    >
      <template v-slot:activator>
        <v-btn
          fab
          color="purple lighten-2"
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
import Vue from 'vue' // eslint-disable-line no-unused-vars
import Amplify, { API, Auth } from 'aws-amplify' // eslint-disable-line no-unused-vars
import $ from 'jquery' // eslint-disable-line no-unused-vars
const awsExports = require('@/aws-exports').default
Amplify.configure(awsExports)
import moment from 'moment'; // eslint-disable-line no-unused-vars
import JsonViewer from 'vue-json-viewer'
Vue.use(JsonViewer)
export default {
  name: 'LimitHours',
  props: [ 'showLimitHours', 'debug' ],
  data: () => ({
    now: undefined,
    today: moment().format('yyyy-MM-DD'),
    showCalendar: false,
    showProgress: false,
    events: [],
    limitHours: [],
    regularHolidays: [],
    dayOfWeekLimitHoursData: [],
    alertMessage: [],
    calendarInfo: {},
    showOverlayLoading: false,
    overlayMessage: ``,
    showSearch: false,
    requests: [],

    showForm: false,
    selectedHours: undefined,
    selectedDate: undefined,

    showAlertInfo: false,
    showAlertDanger: false,

    onClickInfoOK: undefined,
    onClickDangerOK: undefined,

    searchYYYYMM: moment().format('yyyy-MM'),

    hourList: [
      { label: `上限なし`, value: 0, },
      { label: `1時間`, value: 1, },
      { label: `1.5時間`, value: 1.5, },
      { label: `2時間`, value: 2, },
      { label: `2.5時間`, value: 2.5, },
      { label: `3時間`, value: 3, },
      { label: `3.5時間`, value: 3.5, },
      { label: `4時間`, value: 4, },
      { label: `4.5時間`, value: 4.5, },
      { label: `5時間`, value: 5, },
      { label: `5.5時間`, value: 5.5, },
      { label: `6時間`, value: 6, },
      { label: `6.5時間`, value: 6.5, },
      { label: `7時間`, value: 7, },
      { label: `7.5時間`, value: 7.5, },
      { label: `8時間`, value: 8, },
      { label: `8.5時間`, value: 8.5, },
      { label: `9時間`, value: 9, },
      { label: `9.5時間`, value: 9.5, },
      { label: `10時間`, value: 10, },
      { label: `10.5時間`, value: 10.5, },
      { label: `11時間`, value: 11, },
      { label: `11.5時間`, value: 11.5, },
      { label: `12時間`, value: 12, },
      { label: `12.5時間`, value: 12.5, },
      { label: `13時間`, value: 13, },
      { label: `13.5時間`, value: 13.5, },
      { label: `14時間`, value: 14, },
      { label: `14.5時間`, value: 14.5, },
      { label: `15時間`, value: 15, },
      { label: `15.5時間`, value: 15.5, },
      { label: `16時間`, value: 16, },
      { label: `16.5時間`, value: 16.5, },
      { label: `17時間`, value: 17, },
      { label: `17.5時間`, value: 17.5, },
      { label: `18時間`, value: 18, },
      { label: `18.5時間`, value: 18.5, },
      { label: `19時間`, value: 19, },
      { label: `19.5時間`, value: 19.5, },
      { label: `20時間`, value: 20, },
      { label: `20.5時間`, value: 20.5, },
      { label: `21時間`, value: 21, },
      { label: `21.5時間`, value: 21.5, },
      { label: `22時間`, value: 22, },
      { label: `22.5時間`, value: 22.5, },
      { label: `23時間`, value: 23, },
      { label: `23.5時間`, value: 23.5, },
      { label: `24時間`, value: 24, },
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
    setTimeout(() => {
      this.drawHolyday()
      this.showCalendar = true
    }, 0)
  },
  beforeDestroy: function () {
  },
  mounted () {
    this.eventBusOn('reload-limit-hours', data => {
      if (data.today != undefined) {
        this.today = data.today
      }
      this.limitHours = []
      this.regularHolidays = []
      this.onChange(this.calendarInfo)
    })
    this.eventBusOn('change-month', yyyymm => { // eslint-disable-line no-unused-vars
      this.today = moment(`${yyyymm.replaceAll('-', '/')}/01`).format('yyyy-MM-DD')
    })
    this.eventBusOn('close-limit-hours', userInfo => { // eslint-disable-line no-unused-vars
    })
  },
  computed: {
    title () {
      return moment(this.today).format('YY年M月');
    },
    selectedDateFormatted () {
      if (this.selectedDate) {
        let splited = this.selectedDate.split('-')
        return moment({ years: splited[0], months: Number(splited[1]) - 1, days: splited[2] }).format("YYYY年 M月 D日")
      }
      return ``
    },
  },
  methods: {
    swipe (direction) {
      this.eventBusEmit('swipe-detected', direction)
      switch (direction) {
        case `Left`:
          this.$refs.calendar.next()
          break;
        case `Right`:
          this.$refs.calendar.prev()
          break;
        case `Up`:
          break;
        case `Down`:
          break;
        default:
          break;
      }
    },
    drawHolyday () {
      console.log(`drawHoliday start`);
      let year = this.calendarInfo.start.year
      let month = this.calendarInfo.start.month
      let momented = moment(`${year}/${month}/1`)
      let yyyym = { yyyy: momented.format('yyyy'), m: momented.format('M') }
      let yyyymPrev = { yyyy: momented.add(-1, 'M').format('yyyy'), m: momented.format('M') }
      let yyyymNext = { yyyy: momented.add(+2, 'M').format('yyyy'), m: momented.format('M') }
      let outsideSlashAppeared = false
      let _yyyym = yyyymPrev
      let isThisMonthFirstDayComing = false
      let _index = 0
      $(".limit-hours-dialog .v-calendar-weekly__day").each((index, element) => { // eslint-disable-line no-unused-vars
        _index = index
        let child = $($(element).find('.v-calendar-weekly__day-label'))
        let dateButton = $(child.find('.v-btn__content'))

        let yyyymmdd = undefined
        let date = dateButton.html()

        if (!outsideSlashAppeared) {
          let splited = date.split('/')
          if (splited.length === 2) {
            date = splited[splited.length - 1].trim()
            outsideSlashAppeared = true
          }
        }

        function explodeToMonthAndDay (date) {
          let splited = date.split('/')
          if (splited.length === 2) {
            return { m: splited[0].trim(), d: splited[1].trim() }
          }
          return { m: undefined, d: date.trim() }
        }
        let monthAndDay = explodeToMonthAndDay(date)

        if (monthAndDay.d === '1') {
          if (isThisMonthFirstDayComing) {
            _yyyym = yyyymNext
          } else {
            _yyyym = yyyym
            isThisMonthFirstDayComing = true
          }
        }
        if (monthAndDay.m === undefined) {
          yyyymmdd = moment(`${_yyyym.yyyy}/${_yyyym.m}/${date}`).format(`yyyy-MM-DD`)
        } else {
          yyyymmdd = moment(`${_yyyym.yyyy}/${monthAndDay.m}/${monthAndDay.d}`).format(`yyyy-MM-DD`)
        }
        console.log(`yyyymmdd: ${yyyymmdd}`);

        /*
        if (monthAndDay.m === undefined) {
          if ($(element).hasClass('v-outside')) {
            if (outsideSlashAppeared) {
              yyyymmdd = moment(`${yyyymNext.yyyy}/${yyyymNext.m}/${date}`).format(`yyyy-MM-DD`)
            } else {
              yyyymmdd = moment(`${yyyymPrev.yyyy}/${yyyymPrev.m}/${date}`).format(`yyyy-MM-DD`)
            }
          } else {
            yyyymmdd = moment(`${yyyym.yyyy}/${yyyym.m}/${date}`).format(`yyyy-MM-DD`)
          }
        } else {
          yyyymmdd = moment(`${yyyym.yyyy}/${monthAndDay.m}/${monthAndDay.d}`).format(`yyyy-MM-DD`)
        }
        */

        if (this.isSunday(yyyymmdd)) {
          $(element).addClass('sunday')
        }
        else
        if (this.isSaturday(yyyymmdd)) {
          $(element).addClass('saturday')
        }
        else
        {
          $(element).removeClass('saturday')
          $(element).removeClass('sunday')
        }

        let isRegularHoliday = false
        child.removeClass('regular-holiday')
        $(child.find('#xxxx')).remove()
        if (this.isRegularHoliday(yyyymmdd)) {
          isRegularHoliday = true
          // console.log(`isRegularHoliday=${this.isRegularHoliday(yyyymmdd)} / ${yyyymmdd}`);
          child.addClass('regular-holiday')
          let $ele = $('<div />', { id: 'xxxx', class: 'regular-holiday-label' }).append('定休日');
          child.prepend($ele)
        }

        let hasLimitHours = false // eslint-disable-line no-unused-vars
        child.removeClass('limit-hours')
        child.removeClass('fail')
        $(child.find('#yyyy')).remove()
        if (!isRegularHoliday) {
          let limitHours = this.getLimitHours(yyyymmdd)
          if (limitHours != undefined) {
            hasLimitHours = true
            child.addClass('limit-hours')
            let $ele = $('<div />', { id: 'yyyy', class: 'limit-hours-label' }).append(`上限${limitHours.hours}時間`);
            child.prepend($ele)
            if (this.getLimitHoursError(yyyymmdd)) {
              child.addClass('fail')
            }
          }
        }

        child.removeClass('day-of-week-limit-hours')
        $(child.find('#zzzz')).remove()
        if (!isRegularHoliday && !hasLimitHours) {
          let dayOfWeekLimitHours = this.getDayOfWeekLimitHours(yyyymmdd)
          if (dayOfWeekLimitHours != undefined) {
            child.addClass('day-of-week-limit-hours')
            let $ele = $('<div />', { id: 'zzzz', class: 'day-of-week-limit-hours-label' }).append(`上限${dayOfWeekLimitHours}時間`);
            child.prepend($ele)
          }
        }
      })
      console.log(`drawHoliday end / index: ${_index}`);
    },
    onClickClose () {
      this.eventBusEmit('close-limit-hours')
    },
    onClickSearch () {
      this.eventBusEmit('click-search')
    },
    onClickRefresh () {
      this.eventBusEmit('reload-limit-hours', {})
    },
    search1 () {
      this.showSearch = true
    },
    search2 (yyyymm) {
      this.showSearch = false
      this.eventBusEmit('change-month', yyyymm)
    },
    async getAuthHeader () {
      return {
        Authorization: (await Auth.currentAuthenticatedUser()).signInUserSession.idToken.jwtToken,
      }
    },
    pushDate (request) {
      const formatted = request.date.replaceAll('-', '')
      for (let date of this.limitHours) {
        if (date.yyyymmdd == formatted) {
          // 既存のものは消す
          this.limitHours.splice(this.limitHours.indexOf(date), 1)
          break
        }
      }
      this.limitHours.push({ yyyymmdd: formatted, hours: request.hours, error: request.error })
    },
    pullDate (request) {
      for (let date of this.limitHours) {
        if (date.yyyymmdd == request.date) {
          // 既存のものは消す
          this.limitHours.splice(this.limitHours.indexOf(date), 1)
          break
        }
      }
    },
    findDate (request) {
      for (let date of this.limitHours) {
        if (date.yyyymmdd == request.date) {
          return date
        }
      }
    },
    getLimitHours (yyyymmdd) {
      yyyymmdd = yyyymmdd.replaceAll('-', '')
      for (let _data of this.limitHours) {
        // console.log(_data);
        if (yyyymmdd === _data.yyyymmdd) {
          /*
          if (_data.hours > 0 ? _data : undefined) {
            console.log(`getLimitHours: ${yyyymmdd} / ${_data.yyyymmdd}`);
            console.log(_data);
          }
          */
          return _data.hours > 0 ? _data : undefined
        }
      }
      return undefined
    },
    getLimitHoursError (yyyymmdd) {
      for (let _date of this.limitHours) {
        if (yyyymmdd === _date.yyyymmdd) {
          return _date.error === true
        }
      }
      return false
    },
    getDayOfWeekLimitHours (yyyymmdd) {
      const dayNumber = moment(yyyymmdd.replaceAll('-', '/')).format('d')
      for (let _data of this.dayOfWeekLimitHoursData) {
        let day = Object.keys(_data)[0]
        if (day === 'mon' && dayNumber == 1 && _data[day] > 0) {
          return _data[day]
        }
        else if (day === 'tue' && dayNumber == 2 && _data[day] > 0) {
          return _data[day]
        }
        else if (day === 'wed' && dayNumber == 3 && _data[day] > 0) {
          return _data[day]
        }
        else if (day === 'thu' && dayNumber == 4 && _data[day] > 0) {
          return _data[day]
        }
        else if (day === 'fri' && dayNumber == 5 && _data[day] > 0) {
          return _data[day]
        }
        else if (day === 'sat' && dayNumber == 6 && _data[day] > 0) {
          return _data[day]
        }
        else if (day === 'sun' && dayNumber == 0 && _data[day] > 0) {
          return _data[day]
        }
      }
      return undefined
    },
    isSaturday (yyyymmdd) {
      return moment(yyyymmdd.replaceAll('-', '/')).format('d') == 6;
    },
    isSunday (yyyymmdd) {
      return moment(yyyymmdd.replaceAll('-', '/')).format('d') == 0;
    },
    isCurrMonth (today, month) {
      return moment(today.replaceAll('-', '/')).format(`M`) == month;
    },
    isRegularHoliday (yyyymmdd) {
      for (let _date of this.regularHolidays) {
        if (yyyymmdd === _date.yyyymmdd) {
          return true
        }
      }
      return false
    },
    isRegularHolidayError (yyyymmdd) {
      for (let _date of this.regularHolidays) {
        if (yyyymmdd === _date.yyyymmdd) {
          return _date.error === true
        }
      }
      return false
    },
    onDate (date, month, today, past) { // eslint-disable-line no-unused-vars
      // console.log(`date: ${date}`);
      return `#00000000`
    },
    getDateColor (date, month, today, past) { // eslint-disable-line no-unused-vars
      if (!this.isCurrMonth(today, month)) {
        return `#00000000`
      }
      if (this.isSaturday(date)) {
        return `#4169e122`
      }
      if (this.isSunday(date)) {
        return `#FF000022`
      }
      return `#00000000`
    },
    showEvent({ event }) { // eslint-disable-line no-unused-vars
      // alert(`clicked ${event.name}`);
    },
    clickDay({ date }) { // eslint-disable-line no-unused-vars

      var findHours = (targetDate) => {
        for (let l of this.limitHours) {
          if (l.yyyymmdd.replaceAll('-', '') === targetDate.replaceAll('-', '')) {
            return l.hours
          }
        }
        let hours = this.getDayOfWeekLimitHours(targetDate)
        console.log(`targetDate: ${targetDate} / hours: ${hours}`);
        return hours > 0 ? hours : this.hourList[0].value
      }

      this.showForm = true
      this.selectedDate = date
      this.selectedHours = findHours(date)
    },
    async fetchData (yyyymm, onSucceeded, onFailed, showLoading) {
      if (showLoading) this.eventBusEmit('show-overlay-loading', { show: true, message: `${yyyymm}...` })
      API.get((await this.apiNameForLoginUser()), `/fetch_limit_hours_data/${yyyymm}`, { headers: (await this.getAuthHeader()) }).then(response => { // eslint-disable-line no-unused-vars
        console.log(response);
        if (showLoading) this.eventBusEmit('show-overlay-loading', { show: false, delay: 1000 })
        // console.log(response);
        this.eventBusEmit('show-debug', { show: true, message: [ `fetchData: ${yyyymm} / uniqueId: ${this.uniqueId}` ] })
        response.data.forEach(data => {
          for (let l of this.limitHours) {
            if (l.yyyymmdd === data.yyyymmdd) {
              // 既存のものは消す
              this.limitHours.splice(this.limitHours.indexOf(l), 1)
              break
            }
          }

          this.limitHours.push({
            yyyymmdd: data.yyyymmdd,
            hours: data.hours,
          })
        })

        // また、無くなっているものも消す
        let deleteIdxList = []
        for (let l of this.limitHours) {
          let _yyyymm = moment(l.yyyymmdd.replaceAll('-', '/')).format(`YYYY-MM`)
          if (yyyymm === _yyyymm) {
            let exists = false
            response.data.forEach(data => {
              if (data.yyyymmdd == l.yyyymmdd) {
                exists = true
              }
            })

            if (!exists)
              deleteIdxList.push(this.limitHours.indexOf(l))
          }
        }
        deleteIdxList.forEach(idx => {
          this.limitHours[idx] = undefined
        })
        this.limitHours = this.limitHours.filter(Boolean)

        if (true) { // eslint-disable-line no-constant-condition
          // 定休日
          response.regular_holiday_data.forEach(yyyymmdd => {
            for (let date of this.regularHolidays) {
              if (date.yyyymmdd === yyyymmdd) {
                // 既存のものは消す
                this.regularHolidays.splice(this.regularHolidays.indexOf(date), 1)
                break
              }
            }

            this.regularHolidays.push({
              yyyymmdd: yyyymmdd,
            })
          })

          // また、無くなっているものも消す
          let deleteIdxList = []
          for (let date of this.regularHolidays) {
            let _yyyymm = moment(date.yyyymmdd.replaceAll('-', '/')).format(`YYYY-MM`)
            if (yyyymm === _yyyymm) {
              let exists = false
              response.regular_holiday_data.forEach(yyyymmdd => {
                if (yyyymmdd == date.yyyymmdd) {
                  exists = true
                }
              })

              if (!exists)
                deleteIdxList.push(this.regularHolidays.indexOf(date))
            }
          }
          deleteIdxList.forEach(idx => {
            this.regularHolidays[idx] = undefined
          })
          this.regularHolidays = this.regularHolidays.filter(Boolean)
        }

        if (true) { // eslint-disable-line no-constant-condition
          // 曜日別上限時間
          this.dayOfWeekLimitHoursData = response.day_of_week_limit_hours_data
        }

        if (onSucceeded)
          onSucceeded(response)

        this.$nextTick(() => { this.drawHolyday() })

      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-overlay-loading', { show: false, delay: 1000 })
        this.eventBusEmit('show-error', { show: true, message: [ `検索に失敗しました！!`, `リロードしてしてください。` ] } )
        console.log('error', error)

        if (onFailed)
          onFailed(error)
      })
    },
    onFetchDataSucceeded (response) { // eslint-disable-line no-unused-vars
    },
    register () {

      const self = this
      const processOK = () => {

        self.showForm = false
        self.showAlertDanger = false
        self.onClickDangerOK = undefined

        let newRequest = {
          action: `register`,
          date: this.selectedDate,
          hours: this.selectedHours,
        }
        self.pushDate(newRequest)
        self.requests.push(newRequest)

        if (this.showProgress === false) {
          self.showProgress = true
          this.eventBusEmit('show-progress', true)
          setTimeout(async () => {
            await self.consumeRequest()
          }, 10);
        }

        this.$nextTick(() => { this.drawHolyday() })
      }

      if (this.selectedHours != 0) {
        this.showAlertDanger = true
        this.alertMessage = [ `${this.selectedDate}に上限時間を設定します。`, `(アルバイトさんは上限時間を超えたシフトの登録が出来なくなります。)` ]
        this.onClickDangerOK = processOK
      } else {
        processOK()
      }
    },
    async consumeRequest () {
      let aRequest = this.requests.shift()
      if (aRequest != undefined) {
        // request api
        const params = {
          headers: (await this.getAuthHeader()),
          body: {
            yyyymmdd: aRequest.date,
            hours: aRequest.hours,
          }
        }
        let requestPath = `register_limit_hours`
        if (aRequest.action === `register`) {
          this.pushDate(aRequest)
          aRequest.action = `register`
        }
        const self = this
        API.post((await this.apiNameForLoginUser()), `/${requestPath}`, params).then(response => { // eslint-disable-line no-unused-vars
          if (this.requests.length > 0) {
            setTimeout(async () => {
              await self.consumeRequest()
            }, 10);
          } else {
            this.showProgress = false
            this.eventBusEmit('show-progress', false)
          }

          this.$nextTick(() => { this.drawHolyday() })
        }).catch((error) => { // eslint-disable-line no-unused-vars
          console.log('error', error)
          let found = this.findDate(aRequest)
          if (found != undefined) {
            found.color = `red`
            found.error = true
          } else {
            aRequest.color = 'red'
            aRequest.error = true
            this.pushDate(aRequest);
          }
          this.eventBusEmit('show-error', { show: true, message: [ `保存に失敗しました ！!`, `赤色の箇所をやり直してください。` ] })

          if (this.requests.length > 0) {
            setTimeout(async () => {
              await self.consumeRequest()
            }, 10);
          } else {
            this.showProgress = false
            this.eventBusEmit('show-progress', false)
          }

          this.$nextTick(() => { this.drawHolyday() })
        })
      } else {
        this.showProgress = false
        this.eventBusEmit('show-progress', false)
      }
    },
    async onChange(info) {
      this.calendarInfo = JSON.parse(JSON.stringify(info))

      setTimeout(async () => {
        this.drawHolyday()
        this.showCalendar = true

        let year = this.calendarInfo.start.year
        let month = this.calendarInfo.start.month
        let momented = moment(`${year}/${month}/1`)
        this.fetchData(momented.format('yyyy-MM'), this.onFetchDataSucceeded, undefined, true)
        // prev month
        this.fetchData(momented.add(-1, 'M').format('yyyy-MM'), undefined, undefined, false)
        // next month
        this.fetchData(momented.add(+2, 'M').format('yyyy-MM'), undefined, undefined, false)
      }, 0);
    },
    getEventColor(event) {
      return event.color
    },
  },
  watch: {
    selectedDate: function (date, old) {
      date = moment(date).format('D')
      old = moment(old).format('D')
      $(".v-calendar-weekly__day").each((index, element) => { // eslint-disable-line no-unused-vars
        let child = $($(element).find('.v-calendar-weekly__day-label'))
        let dateButton = $(child.find('.v-btn__content'))
        if (date == dateButton.html()) {
          child.addClass('selected')
        }
        else
        if (old == dateButton.html()) {
          child.removeClass('selected')
        }
      })
    },
    showForm: function () {
      const self = this
      if (this.showForm) {
        this.drawHolyday()
        Vue.nextTick(function () {
          self.drawHolyday()
        })
      }
    },
  },
}
</script>
<style lang="scss">
.v-calendar-weekly__day.sunday {
  background-color: #E91E6322;
}
.v-calendar-weekly__day.saturday {
  background-color: #4169e122;
}
.v-calendar-weekly__day-label.regular-holiday {
  background-color: rgba(100, 100, 100, .4);
  height: 6.25em;
  @media screen and (min-width: 600px) { /* `mq()` */
    height: 6.25em;
  }
}
.regular-holiday-label {
  color: rgba(255, 0, 0, .6);
  font-weight: 2rem;
  font-size: 0.75em;
  @media screen and (min-width: 600px) { /* `mq()` */
    font-size: 1.0em;
  }
}
.v-calendar-weekly__day-label.limit-hours {
  height: 3em;
  @media screen and (min-width: 600px) { /* `mq()` */
    height: 3.5em;
  }
}
.v-calendar-weekly__day-label.limit-hours.fail {
  background-color: rgba(255, 0, 0, .6);
}
.limit-hours-label {
  color: rgba(206, 147, 216, 1.0);
  font-size: 0.75em;
  @media screen and (min-width: 600px) { /* `mq()` */
    font-size: 1.0em;
  }
}

.v-calendar-weekly__day-label.day-of-week-limit-hours {
  height: 6em;
  @media screen and (min-width: 600px) { /* `mq()` */
    height: 6.5em;
  }
}
.day-of-week-limit-hours-label {
  color: rgba(0, 100, 255, .6);
  font-size: 0.75em;
  @media screen and (min-width: 600px) { /* `mq()` */
    font-size: 1.0em;
  }
}

.v-calendar-weekly__day-label {
  border: solid transparent;
}
.v-calendar-weekly__day-label.selected {
  border: solid 6px #2196F322;
}
.fixed-top {
  position: fixed;
  top: 0px;
  z-index: 10;
}
.text-transparent {
  color: transparent
}
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