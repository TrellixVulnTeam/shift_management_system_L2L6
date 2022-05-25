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
          v-for="n in Math.max(fixedRowNumber, Object.keys(kintai).length)"
          :key="n"
          :set="index = n-1"
          no-gutters
        >
          <span v-show="false" :set="key = 'kintai'"></span>
          <span v-show="false" :set="obj = $data[key]"></span>
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
                  :id="`text-${n-1}`"
                  class="centered-input"
                  type="number"
                  :value="unformatForPrice(value)"
                  outlined
                  hide-details
                  readonly
                >
                  <template v-slot:append-outer>
                    <v-btn
                      class="no-print"
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key)"
                    >
                      <v-icon
                        class="no-print"
                        color="grey"
                        :id="`icon-${n-1}`"
                      >
                        mdi-pencil
                      </v-icon>
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
          v-for="n in Math.max(fixedRowNumber, Object.keys(sikyuu).length)"
          :key="n"
          :set="index = n-1"
          no-gutters
        >
          <span v-show="false" :set="key = 'sikyuu'"></span>
          <span v-show="false" :set="obj = $data[key]"></span>
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
                  :id="`text-${n-1}`"
                  class="centered-input"
                  type="number"
                  :value="unformatForPrice(value)"
                  outlined
                  hide-details
                  readonly
                >
                  <template v-slot:append-outer>
                    <v-btn
                      class=""
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key)"
                    >
                      <v-icon
                        color="grey"
                        :id="`icon-${n-1}`"
                      >
                        mdi-pencil
                      </v-icon>
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
          <span v-show="false" :set="key = 'koujo'"></span>
          <span v-show="false" :set="obj = $data[key]"></span>
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
                  :id="`text-${n-1}`"
                  class="centered-input"
                  type="number"
                  :value="unformatForPrice(value)"
                  outlined
                  hide-details
                  readonly
                >
                  <template v-slot:append-outer>
                    <v-btn
                      class=""
                      x-small
                      elevation="0"
                      color="transparent"
                      @click="onClickEditMeisai($event, key)"
                    >
                      <v-icon
                        color="grey"
                        :id="`icon-${n-1}`"
                      >
                        mdi-pencil
                      </v-icon>
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
              cols="1"
            >
              <v-btn
                v-if="_editable"
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
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>
<script>
import Amplify, { API } from 'aws-amplify' // eslint-disable-line no-unused-vars
import moment from 'moment'; // eslint-disable-line no-unused-vars
import $ from 'jquery' // eslint-disable-line no-unused-vars
const awsExports = require('@/aws-exports').default
Amplify.configure(awsExports)
const priceFormatter = new Intl.NumberFormat('ja-JP');
export default {
  props: [ 'userInfo', 'debug' ],
  data: () => ({
    whiteSpace: `　 `, // eslint-disable-line no-irregular-whitespace
    fixedRowNumber: 10,
    kintai: {},
    sikyuu: {},
    koujo: {},
    calendarInfo: undefined,
    events: undefined,
    memo: ``,
    showMemo: true,
    _editable: false,
  }),
  created () {
    this.init()
    this.eventBusOn('reload-shift', data => { // eslint-disable-line no-unused-vars
      this.memo = ``
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
    },
    onClickEditMeisai (event, key) { // eslint-disable-line no-unused-vars
      let splited = event.target.id.split('-')
      let index = Number(splited[splited.length - 1])
      // let obj = this.$data[key][Object.keys(this.$data[key])[index]]
      let textObj = $('#' + `text-${index}`)
      textObj.attr('readonly', false)
      textObj.focus()
      const self = this
      textObj.focusout(() => {
        if (textObj.prop('readonly') === false) {
          textObj.attr('readonly', true)
          self.updateMeisaiValue(key, Object.keys(this.$data[key])[index], textObj.val())
        }
      })
    },
    onClickEditMemo (event) { // eslint-disable-line no-unused-vars
      let textObj = $("#memo")
      textObj.attr('readonly', false)
      textObj.focus()
      const self = this
      textObj.focusout(() => {
        if (textObj.prop('readonly') === false) {
          textObj.attr('readonly', true)
          self.updateMeisaiMemo(self.memo)
        }
      })
    },
    unformatForPrice (price) {
      return price != undefined ? Number(price.replaceAll(',', '')) : 0
    },
    async updateMeisaiValue (key, attribute, value) {
      this.eventBusEmit('show-progress', true)
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userid: this.userInfo.userId,
          yyyymm: this.yyyymm,
          key: key,
          attribute: attribute,
          value: value,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/update_meisai_value`, params).then(response => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
        this.eventBusEmit('data-changed', {
          calendarInfo: this.calendarInfo,
          events: this.events,
          meisai: response.meisai,
          memo: this.memo,
        })
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
        this.eventBusEmit('show-error', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    async updateMeisaiMemo (memo) {
      this.eventBusEmit('show-progress', true)
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userid: this.userInfo.userId,
          yyyymm: this.yyyymm,
          memo: memo,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/update_meisai_memo`, params).then(response => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.eventBusEmit('show-progress', false)
        this.eventBusEmit('show-error', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
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