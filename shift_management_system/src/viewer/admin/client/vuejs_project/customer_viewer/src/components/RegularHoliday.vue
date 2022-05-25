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

    <v-sheet tile width="100vw" height="6vh" color="orange lighten-3" class="d-flex align-center fixed-top">
      <v-btn icon @click="onClickClose" class="no-print">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-btn outlined small class="text-h6">
        定休日設定
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
        color="orange"
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


    <v-speed-dial
      direction="top"
      transition="slide-y-transition"
      class="bottom-btn no-print"
    >
      <template v-slot:activator>
        <v-btn
          fab
          color="orange"
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
  name: 'RegularHoliday',
  props: [ 'showRegularHoliday', 'debug' ],
  data: () => ({
    now: undefined,
    today: moment().format('yyyy-MM-DD'),
    showCalendar: false,
    showProgress: false,
    events: [],
    regularHolidays: [],
    alertMessage: [],
    calendarInfo: {},
    showOverlayLoading: false,
    overlayMessage: ``,
    showSearch: false,
    requests: [],

    showAlertInfo: false,
    showAlertDanger: false,

    onClickInfoOK: undefined,
    onClickDangerOK: undefined,

    searchYYYYMM: moment().format('yyyy-MM'),
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
    this.eventBusOn('reload-regular-holiday', data => {
      if (data.today != undefined) {
        this.today = data.today
      }
      this.regularHolidays = []
      this.onChange(this.calendarInfo)
    })
    this.eventBusOn('change-month', yyyymm => { // eslint-disable-line no-unused-vars
      this.today = moment(`${yyyymm.replaceAll('-', '/')}/01`).format('yyyy-MM-DD')
    })
    this.eventBusOn('close-regular-holiday', userInfo => { // eslint-disable-line no-unused-vars
    })
  },
  computed: {
    title () {
      return moment(this.today).format('YY年M月');
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
      let year = this.calendarInfo.start.year
      let month = this.calendarInfo.start.month
      let momented = moment(`${year}/${month}/1`)
      let yyyym = { yyyy: momented.format('yyyy'), m: momented.format('M') }
      let yyyymPrev = { yyyy: momented.add(-1, 'M').format('yyyy'), m: momented.format('M') }
      let yyyymNext = { yyyy: momented.add(+2, 'M').format('yyyy'), m: momented.format('M') }
      let outsideSlashAppeared = false
      $(".v-calendar-weekly__day").each((index, element) => { // eslint-disable-line no-unused-vars
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

        child.removeClass('regular-holiday')
        child.removeClass('fail')
        $(child.find('#xxxx')).remove()
        console.log(`isRegularHoliday=${this.isRegularHoliday(yyyymmdd)} / ${yyyymmdd}`);
        if (this.isRegularHoliday(yyyymmdd)) {
          child.addClass('regular-holiday')
          var $ele = $('<div />', { id: 'xxxx', class: 'regular-holiday-label' }).append('定休日');
          child.prepend($ele)
          if (this.isRegularHolidayError(yyyymmdd)) {
            child.addClass('fail')
          }
        }
      })
    },
    onClickClose () {
      this.eventBusEmit('close-regular-holiday')
    },
    onClickSearch () {
      this.eventBusEmit('click-search')
    },
    onClickRefresh () {
      this.eventBusEmit('reload-regular-holiday', {})
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
      for (let date of this.regularHolidays) {
        if (date.yyyymmdd == request.date) {
          // 既存のものは消す
          this.regularHolidays.splice(this.regularHolidays.indexOf(date), 1)
          break
        }
      }
      this.regularHolidays.push({ yyyymmdd: request.date, error: request.error })
    },
    pullDate (request) {
      for (let date of this.regularHolidays) {
        if (date.yyyymmdd == request.date) {
          // 既存のものは消す
          this.regularHolidays.splice(this.regularHolidays.indexOf(date), 1)
          break
        }
      }
    },
    findDate (request) {
      for (let date of this.regularHolidays) {
        if (date.yyyymmdd == request.date) {
          return date
        }
      }
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
    isSaturday (yyyymmdd) {
      return moment(yyyymmdd.replaceAll('-', '/')).format('d') == 6;
    },
    isSunday (yyyymmdd) {
      return moment(yyyymmdd.replaceAll('-', '/')).format('d') == 0;
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
    showEvent({ event }) { // eslint-disable-line no-unused-vars
      // alert(`clicked ${event.name}`);
    },
    clickDay({ date }) { // eslint-disable-line no-unused-vars
      if (this.isRegularHoliday(date)) {
        this.unregister(date)
      } else {
        this.register(date)
      }
    },
    async fetchData (yyyymm, onSucceeded, onFailed, showLoading) {
      if (showLoading) this.eventBusEmit('show-overlay-loading', { show: true, message: `${yyyymm}...` })
      API.get((await this.apiNameForLoginUser()), `/fetch_regular_holiday_data/${yyyymm}`, { headers: (await this.getAuthHeader()) }).then(response => { // eslint-disable-line no-unused-vars
        if (showLoading) this.eventBusEmit('show-overlay-loading', { show: false, delay: 1000 })
        this.eventBusEmit('show-debug', { show: true, message: [ `fetchData: ${yyyymm} / uniqueId: ${this.uniqueId}` ] })
        response.data.forEach(yyyymmdd => {
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
            response.data.forEach(yyyymmdd => {
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
    register (date) {
      this.showAlertDanger = true
      this.alertMessage = [ `${date}を定休日に設定します。`, `(アルバイトさんはこの日のシフトを登録出来なくなります。)` ]
      const self = this
      this.onClickDangerOK = () => {

        self.showAlertDanger = false
        self.onClickDangerOK = undefined

        let newRequest = {
          action: `register`,
          date: date
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
    },
    unregister (date) {
      this.showAlertInfo = true
      this.alertMessage = [ `${date}を普通日に戻します。`, `(アルバイトさんはこの日のシフトを登録出来るようになります。)` ]
      const self = this
      this.onClickInfoOK = () => {
        self.showAlertInfo = false
        self.onClickInfoOK = undefined

        let newRequest = {
          action: `unregister`,
          date: date
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
    },
    async consumeRequest () {
      let aRequest = this.requests.shift()
      if (aRequest != undefined) {
        // request api
        const params = {
          headers: (await this.getAuthHeader()),
          body: {
            yyyymmdd: aRequest.date
          }
        }
        let requestPath = aRequest.action === `register` ? `register_regular_holiday` : ( aRequest.action === `unregister` ? `unregister_regular_holiday` : `xxxx` )
        if (aRequest.action === `register`) {
          this.pushDate(aRequest)
          aRequest.action = `register`
        }
        else
        if (aRequest.action === `unregister`) {
          this.pullDate(aRequest)
          aRequest.action = `unregister`
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
.v-calendar-weekly__day-label.regular-holiday.fail {
  background-color: rgba(255, 0, 0, .6);
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