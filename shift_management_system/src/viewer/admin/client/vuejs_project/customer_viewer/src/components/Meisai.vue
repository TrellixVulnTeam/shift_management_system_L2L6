<template>
  <div>
    <v-sheet
      tile
      height="8vh"
      color="grey
      lighten-3"
      class="d-flex align-center"
      >
      <v-toolbar-title class="ml-3">給与明細</v-toolbar-title>
    </v-sheet>

    <v-container width="50vw" class="mb-4">
      <v-card class="mx-auto mt-0">
        <v-card-title>
          差引支給額
        </v-card-title>
        <v-card-text class="black--text font-weight-thin display-2">
          <v-container>
            <v-row>
              <v-spacer/>
              <v-spacer/>
              <v-spacer/>
              <v-spacer/>
              <v-spacer/>
              <v-spacer/>
              <v-spacer/>
              <v-spacer/>
              <v-spacer/>
              <v-col><span class="font-weight-bold">{{ sashihikiSikyuuGaku }}</span></v-col>
              <v-col>円</v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>

      {{ $data['editable'] }}

      <v-card class="mx-auto green mt-3">
        <v-row
          class="mb-0"
          no-gutters
        >
          <v-col>
            <v-card
              class="pa-2 green white--text"
              outlined
              tile
            >
              <v-card-text
                class="meisai-header white--text"
              >
                勤怠
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row
          v-for="n in Math.max(fixedRowNumber, Object.keys(koujo).length)"
          :key="n"
          :set="index = n-1"
          no-gutters
        >
          <span v-show="false" :set="key1 = 'kintai'"></span>
          <span v-show="false" :set="obj = $data[key1]"></span>
          <span v-show="false" :set="length = Object.keys(obj).length"></span>
          <span v-show="false" :set="formatter = length > index ? obj[Object.keys(obj)[index]]['formatter'] : undefined"></span>
          <span v-show="false" :set="editable = $data['_editable'] && length > index ? obj[Object.keys(obj)[index]]['editable'] : false"></span>
          <span v-show="false" :set='text = length > index ? obj[Object.keys(obj)[index]]["text"] : whiteSpace'></span>
          <span v-show="false" :set='value = length > index ? (formatter != undefined  ? formatter.format(obj[Object.keys(obj)[index]]["value"]) : obj[Object.keys(obj)[index]]["value"]) : whiteSpace'></span>
          <span v-show="false" :set="classs = length > index ? obj[Object.keys(obj)[index]]['class'] : ''"></span>
          <span v-show="false" :set="height = editable ? '40' : 'auto'"></span>
          <span v-show="false" :set="click = length > index ? obj[Object.keys(obj)[index]]['click'] : undefined"></span>
          <v-col
            color="green"
            >
            <v-card
              class="pa-1"
              outlined
              tile
              shaped
            >
              <v-card-text
                :class="classs"
                class="meisai-title black--text"
              >
                {{ text }}
              </v-card-text>
            </v-card>
          </v-col>
          <v-col
            color="green"
            >
            <v-card
              class="pa-1"
              :class="classs"
              outlined
              tile
              shaped
            >
              <v-card-text
                v-if="editable"
                class="ma-0 pa-0"
                >
                <v-text-field
                  :id="`${key1}-text-${n-1}`"
                  class="centered-input"
                  type="number"
                  :value="unformatForPrice(value)"
                  @input="flagHolder[`${key1}-text-${n-1}`]['modified'] = true; flagHolder[`${key1}-text-${n-1}`]['showUpdateCompletedMessage'] = false;"
                  outlined
                  hide-details
                  readonly
                >
                  <template v-slot:append-outer>
                    <v-btn
                      v-if="flagHolder[`${key1}-text-${n-1}`]['modified'] === false && flagHolder[`${key1}-text-${n-1}`]['showUpdateCompletedMessage'] === false"
                      class="no-print"
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key1)"
                    >
                      <v-icon
                        class="no-print"
                        color="grey"
                        :id="`icon-${n-1}`"
                      >
                        mdi-pencil
                      </v-icon>
                    </v-btn>
                    <v-btn
                      v-else-if="flagHolder[`${key1}-text-${n-1}`]['showUpdateCompletedMessage']"
                      class="no-print"
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key1)"
                    >
                      <v-icon
                        class="no-print"
                        color="green"
                        left
                        :id="`icon-${n-1}`"
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
                      @click="updateMeisaiValue($event, key1, `${key1}-text-${n-1}`)"
                    >
                      <v-icon
                        class="no-print"
                        color="red"
                        left
                        :id="`icon-${n-1}`"
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
              </v-card-text>
              <v-card-text
                v-else
                :class="classs"
                class="meisai-value black--text"
              >
                {{ value }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card>

      <v-card class="mx-auto green mt-3">
        <v-row
          class="mb-0"
          no-gutters
        >
          <v-col>
            <v-card
              class="pa-2 green white--text"
              outlined
              tile
            >
              <v-card-text
                class="meisai-header white--text"
              >
                支給
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row
          v-for="n in Math.max(fixedRowNumber, Object.keys(koujo).length)"
          :key="n"
          :set="index = n-1"
          no-gutters
        >
          <span v-show="false" :set="key2 = 'sikyuu'"></span>
          <span v-show="false" :set="obj = $data[key2]"></span>
          <span v-show="false" :set="length = Object.keys(obj).length"></span>
          <span v-show="false" :set="formatter = length > index ? obj[Object.keys(obj)[index]]['formatter'] : undefined"></span>
          <span v-show="false" :set="editable = $data['_editable'] && length > index ? obj[Object.keys(obj)[index]]['editable'] : false"></span>
          <span v-show="false" :set='text = length > index ? obj[Object.keys(obj)[index]]["text"] : whiteSpace'></span>
          <span v-show="false" :set='value = length > index ? (formatter != undefined  ? formatter.format(obj[Object.keys(obj)[index]]["value"]) : obj[Object.keys(obj)[index]]["value"]) : whiteSpace'></span>
          <span v-show="false" :set="classs = length > index ? obj[Object.keys(obj)[index]]['class'] : ''"></span>
          <span v-show="false" :set="height = editable ? '40' : 'auto'"></span>
          <span v-show="false" :set="click = length > index ? obj[Object.keys(obj)[index]]['click'] : undefined"></span>
          <v-col
            color="green"
            >
            <v-card
              class="pa-1"
              outlined
              tile
              shaped
            >
              <v-card-text
                :class="classs"
                class="meisai-title black--text"
              >
                {{ text }}
              </v-card-text>
            </v-card>
          </v-col>
          <v-col
            color="green"
            >
            <v-card
              class="pa-1"
              :class="classs"
              outlined
              tile
              shaped
            >
              <v-card-text
                v-if="editable"
                class="ma-0 pa-0"
                >
                <v-text-field
                  :id="`${key2}-text-${n-1}`"
                  class="centered-input"
                  type="number"
                  :value="unformatForPrice(value)"
                  @input="flagHolder[`${key2}-text-${n-1}`]['modified'] = true; flagHolder[`${key2}-text-${n-1}`]['showUpdateCompletedMessage'] = false;"
                  outlined
                  hide-details
                  readonly
                >
                  <template v-slot:append-outer>
                    <v-btn
                      v-if="flagHolder[`${key2}-text-${n-1}`]['modified'] === false && flagHolder[`${key2}-text-${n-1}`]['showUpdateCompletedMessage'] === false"
                      class="no-print"
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key2)"
                    >
                      <v-icon
                        class="no-print"
                        color="grey"
                        :id="`icon-${n-1}`"
                      >
                        mdi-pencil
                      </v-icon>
                    </v-btn>
                    <v-btn
                      v-else-if="flagHolder[`${key2}-text-${n-1}`]['showUpdateCompletedMessage']"
                      class="no-print"
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key2)"
                    >
                      <v-icon
                        class="no-print"
                        color="green"
                        left
                        :id="`icon-${n-1}`"
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
                      @click="updateMeisaiValue($event, key2, `${key2}-text-${n-1}`)"
                    >
                      <v-icon
                        class="no-print"
                        color="red"
                        left
                        :id="`icon-${n-1}`"
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
              </v-card-text>
              <v-card-text
                v-else
                :class="classs"
                class="meisai-value black--text"
              >
                {{ value }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card>


      <v-card class="mx-auto green mt-3">
        <v-row
          class="mb-0"
          no-gutters
        >
          <v-col>
            <v-card
              class="pa-2 green white--text"
              outlined
              tile
            >
              <v-card-text
                class="meisai-header white--text"
              >
                控除
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row
          v-for="n in Math.max(fixedRowNumber, Object.keys(koujo).length)"
          :key="n"
          :set="index = n-1"
          no-gutters
        >
          <span v-show="false" :set="key3 = 'koujo'"></span>
          <span v-show="false" :set="obj = $data[key3]"></span>
          <span v-show="false" :set="length = Object.keys(obj).length"></span>
          <span v-show="false" :set="formatter = length > index ? obj[Object.keys(obj)[index]]['formatter'] : undefined"></span>
          <span v-show="false" :set="editable = $data['_editable'] && length > index ? obj[Object.keys(obj)[index]]['editable'] : false"></span>
          <span v-show="false" :set='text = length > index ? obj[Object.keys(obj)[index]]["text"] : whiteSpace'></span>
          <span v-show="false" :set='value = length > index ? (formatter != undefined  ? formatter.format(obj[Object.keys(obj)[index]]["value"]) : obj[Object.keys(obj)[index]]["value"]) : whiteSpace'></span>
          <span v-show="false" :set="classs = length > index ? obj[Object.keys(obj)[index]]['class'] : ''"></span>
          <span v-show="false" :set="height = editable ? '40' : 'auto'"></span>
          <span v-show="false" :set="click = length > index ? obj[Object.keys(obj)[index]]['click'] : undefined"></span>
          <v-col
            color="green"
            >
            <v-card
              class="pa-1"
              outlined
              tile
              shaped
            >
              <v-card-text
                :class="classs"
                class="meisai-title black--text"
              >
                {{ text }}
              </v-card-text>
            </v-card>
          </v-col>
          <v-col
            color="green"
            >
            <v-card
              class="pa-1"
              :class="classs"
              outlined
              tile
              shaped
            >
              <v-card-text
                v-if="editable"
                class="ma-0 pa-0"
                >
                <v-text-field
                  :id="`${key3}-text-${n-1}`"
                  class="centered-input"
                  type="number"
                  :value="unformatForPrice(value)"
                  @input="flagHolder[`${key3}-text-${n-1}`]['modified'] = true; flagHolder[`${key3}-text-${n-1}`]['showUpdateCompletedMessage'] = false;"
                  outlined
                  hide-details
                  readonly
                >
                  <template v-slot:append-outer>
                    <v-btn
                      v-if="flagHolder[`${key3}-text-${n-1}`]['modified'] === false && flagHolder[`${key3}-text-${n-1}`]['showUpdateCompletedMessage'] === false"
                      class="no-print"
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key3)"
                    >
                      <v-icon
                        class="no-print"
                        color="grey"
                        :id="`icon-${n-1}`"
                      >
                        mdi-pencil
                      </v-icon>
                    </v-btn>
                    <v-btn
                      v-else-if="flagHolder[`${key3}-text-${n-1}`]['showUpdateCompletedMessage']"
                      class="no-print"
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key3)"
                    >
                      <v-icon
                        class="no-print"
                        color="green"
                        left
                        :id="`icon-${n-1}`"
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
                      @click="updateMeisaiValue($event, key3, `${key3}-text-${n-1}`)"
                    >
                      <v-icon
                        class="no-print"
                        color="red"
                        left
                        :id="`icon-${n-1}`"
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
              </v-card-text>
              <v-card-text
                v-else
                :class="classs"
                class="meisai-value black--text"
              >
                {{ value }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </v-container>

    <v-container v-if="!showMemo" class="mt-14">
    </v-container>

    <v-container v-if="showMemo" class="mt-0 mb-14">
      <v-card>
        <v-card-title>
          備考
        </v-card-title>
        <v-card-text>
          <v-row
            class="ma-0 pa-0"
            no-gutters
          >
            <v-col
            >
              <v-textarea
                id="memo"
                v-model="memo"
                @input="memoModified = true; showUpdateMemoCompletedMessage = false"
                outlined
                readonly
                hide-details
                value=""
              ></v-textarea>
            </v-col>
          </v-row>
          <v-row
            class="mt-1"
            no-gutters
          >
            <v-spacer></v-spacer>
            <v-col
              :cols="memoModified || showUpdateMemoCompletedMessage ? 2 : 1"
            >
              <v-btn
                v-if="memoModified === false && showUpdateMemoCompletedMessage === false"
                class="no-print"
                x-small
                elevation="0"
                color="transparent"
                @click="onClickEditMemo($event)"
              >
                <v-icon
                  class="no-print"
                  color="grey"
                >
                  mdi-pencil
                </v-icon>
              </v-btn>
              <v-btn
                v-else-if="showUpdateMemoCompletedMessage"
                class="no-print"
                x-small
                elevation="0"
                color="transparent"
                @click="onClickEditMemo($event)"
              >
                <v-icon
                  class="no-print"
                  color="green"
                  left
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
                @click="updateMeisaiMemo($event)"
              >
                <v-icon
                  class="no-print"
                  color="red"
                  left
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
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <div class="no-print mt-8">
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
                        :value="flagHolder"
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

    </v-container>
  </div>
</template>
<script>
import Vue from 'vue'
import Amplify, { API } from 'aws-amplify' // eslint-disable-line no-unused-vars
import moment from 'moment'; // eslint-disable-line no-unused-vars
import $ from 'jquery' // eslint-disable-line no-unused-vars
const awsExports = require('@/aws-exports').default
Amplify.configure(awsExports)
const priceFormatter = new Intl.NumberFormat('ja-JP');
import JsonViewer from 'vue-json-viewer'
Vue.use(JsonViewer)
export default {
  name: 'Meisai',
  props: [ 'userInfo', 'debug' ],
  data: () => ({
    isMobile: false,

    whiteSpace: `　　`, // eslint-disable-line no-irregular-whitespace
    fixedRowNumber: 10,
    kintai: {},
    sikyuu: {},
    koujo: {},
    calendarInfo: undefined,
    events: undefined,
    memo: ``,
    showMemo: true,
    _editable: true,
    memoModified: false,
    showUpdateMemoCompletedMessage: false,
    flagHolder: {},
  }),
  created () {
    this.init()
    this.eventBusOn('reload-shift', data => { // eslint-disable-line no-unused-vars
      this.memo = ``
      this.memoModified = false
      this.showUpdateMemoCompletedMessage = false
      this.init()
      this.initFlagHolder()
    })
    this.eventBusOn('data-changed', data => { // eslint-disable-line no-unused-vars
      let meisai = data.meisai
      this.calendarInfo = data.calendarInfo
      this.events = data.events
      this.memo = data.memo
      let tmp = ['kintai', 'sikyuu', 'koujo']
      tmp.forEach(koumoku1 => {
        Object.keys(this[koumoku1]).forEach(koumoku2 => {
          this[koumoku1][koumoku2].value = meisai[koumoku1] != undefined && meisai[koumoku1][koumoku2] != undefined ? meisai[koumoku1][koumoku2] : 0
        })
      })
    })
  },
  computed: {
    sashihikiSikyuuGaku () {
      return priceFormatter.format(this.sikyuu.souSikyuuGaku.value - this.koujo.koujoKei.value);
    },
    yyyymm () {
      let year = this.calendarInfo.start.year
      let month = this.calendarInfo.start.month
      return moment(`${year}/${month}/1`).format('yyyy-MM')
    },
  },
  methods: {
    init () {
      this.kintai = {
        roudouNisuu: { text: `労働日数`, value: 0, class: ``, formatter: undefined, editable: false, },
        souroudouJikan: { text: `総労働時間`, value: 0, class: ``, formatter: undefined, editable: false, },
      }
      this.sikyuu = {
        kihonKyuu: { text: `基本給`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        fusyuurouKoujo: { text: `不就労控除`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        souSikyuuGaku: { text: `総支給額`, value: 0, class: 'font-weight-bold', formatter: priceFormatter, editable: false, },
        kazeiTaisyouGaku: { text: `課税対象額`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
      }
      this.koujo = {
        kaigoHoken: { text: `介護保険`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        kenkouHoken: { text: `健康保険`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        kouseiNenkin: { text: `厚生年金`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        koyouHoken: { text: `雇用保険`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        syakaiHokenGoukei: { text: `社会保険合計`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        syotokuZei: { text: `所得税`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        jyuuminZei: { text: `住民税`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        seimeiHokenRyou: { text: `生命保険料`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        tsumitateKin: { text: `積立金`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        hensai: { text: `返済`, value: 0, class: ``, formatter: priceFormatter, editable: false, },
        cyouseigaku: { text: `調整額`, value: 0, class: ``, formatter: priceFormatter, editable: true, },
        koujoKei: { text: `控除計`, value: 0, class: `font-weight-bold`, formatter: priceFormatter, editable: false, },
      }
      this.initFlagHolder()
    },
    onResize () {
      this.isMobile = window.innerWidth < 600
    },
    initFlagHolder () {
      let tmp = ['kintai', 'sikyuu', 'koujo']
      const self = this
      tmp.forEach((koumoku1, index1) => { // eslint-disable-line no-unused-vars
        Object.keys(this[koumoku1]).forEach((koumoku2, index2) => { // eslint-disable-line no-unused-vars
          if (self.flagHolder[`${koumoku1}-text-${index2}`] === undefined)
            self.flagHolder[`${koumoku1}-text-${index2}`] = {}
          self.flagHolder[`${koumoku1}-text-${index2}`][`modified`] = false
          self.flagHolder[`${koumoku1}-text-${index2}`][`showUpdateCompletedMessage`] = false
        })
      })
    },
    onClickEditMeisai (event, key) { // eslint-disable-line no-unused-vars
      let splited = event.target.id.split('-')
      let index = Number(splited[splited.length - 1])
      let elementId = `${key}-text-${index}`
      // console.log(`onClickEditMeisai: key ${key} / elementId ${elementId}`);
      this.flagHolder[elementId]['modified'] = this.flagHolder[elementId][`showUpdateCompletedMessage`] = false
      let textObj = $('#' + `${elementId}`)
      textObj.attr('readonly', false)
      textObj.focus()
      textObj.focusout(() => {
        if (textObj.prop('readonly') === false) {
          // textObj.attr('readonly', true)
          // self.updateMeisaiValue(key, Object.keys(this.$data[key])[index], textObj.val())
        }
      })
    },
    onClickEditMemo (event) { // eslint-disable-line no-unused-vars
      this.showUpdateMemoCompletedMessage = this.memoModified = false
      let textObj = $("#memo")
      textObj.attr('readonly', false)
      textObj.focus()
      textObj.focusout(() => {
        if (textObj.prop('readonly') === false) {
          // textObj.attr('readonly', true)
        }
      })
    },
    unformatForPrice (price) {
      return price != undefined ? Number(price.replaceAll(',', '')) : 0
    },
    async updateMeisaiValue (event, key, elementId) { // eslint-disable-line no-unused-vars
      let textObj = $('#' + `${elementId}`)
      let splited = elementId.split('-')
      let index = Number(splited[splited.length - 1])
      let attr = Object.keys(this.$data[key])[index]
      let val = textObj.val()
      console.log(`updateMeisaiValue: key ${key} / attr ${attr} / val ${val}`);
      this.eventBusEmit('show-progress', true)
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userid: this.userInfo.userId,
          yyyymm: this.yyyymm,
          key: key,
          attribute: attr,
          value: val,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/update_meisai_value`, params).then(response => { // eslint-disable-line no-unused-vars
        this.flagHolder[elementId]['modified'] = false
        this.flagHolder[elementId]['showUpdateCompletedMessage'] = true
        this.eventBusEmit('show-progress', false)
        this.eventBusEmit('data-changed', {
          calendarInfo: this.calendarInfo,
          events: this.events,
          meisai: response.meisai,
          memo: this.memo,
        })
        textObj.attr('readonly', true)
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
        this.eventBusEmit('show-error', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    async updateMeisaiMemo () {
      this.eventBusEmit('show-progress', true)
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userid: this.userInfo.userId,
          yyyymm: this.yyyymm,
          memo: this.memo,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/update_meisai_memo`, params).then(response => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
        this.memoModified = false
        this.showUpdateMemoCompletedMessage = true
        let textObj = $("#memo")
        textObj.attr('readonly', true)
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
        this.eventBusEmit('show-error', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
  },
  beforeDestroy: function () {
    window.removeEventListener('resize', this.onResize, { passive: true })
  },
  mounted () {
    this.onResize()
    window.addEventListener('resize', this.onResize, { passive: true })
  },
  watch: {
  },
}
</script>
<style scoped>
.centered-input >>> input {
  text-align: center;
}
.meisai-header {
  font-size: 1.25rem;
}
.meisai-title {
  font-size: 1.15rem;
}
.meisai-value {
  font-size: 1.15rem;
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
</style>