<template>
  <div
    class="calendar-dialog"
  >
    <v-sheet tile width="100vw" height="6vh" color="grey lighten-3" class="d-flex align-center fixed-top">
      <v-btn icon @click="onClickClose" class="no-print">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-btn outlined small class="text-h6">
        {{ userInfo.username }}&nbsp;さん
      </v-btn>
      <div class="show-on-print">&nbsp;&nbsp;</div>
      <v-btn icon small @click="$refs.calendar.prev()" class="no-print">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-btn icon small @click="$refs.calendar.next()" class="no-print">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
      <v-badge
        v-if="isLocked.value"
        bordered
        color="error"
        icon="mdi-lock"
        overlap
      >
        <v-toolbar-title>{{ title }}</v-toolbar-title>
      </v-badge>
      <v-toolbar-title v-else>{{ title }}</v-toolbar-title>
      <v-btn icon small @click="onClickSearch" class="no-print">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-sheet>
    <v-sheet tile min-height="6vh" color="grey lighten-3" class="text--transparent">
      &nbsp;&nbsp;
    </v-sheet>
    <v-sheet width="97vw" height="104vh" class="">
      <v-calendar
        v-show="showCalendar"
        ref="calendar"
        :now="now"
        :value="today"
        color="primary"
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
        <template v-slot:day="{ past, date, month }">
          <v-row
            class="fill-height"
            :set="workHours = calcWorkHours(date)"
          >
            <template>
              <v-sheet
                :title="date"
                :color="onDate(date, month, today, past)"
                width="100%"
                height="100%"
                tile
              >
                <v-chip
                  v-if="workHours > 0"
                  class="mt-3"
                  x-small
                  >
                  {{ workHours }}時間
                </v-chip>
              </v-sheet>
            </template>
          </v-row>
        </template>
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
                      :value="calendarInfo"
                      :expand-depth=99
                      copyable></json-viewer>
                  </v-col>
                  <v-col>
                    <json-viewer
                      :value="jsonData"
                      :expand-depth=99
                      copyable></json-viewer>
                  </v-col>
                  <v-col>
                    <json-viewer
                      :value="regularHolidays"
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
                    v-model="selectedStartTime"
                    :items="timeListStart"
                    label="開始時間*"
                  ></v-select>
                </v-col>
                <v-col
                  cols="12"
                  sm="6"
                >
                  <v-select
                    v-model="selectedEndTime"
                    :items="timeListEnd"
                    label="終了時間*"
                  ></v-select>
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col
                  cols="12"
                  sm="1"
                >
                  <v-icon>mdi-information</v-icon>
                </v-col>
                <v-col
                  cols="12"
                  sm="5"
                >
                  <p class="form-alert">{{ formAlertWorkableHours }}</p>
                </v-col>
                <v-spacer></v-spacer>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="red darken-1"
              text
              @click="unregister()"
            >
              削除
            </v-btn>
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
  </div>
