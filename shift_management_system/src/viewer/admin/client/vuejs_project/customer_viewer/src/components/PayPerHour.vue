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
    <v-sheet tile width="100vw" height="6vh" color="lime darken-3" class="d-flex align-center fixed-top">
      <v-btn icon @click="onClickClose" class="no-print">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-card-text class="fw-bold">時給設定</v-card-text>
    </v-sheet>

    <div></div>
    <v-form class="mt-10">
      <v-container>

        <v-row class="pa-3">
          <v-col
            cols="12"
            sm="12"
            md="12"
          >
            <v-text-field
              :id="`common-jikyuu`"
              label="共通基本時給"
              :placeholder="String(commonJikyuu)"
              v-model="commonJikyuu"
              type="number"
              @input="flagHolder[`common-jikyuu`]['modified'] = true; flagHolder[`common-jikyuu`]['showUpdateCompletedMessage'] = false;"
              outlined
              hide-details
              readonly
            >
              <template v-slot:append-outer>
                <v-btn
                  v-if="flagHolder[`common-jikyuu`]['modified'] === false && flagHolder[`common-jikyuu`]['showUpdateCompletedMessage'] === false"
                  class="no-print"
                  x-small
                  elevation="0"
                  color="transparent"
                  @click="onClickEditJikyuu($event, 'common')"
                >
                  <v-icon
                    class="no-print"
                    color="grey"
                    :id="`icon-0`"
                  >
                    mdi-pencil
                  </v-icon>
                </v-btn>
                <v-btn
                  v-else-if="flagHolder[`common-jikyuu`]['showUpdateCompletedMessage']"
                  class="no-print"
                  x-small
                  elevation="0"
                  color="transparent"
                  @click="onClickEditJikyuu($event, 'common')"
                >
                  <v-icon
                    class="no-print"
                    color="green"
                    left
                    :id="`icon-0`"
                  >
                    mdi-pencil
                  </v-icon>
                  <v-sheet
                    v-show="!isMobile"
                    class="ml-1 white--text text--darken-2 pa-1"
                    color="#90ee90FF"
                    rounded
                    shaped
                    evaluation="50"
                    >
                    保存しました
                  </v-sheet>
                </v-btn>
                <v-btn
                  v-else
                  class="no-print"
                  x-small
                  elevation="0"
                  color="transparent"
                  @click="updateJikyuu($event, 'common', `common-jikyuu`)"
                >
                  <v-icon
                    class="no-print"
                    color="red"
                    left
                    :id="`icon-0`"
                  >
                    mdi-content-save-alert
                  </v-icon>
                  <v-sheet
                    v-show="!isMobile"
                    class="ml-1 white--text text--darken-2 pa-1"
                    color="#ff000066"
                    rounded
                    shaped
                    evaluation="50"
                    >
                    クリックして保存
                  </v-sheet>
                </v-btn>
              </template>
            </v-text-field>
          </v-col>
        </v-row>

        <v-divider></v-divider>

        <div class="mt-4 pa-8">
          <v-row
            v-for="(data, index) in jikyuuData"
            :key="index"
          >
            <v-col
              cols="12"
              sm="12"
              md="12"
            >
              <v-text-field
                :id="`${data.userid}-jikyuu`"
                :label="`${data.username}さん時給`"
                :placeholder="String(data.jikyuu)"
                v-model="data.jikyuu"
                type="number"
                @input="flagHolder[`${data.userid}-jikyuu`]['modified'] = true; flagHolder[`${data.userid}-jikyuu`]['showUpdateCompletedMessage'] = false;"
                outlined
                hide-details
                readonly
              >
                <template v-slot:append-outer>
                  <v-btn
                    v-if="flagHolder[`${data.userid}-jikyuu`]['modified'] === false && flagHolder[`${data.userid}-jikyuu`]['showUpdateCompletedMessage'] === false"
                    class="no-print"
                    x-small
                    elevation="0"
                    color="transparent"
                    @click="onClickEditJikyuu($event, data.userid)"
                  >
                    <v-icon
                      class="no-print"
                      color="grey"
                      :id="`icon-0`"
                    >
                      mdi-pencil
                    </v-icon>
                  </v-btn>
                  <v-btn
                    v-else-if="flagHolder[`${data.userid}-jikyuu`]['showUpdateCompletedMessage']"
                    class="no-print"
                    x-small
                    elevation="0"
                    color="transparent"
                    @click="onClickEditJikyuu($event, data.userid)"
                  >
                    <v-icon
                      class="no-print"
                      color="green"
                      left
                      :id="`icon-0`"
                    >
                      mdi-pencil
                    </v-icon>
                    <v-sheet
                      v-show="!isMobile"
                      class="ml-1 white--text text--darken-2 pa-1"
                      color="#90ee90FF"
                      rounded
                      shaped
                      evaluation="50"
                      >
                      保存しました
                    </v-sheet>
                  </v-btn>
                  <v-btn
                    v-else
                    class="no-print"
                    x-small
                    elevation="0"
                    color="transparent"
                    @click="updateJikyuu($event, data.userid, `${data.userid}-jikyuu`)"
                  >
                    <v-icon
                      class="no-print"
                      color="red"
                      left
                      :id="`icon-0`"
                    >
                      mdi-content-save-alert
                    </v-icon>
                    <v-sheet
                      v-show="!isMobile"
                      class="ml-1 white--text text--darken-2 pa-1"
                      color="#ff000066"
                      rounded
                      shaped
                      evaluation="50"
                      >
                      クリックして保存
                    </v-sheet>
                  </v-btn>
                </template>
              </v-text-field>
            </v-col>
          </v-row>
        </div>

        <div>
          共通基本時給に合わせたい場合は、時給0円に更新してください。
        </div>
      </v-container>
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
          color="lime darken-3"
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
  name: 'PayPerHour',
  props: [ 'showPayPerHours', 'debug' ],
  data: () => ({
    isMobile: false,

    showProgress: false,
    showOverlayLoading: false,
    overlayMessage: ``,

    jikyuuData: [],
    commonJikyuu: 0,
    flagHolder: {},
  }),
  created () {
    this.init()
    this.eventBusOn('show-progress', show => { // eslint-disable-line no-unused-vars
      this.showProgress = show
    })
    this.eventBusOn('show-overlay-loading', obj => { // eslint-disable-line no-unused-vars
      setTimeout(() => {
        this.showOverlayLoading = obj.show
        this.overlayMessage = obj.message != undefined ? obj.message : ``
      }, obj.delay != undefined ? obj.delay : 0);
    })
    this.eventBusOn('reload-pay-per-hour', () => {
      this.fetchData(this.onFetchDataSucceeded, this.onFetchDataFailed, true)
      this.init()
      this.initFlagHolder()
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
    onResize () {
      this.isMobile = window.innerWidth < 600
    },
    init () {
      this.common = {
        jikyu: 0,
      }
      this.initFlagHolder()
    },
    initFlagHolder () {
      let tmp = [ 'common' ]
      for (let data of this.jikyuuData)  {
        tmp.push(data.userid)
      }
      console.log(tmp);
      const self = this
      tmp.forEach((koumoku1, index1) => { // eslint-disable-line no-unused-vars
        if (self.flagHolder[`${koumoku1}-jikyuu`] === undefined)
          self.flagHolder[`${koumoku1}-jikyuu`] = {}
        self.flagHolder[`${koumoku1}-jikyuu`][`modified`] = false
        self.flagHolder[`${koumoku1}-jikyuu`][`showUpdateCompletedMessage`] = false
      })
      console.log(self.flagHolder);
    },
    onClickClose () {
      this.eventBusEmit('close-pay-per-hour')
    },
    onClickRefresh () {
      this.eventBusEmit('reload-pay-per-hour', {})
    },
    onClickEditJikyuu (event, key) { // eslint-disable-line no-unused-vars
      let splited = event.target.id.split('-')
      console.log(splited);
      let elementId = `${key}-jikyuu`
      this.flagHolder[elementId]['modified'] = this.flagHolder[elementId][`showUpdateCompletedMessage`] = false
      let textObj = $(`#${elementId.replace('.', '\\.')}`)
      textObj.attr('readonly', false)
      textObj.focus()
      console.log(`onClickEditJikyuu: key: ${key} / elementId: ${elementId} / value: ${textObj.val()}`);
      textObj.focusout(() => {
        if (textObj.prop('readonly') === false) {
          // textObj.attr('readonly', true)
          // self.updateValue(key, Object.keys(this.$data[key])[index], textObj.val())
        }
      })
    },
    async updateJikyuu (event, key, elementId) { // eslint-disable-line no-unused-vars
      let textObj = $(`#${elementId.replace('.', '\\.')}`)
      let val = textObj.val()
      console.log(`updateJikyuu: key ${key} / elementId ${elementId} / val: ${val}`);
      this.eventBusEmit('show-progress', true)
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userid: key,
          value: val,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/update_pay_per_hour`, params).then(response => { // eslint-disable-line no-unused-vars
        this.flagHolder[elementId]['modified'] = false
        this.flagHolder[elementId]['showUpdateCompletedMessage'] = true
        this.eventBusEmit('show-progress', false)

        this.jikyuuData = []
        response.jikyuu.forEach(d => {
          this.jikyuuData.push({
            userid: d['Username'],
            username: d['UsernameJa'],
            jikyuu: d['jikyuu'],
          })
        })
        console.log(this.jikyuuData);
        this.initFlagHolder()
        this.commonJikyuu = Number(response.common_jikyuu)

        textObj.attr('readonly', true)
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
        this.eventBusEmit('show-error', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    async fetchData (onSucceeded, onFailed, showLoading) {
      if (showLoading) this.eventBusEmit('show-overlay-loading', { show: true, message: `ロード中...` })
      API.get((await this.apiNameForLoginUser()), `/fetch_pay_per_hour`, { headers: (await this.getAuthHeader()) }).then(response => { // eslint-disable-line no-unused-vars
        if (showLoading) this.eventBusEmit('show-overlay-loading', { show: false, delay: 1000 })
        console.log(response.jikyuu);

        this.jikyuuData = []
        response.jikyuu.forEach(d => {
          this.jikyuuData.push({
            userid: d['Username'],
            username: d['UsernameJa'],
            jikyuu: d['jikyuu'],
          })
        })
        console.log(this.jikyuuData);
        this.initFlagHolder()

        this.commonJikyuu = Number(response.common_jikyuu)

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