</template>
<script>
import Vue from 'vue'
import Amplify, { API, Auth } from 'aws-amplify'
import $ from 'jquery' // eslint-disable-line no-unused-vars
const awsExports = require('@/aws-exports').default
Amplify.configure(awsExports)
import moment from 'moment';
import JsonViewer from 'vue-json-viewer'
Vue.use(JsonViewer)
const timeList = [
  `07:00`,
  `07:30`,
  `08:00`,
  `08:30`,
  `09:00`,
  `09:30`,
  `10:00`,
  `10:30`,
  `11:00`,
  `11:30`,
  `12:00`,
  `12:30`,
  `13:00`,
  `13:30`,
  `14:00`,
  `14:30`,
  `15:00`,
  `15:30`,
  `16:00`,
  `16:30`,
  `17:00`,
  `17:30`,
  `18:00`,
  `18:30`,
  `19:00`,
  `19:30`,
  `20:00`,
  `20:30`,
  `21:00`,
  `21:30`,
  `22:00`,
  `22:30`,
  `23:00`,
  `23:30`,
]
var id = 0
function generateId() { return id++ }
export default {
  props: [ 'showShift', 'commonEvents', 'userInfo', 'isLocked', 'debug' ],
  data: () => ({
    uniqueId: generateId(),
    show: false,
    requested: false,
    events: [],
    regularHolidays: [],
    workableHoursLeftData: {},
    limitHours: [],
    dayOfWeekLimitHoursData: [],
    jsonData: {},
    calendarInfo: {},
    now: undefined,
    today: moment().format('yyyy-MM-DD'),
    showCalendar: false,
    showForm: false,
    showProgress: false,
    selectedDate: undefined,
    selectedStartTime: undefined,
    selectedEndTime: undefined,
    timeListStart: JSON.parse(JSON.stringify(timeList)),
    timeListEnd: JSON.parse(JSON.stringify(timeList)),
    requests: [],
    dataHashes: {},
  }),
  async created () {
    setTimeout(() => {
      //this.drawHolyday()
      this.showCalendar = true
    }, 0)
  },
  beforeDestroy: function () {
    var hidden, visibilityState, visibilityChange; // eslint-disable-line no-unused-vars
    if (typeof document.hidden !== "undefined") {
      hidden = "hidden", visibilityChange = "visibilitychange", visibilityState = "visibilityState";
    } else if (typeof document.msHidden !== "undefined") {
      hidden = "msHidden", visibilityChange = "msvisibilitychange", visibilityState = "msVisibilityState";
    }
    document.removeEventListener(visibilityChange, this.checkAppWasUpdated)
  },
  mounted () {
    if (true) { // eslint-disable-line no-constant-condition
      var hidden, visibilityState, visibilityChange; // eslint-disable-line no-unused-vars

      if (typeof document.hidden !== "undefined") {
        hidden = "hidden", visibilityChange = "visibilitychange", visibilityState = "visibilityState";
      } else if (typeof document.msHidden !== "undefined") {
        hidden = "msHidden", visibilityChange = "msvisibilitychange", visibilityState = "msVisibilityState";
      }

      var document_hidden = document[hidden];

      const self = this
      document.addEventListener(visibilityChange, function() {
        if(document_hidden != document[hidden]) {
          if(document[hidden]) {
            // Document hidden
          } else {
            // Document shown
            self.checkAppWasUpdated()
          }

          document_hidden = document[hidden];
        }
      });
    }
    this.eventBusOn('swipe-detected', direction => { // eslint-disable-line no-unused-vars
      if (this.showShift.value === false) return
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
    })
    this.eventBusOn('change-month', yyyymm => { // eslint-disable-line no-unused-vars
      this.today = moment(`${yyyymm.replaceAll('-', '/')}/01`).format('yyyy-MM-DD')
    })
    this.eventBusOn('reload-shift', data => {
      if (data.today != undefined) {
        this.today = data.today
      }
      this.userInfo = data.userInfo
      this.events = []
      this.regularHolidays = []
      this.limitHours = []
      this.workableHoursLeftData = {}
      this.jsonData = {}
      this.onChange(this.calendarInfo)
    })
    this.eventBusOn('shift-locked', userInfo => { // eslint-disable-line no-unused-vars
      let year = this.calendarInfo.start.year
      let month = this.calendarInfo.start.month
      this.isLocked.value = moment(`${year}/${month}/1`).format('yyyy-MM') === userInfo.yyyymm && this.userInfo.userId === userInfo.userId
    })
    this.eventBusOn('shift-unlocked', userInfo => { // eslint-disable-line no-unused-vars
      let year = this.calendarInfo.start.year
      let month = this.calendarInfo.start.month
      this.isLocked.value = !(moment(`${year}/${month}/1`).format('yyyy-MM') === userInfo.yyyymm && this.userInfo.userId === userInfo.userId)
    })
    this.eventBusOn('close-shift', userInfo => { // eslint-disable-line no-unused-vars
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
    selectedMonth () {
      let year = this.calendarInfo.start.year
      let month = this.calendarInfo.start.month
      let momented = moment(`${year}/${month}/1`)
      return momented.format('yyyy-MM')
    },
    formAlertWorkableHours () {
      let yyyymmdd = this.selectedDate
      if (yyyymmdd) {
        if (this.isRegularHoliday(yyyymmdd)) {
          return `この日は定休日です。`
        } else {
          let workableHoursLeftData = this.getWorkableHoursLeft(yyyymmdd)
          if (workableHoursLeftData != 0 && workableHoursLeftData != 9999) {
            return `この日は残り${workableHoursLeftData}時間働けます。`
          } else if (workableHoursLeftData == 0) {
            return `この日は残り0時間働けます。`
          }
        }
      }
      return ``
    },
  },
  methods: {
    calcWorkHours (date) {
      for (let e of this.events) {
        let start = moment(e.start)
        if (start.format('yyyy-MM-DD') == date) {
          let end = moment(e.end)
          return end.diff(start, 'seconds') / 60 / 60
          // return Math.floor(end.diff(start, 'seconds') / 60 / 60)
        }
      }
      return 0
    },
    hasEvent (date) {
      for (let e of this.events) {
        if (moment(e.start).format('yyyy-MM-DD') == date) {
          return true
        }
      }
      return false
    },
    async reload () {
      let year = this.calendarInfo.start.year
      let month = this.calendarInfo.start.month
      let momented = moment(`${year}/${month}/1`)
      let yyyymm = momented.format('yyyy-MM')
      // this.eventBusEmit('show-overlay-loading', { show: true, message: `${yyyymm}...` })
      this.eventBusEmit('show-info-shift', { show: false })
      this.fetchData(yyyymm, this.onFetchDataSucceeded, undefined, true)
      this.fetchData(momented.add(-1, 'M').format('yyyy-MM'), undefined, undefined, false)
      this.fetchData(momented.add(+2, 'M').format('yyyy-MM'), undefined, undefined, false)
    },
    drawHolyday () {
      let year = this.calendarInfo.start.year
      let month = this.calendarInfo.start.month
      console.log(`drawHoliday start ${year}${month}`);
      let momented = moment(`${year}/${month}/1`)
      let yyyym = { yyyy: momented.format('yyyy'), m: momented.format('M') }
      let yyyymPrev = { yyyy: momented.add(-1, 'M').format('yyyy'), m: momented.format('M') }
      let yyyymNext = { yyyy: momented.add(+2, 'M').format('yyyy'), m: momented.format('M') }
      let outsideSlashAppeared = false
      let _yyyym = yyyymPrev
      let isThisMonthFirstDayComing = false
      let _index = 0
      $(".calendar-dialog .v-calendar-weekly__day").each((index, element) => { // eslint-disable-line no-unused-vars
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
        //console.log(`yyyymmdd: ${yyyymmdd}`);

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
        // console.log(`yyyymmdd: ${yyyymmdd} / date: ${date}`);
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

        // reset
        $(child.find('#yyyy')).remove()
        $(child.find('#zzzz')).remove()
        child.removeClass('day-of-week-limit-hours')
        child.removeClass('limit-hours')
        child.removeClass('fail')

        let isRegularHoliday = false
        child.removeClass('regular-holiday')
        child.removeClass('has-event')
        $(child.find('#xxxx')).remove()
        if (this.isRegularHoliday(yyyymmdd)) {
          isRegularHoliday= true
          child.addClass('regular-holiday')
          var $ele = $('<div />', { id: 'xxxx', class: 'regular-holiday-label' }).append('定休日');
          child.prepend($ele)
          if (this.hasEvent(yyyymmdd)) {
            child.addClass('has-event')
          }
        }

        child.removeClass('workable-hours-left')
        $(child.find('#yyyy')).remove()
        if (!isRegularHoliday) {
          let workableHoursLeftData = this.getWorkableHoursLeft(yyyymmdd)
          if (workableHoursLeftData != 0 && workableHoursLeftData != 9999) {
            child.addClass('workable-hours-left')
            let $ele = $('<div />', { id: 'yyyy', class: 'workable-hours-left-label' }).append(`残り<span class="hour">${workableHoursLeftData}</span>時間働けます`)
            child.prepend($ele)
          } else if (workableHoursLeftData == 0) {
            child.addClass('workable-hours-left')
            let $ele = $('<div />', { id: 'yyyy', class: 'workable-hours-left-label' }).append(`残り<span class="hour">0</span>時間働けます`)
            child.prepend($ele)
          }
        }

      })
      console.log(`drawHoliday end / index: ${_index}`);
    },
    isRegularHoliday (yyyymmdd) {
      for (let _date of this.regularHolidays) {
        if (yyyymmdd === _date.yyyymmdd) {
          return true
        }
      }
      return false
    },
    getWorkableHoursLeft (yyyymmdd) {
      let yyyymm = moment(yyyymmdd.replaceAll('-', '/')).format('yyyy-MM')
      let hours = this.workableHoursLeftData[yyyymm][yyyymmdd]
      if (yyyymmdd === '2021-11-29') {
        console.log(`XXXXXXXXXXXXX yyyymmdd: ${yyyymmdd} / hours: ${hours}`);
        console.log(this.workableHoursLeftData);
      }
      if (hours != undefined) {
        return hours
      }
      hours = this.getLimitHours(yyyymmdd)
      if (yyyymmdd === '2021-11-29') {
        console.log(`XXXXXXXXXXXXX yyyymmdd: ${yyyymmdd} / hours: ${hours}`);
      }
      if (hours === 0)
        hours = this.getDayOfWeekLimitHours(yyyymmdd)
      if (yyyymmdd === '2021-11-29') {
        console.log(`XXXXXXXXXXXXX yyyymmdd: ${yyyymmdd} / hours: ${hours}`);
      }
      return hours > 0 ? hours : 9999
    },
    getLimitHours (yyyymmdd) {
      for (let l of this.limitHours) {
        if (l.yyyymmdd.replaceAll('-', '') === yyyymmdd.replaceAll('-', '')) {
          return l.hours
        }
      }
      return 0
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
    /*
    drawHolyday () {
      $(".v-calendar-weekly__day").each((index, element) => { // eslint-disable-line no-unused-vars
        // console.log(`index: ${index} / element: ${element}`);
        let child = $($(element).find('.v-calendar-weekly__day-label'))
        // console.log(`  child: ${child}`);
        let dateButton = $(child.find('.v-btn__content'))
        // console.log(`    date: ${dateButton.html()}`);
        if (this.isSunday(dateButton.html())) {
          $(element).addClass('sunday')
        }
        else
        if (this.isSaturday(dateButton.html())) {
          $(element).addClass('saturday')
        }
        else
        {
          $(element).removeClass('saturday')
          $(element).removeClass('sunday')
        }
      })
    },
    */
    checkAppWasUpdated () {
      if (this.showShift.value === false) return
      const self = this
      setTimeout(async () => {
        if (self.requested) return
        self.requested = true

        let year = self.calendarInfo.start.year
        let month = self.calendarInfo.start.month
        let momented = moment(`${year}/${month}/1`)
        let yyyymm = momented.format('yyyy-MM')
        let yyyymmPrev = momented.add(-1, 'M').format('yyyy-MM')
        let yyyymmNext = momented.add(+2, 'M').format('yyyy-MM')
        let apiname = await self.apiNameForLoginUser()
        let param = { headers: (await self.getAuthHeader()) }
        let hash1 = (await API.get(apiname, `/check_data_updated/${self.userInfo.userId}/${yyyymm}`, param)).hash
        let hash2 = (await API.get(apiname, `/check_data_updated/${self.userInfo.userId}/${yyyymmPrev}`, param)).hash
        let hash3 = (await API.get(apiname, `/check_data_updated/${self.userInfo.userId}/${yyyymmNext}`, param)).hash
        const debugString = `data_hash: ${hash1.substring(0, 8)} / ${self.dataHashes[yyyymm] != undefined ? self.dataHashes[yyyymm].substring(0, 8) : 'null'} / ${yyyymm} / uniqueId: ${self.uniqueId}`
        this.eventBusEmit('put-log', debugString)
        this.eventBusEmit('show-debug', { show: true, message: [ debugString ] })
        if (
          (self.dataHashes[yyyymm] != hash1) ||
          (self.dataHashes[yyyymmPrev] != hash2) ||
          (self.dataHashes[yyyymmNext] != hash3)
          /*
          (self.dataHashes[yyyymm] != undefined && self.dataHashes[yyyymm] != hash1) ||
          (self.dataHashes[yyyymmPrev] != undefined && self.dataHashes[yyyymmPrev] != hash2) ||
          (self.dataHashes[yyyymmNext] != undefined && self.dataHashes[yyyymmNext] != hash3)
          */
        ) {
          self.requested = false
          this.eventBusEmit('show-info-shift', {
            show: true,
            message: [ `データが更新されました !!`, `ページをリロードしてください。` ],
            data: {
              click: self.reload,
            }
          })
        } else {
          self.requested = false
        }
        /*
        self.dataHashes[yyyymm] = hash1
        self.dataHashes[yyyymmPrev] = hash2
        self.dataHashes[yyyymmNext] = hash3
        */
        console.log('data_hash', self.dataHashes)
      }, 500)
    },
    onClickClose () {
      this.eventBusEmit('close-shift')
    },
    onClickSearch () {
      this.eventBusEmit('click-search')
    },
    async fetchData (yyyymm, onSucceeded, onFailed, showLoading) {
      if (showLoading) this.eventBusEmit('show-overlay-loading', { show: true, message: `${yyyymm}...` })
      API.get((await this.apiNameForLoginUser()), `/fetch_data/${this.userInfo.userId}/${yyyymm}`, { headers: (await this.getAuthHeader()) }).then(response => { // eslint-disable-line no-unused-vars
        console.log(response.workable_hours_left_data)
        if (showLoading) this.eventBusEmit('show-overlay-loading', { show: false, delay: 1000 })
        this.eventBusEmit('show-debug', { show: true, message: [ `fetchData: ${yyyymm} / uniqueId: ${this.uniqueId}` ] })
        this.dataHashes[yyyymm] = response.hash
        response.data.forEach(data => {
          let name = data.name
          let date = moment(data.start).format(`YYYY-MM-DD`)
          let start = moment(data.start).toDate()
          let end = moment(data.end).toDate()

          for (let e of this.events) {
            if (moment(e.start).format('yyyy-MM-DD') == date) {
              // 既存のものは消す
              this.events.splice(this.events.indexOf(e), 1)
              break
            }
          }

          this.events.push({
            name: name,
            start: start,
            end: end,
            color: 'blue',
          })
        })

        // また、無くなっているものも消す
        let deleteIdxList = []
        for (let e of this.events) {
          let _yyyymm = moment(e.start).format(`YYYY-MM`)
          if (yyyymm === _yyyymm) {
            let exists = false
            response.data.forEach(data => {
              let date = moment(data.start).format(`YYYY-MM-DD`)
              if (moment(e.start).format('yyyy-MM-DD') == date) {
                exists = true
              }
            })

            if (!exists)
              deleteIdxList.push(this.events.indexOf(e))

          }
        }
        deleteIdxList.forEach(idx => {
          this.events[idx] = undefined
        })
        this.events = this.events.filter(Boolean)

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

        if (true) { // eslint-disable-line no-constant-condition
          // 特定日別上限時間
          response.limit_hours_data.forEach(data => {
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
        }

        if (true) { // eslint-disable-line no-constant-condition
          // 労働可能残時間
          this.workableHoursLeftData[yyyymm] = response.workable_hours_left_data
        }

        if (onSucceeded)
          onSucceeded(response)

        // this.$nextTick(() => { this.drawHolyday() })

      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-overlay-loading', { show: false, delay: 1000 })
        this.eventBusEmit('show-error-shift', { show: true, message: [ `検索に失敗しました！!`, `リロードしてしてください。` ] } )
        console.log('error', error)

        if (onFailed)
          onFailed(error)
      })
    },
    onFetchDataSucceeded (response) {
      this.isLocked.value = response.isLocked
      this.eventBusEmit('data-changed', {
        calendarInfo: this.calendarInfo,
        events: this.events,
        meisai: response.meisai,
        memo: response.memo.memo,
      })
      //this.$nextTick(() => { this.drawHolyday() })
      const self = this
      setTimeout(() => {
        self.drawHolyday()
        setTimeout(() => {
          self.drawHolyday()
        }, 1500)
      }, 500)
    },
    async getAuthHeader () {
      return {
        Authorization: (await Auth.currentAuthenticatedUser()).signInUserSession.idToken.jwtToken,
      }
    },
    pushEvent (request) {
      for (let e of this.events) {
        if (moment(e.start).format('yyyy-MM-DD') == request.date) {
          // 既存のものは消す
          this.events.splice(this.events.indexOf(e), 1)
          break
        }
      }
      this.events.push(request.event)
    },
    pullEvent (request) {
      for (let e of this.events) {
        if (moment(e.start).format('yyyy-MM-DD') == request.date) {
          // 既存のものは消す
          this.events.splice(this.events.indexOf(e), 1)
          break
        }
      }
    },
    findEvent (request) {
      for (let e of this.events) {
        // console.log(request.date, moment(e.start).format('yyyy-MM-DD'));
        if (moment(e.start).format('yyyy-MM-DD') == request.date) {
          return e
        }
      }
    },
    isCurrMonth (today, month) {
      return moment(today.replaceAll('-', '/')).format(`M`) == month;
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
    register () {
      this.showForm = false
      const self = this
      let splited = self.selectedDate.split('-')
      let splitedStartTime = self.selectedStartTime.split(':')
      let splitedEndTime = self.selectedEndTime.split(':')
      let newRequest = {
        action: `register`,
        date: self.selectedDate,
        startTime: self.selectedStartTime,
        endTime: self.selectedEndTime,
        event:
          {
            name: `${self.selectedStartTime}～${self.selectedEndTime}`,
            start: moment({ years: splited[0], months: Number(splited[1]) - 1, days: splited[2], hours: splitedStartTime[0], minutes: splitedStartTime[1] }).toDate(),
            end: moment({ years: splited[0], months: Number(splited[1]) - 1, days: splited[2], hours: splitedEndTime[0], minutes: splitedEndTime[1] }).toDate(),
            color: 'blue',
          },
      }
      self.requests.push(newRequest)
      if (this.showProgress === false) {
        self.showProgress = true
        this.eventBusEmit('show-progress', true)
        setTimeout(async () => {
          await self.consumeRequest()
        }, 10);
      }
    },
    unregister () {
      this.showForm = false
      const self = this
      let splited = self.selectedDate.split('-')
      let splitedStartTime = self.selectedStartTime.split(':')
      let splitedEndTime = self.selectedEndTime.split(':')
      let newRequest = {
        action: `unregister`,
        date: self.selectedDate,
        event:
          {
            name: `${self.selectedStartTime}～${self.selectedEndTime}`,
            start: moment({ years: splited[0], months: Number(splited[1]) - 1, days: splited[2], hours: splitedStartTime[0], minutes: splitedStartTime[1] }).toDate(),
            end: moment({ years: splited[0], months: Number(splited[1]) - 1, days: splited[2], hours: splitedEndTime[0], minutes: splitedEndTime[1] }).toDate(),
          },
      }
      self.requests.push(newRequest)
      if (this.showProgress === false) {
        self.showProgress = true
        this.eventBusEmit('show-progress', true)
        setTimeout(async () => {
          await self.consumeRequest()
        }, 10);
      }
    },
    async consumeRequest () {
      let aRequest = this.requests.shift()
      if (aRequest != undefined) {
        // request api
        let yyyymm = moment(aRequest.event.start).format('YYYY-MM')
        const params = {
          headers: (await this.getAuthHeader()),
          body: {
            name: aRequest.event != undefined ? aRequest.event.name : undefined,
            start: moment(aRequest.event.start).format('YYYY-MM-DD HH:mm'),
            end: moment(aRequest.event.end).format('YYYY-MM-DD HH:mm'),
            userId: this.userInfo.userId,
            hash: this.dataHashes[yyyymm],
          }
        }
        let requestPath = aRequest.action === `register` ? `register_date` : ( aRequest.action === `unregister` ? `unregister_date` : `xxxx` )
        if (aRequest.action === `register`) {
          this.pushEvent(aRequest)
          aRequest.event.action = `register`
        }
        else
        if (aRequest.action === `unregister`) {
          this.pullEvent(aRequest)
          aRequest.event.action = `unregister`
        }
        //console.log(aRequest.event);
        const self = this
        API.post((await this.apiNameForLoginUser()), `/${requestPath}`, params).then(response => { // eslint-disable-line no-unused-vars
          let nowHash = this.dataHashes[yyyymm]
          if (nowHash != response.prev_hash) {
            this.eventBusEmit('show-info-shift', {
              show: true,
              message: [ `データが更新されました !!`, `ページをリロードしてください。` ],
              data: {
                click: this.reload,
              }
            })
          } else {
            this.dataHashes[yyyymm] = response.hash
          }

          this.eventBusEmit('data-changed', {
            calendarInfo: this.calendarInfo,
            events: this.events,
            meisai: response.meisai,
            memo: response.memo,
          })

          if (true) { // eslint-disable-line no-constant-condition
            console.log(response.workable_hours_left_data);
            // 労働可能残時間
            this.workableHoursLeftData[yyyymm] = response.workable_hours_left_data
          }

          if (this.requests.length > 0) {
            setTimeout(async () => {
              await self.consumeRequest()
            }, 10);
          } else {
            this.showProgress = false
            this.eventBusEmit('show-progress', false)
          }

          this.$nextTick(() => { this.drawHolyday() })

          if (response.error) {
            throw "Error!!";
          }

        }).catch((error) => { // eslint-disable-line no-unused-vars
          console.log('error', error)
          let found = this.findEvent(aRequest)
          if (found != undefined) {
            found.color = `red`
            found.error = true
          } else {
            aRequest.event.color = 'red'
            aRequest.event.error = true
            this.pushEvent(aRequest);
          }
          this.eventBusEmit('show-error-shift', { show: true, message: [ `保存に失敗しました ！!`, `赤色の箇所をやり直してください。` ] })

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
    showEvent({ event }) { // eslint-disable-line no-unused-vars
      // alert(`clicked ${event.name}`);
    },
    clickDay({ date }) { // eslint-disable-line no-unused-vars

      var findEvent = (targetDate) => {
        for (let e of this.events) {
          if (moment(e.start).format('yyyy-MM-DD') == targetDate) {
            return e
          }
        }
      }

      this.showForm = true
      this.selectedDate = date
      let found = findEvent(this.selectedDate)
      if (found != undefined) {
        this.selectedStartTime = moment(found.start).format('HH:mm')
        this.selectedEndTime = moment(found.end).format('HH:mm')
      } else {
        this.selectedStartTime = `09:00`
        this.selectedEndTime = `17:30`
      }
    },
    async onChange(info) {
      this.calendarInfo = JSON.parse(JSON.stringify(info))
      this.isLocked.value = false

      setTimeout(async () => {
        //this.drawHolyday()
        this.showCalendar = true

        let year = this.calendarInfo.start.year
        let month = this.calendarInfo.start.month
        let momented = moment(`${year}/${month}/1`)
        this.fetchData(momented.format('yyyy-MM'), this.onFetchDataSucceeded, undefined, true)
        // prev month
        this.fetchData(momented.add(-1, 'M').format('yyyy-MM'), undefined, undefined, false)
        // next month
        this.fetchData(momented.add(+2, 'M').format('yyyy-MM'), undefined, undefined, false)

        API.get((await this.apiNameForLoginUser()), `/fetch_username/${this.userInfo.userId}`, { headers: (await this.getAuthHeader()) }).then(response => { // eslint-disable-line no-unused-vars
          this.userInfo.username = response.username
        }).catch((error) => { // eslint-disable-line no-unused-vars
          console.log('error', error)
        })

      }, 0);

    },
    getEventColor(event) {
      return event.color
    },
  },
  watch: {
    events: {
      handler: function (val) {
        this.commonEvents.length = 0
        for (let e of val) {
          let momented = moment(e.start)
          let yyyymm = momented.format('yyyy-MM')
          if (this.selectedMonth != yyyymm) continue

          this.commonEvents.push(e)
        }
        this.commonEvents.sort((a, b) => {
          return Number(moment(a.start).format('yyyyMMDD')) - Number(moment(b.start).format('yyyyMMDD'))
        })

        if (!this.debug.value) return
        this.jsonData = {}
        for (let e of val) {
          let momented = moment(e.start)
          let yyyymm = momented.format('yyyy-MM')
          this.jsonData[yyyymm] = this.jsonData[yyyymm] === undefined ? [] : this.jsonData[yyyymm]
          this.jsonData[yyyymm].push(momented.format('yyyy-MM-DD'))
        }
        Object.keys(this.jsonData).forEach(yyyymm => {
          this.jsonData[yyyymm].sort((a, b) => {
            return Number(a.replaceAll('-', '')) - Number(b.replaceAll('-', ''))
          })
        })
      },
      deep: true
    },
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
.v-calendar-weekly__day-label.regular-holiday.has-event {
  height: 6em;
  @media screen and (min-width: 600px) { /* `mq()` */
    height: 6.5em;
  }
}
.regular-holiday-label {
  color: rgba(255, 0, 0, .6);
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
.form-info {
  color: rgba(100, 100, 100, 1.0);
}
.form-alert {
  color: rgba(206, 147, 216, 1.0);
}
</style>
<style lang="scss">
@media print {
  .show-on-print {
    display: block;
  }
  .no-print {
    display: none;
  }
}
.v-calendar-weekly__day-label.workable-hours-left {
  height: 3em;
  @media screen and (min-width: 600px) { /* `mq()` */
    height: 3.5em;
  }

  .v-btn--fab.v-size--small {
    height: 20px;
    @media screen and (min-width: 600px) { /* `mq()` */
      height: 20px;
    }
  }
}
.workable-hours-left-label {
  $font-size: 0.5em;
  color: rgba(206, 147, 216, 1.0);
  font-size: $font-size;
  text-shadow: 0.07em 0.07em 0.02em grey;
  @media screen and (min-width: 600px) { /* `mq()` */
    //font-size: $font-size * 0.5;
  }
  .hour {
    font-size: $font-size * 4.0;
  }
}

.v-calendar-weekly__day-label.day-of-week-limit-hours {
  height: 3em;
  @media screen and (min-width: 600px) { /* `mq()` */
    height: 3.5em;
  }
}
.day-of-week-limit-hours-label {
  color: rgba(0, 100, 255, .6);
  font-size: 0.75em;
  @media screen and (min-width: 600px) { /* `mq()` */
    font-size: 1.0em;
  }
}
.v-calendar .v-event {
  margin-top: 24px;
  @media screen and (min-width: 600px) { /* `mq()` */
    margin-top: 0px;
  }
}
</style>