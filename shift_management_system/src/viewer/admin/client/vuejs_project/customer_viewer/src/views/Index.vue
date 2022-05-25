<template>
  <v-app>
    <notifications group="notifications" position="top right" classes="notification-style"></notifications>
    <v-progress-linear
      indeterminate
      color="primary"
      v-show="showProgress"
      dense
      height="8"
      class="fixed-top"
    ></v-progress-linear>
    <v-container v-show="showUniShift.value === false && showShift.value === false && showRegularHoliday.value === false && showLimitHours.value === false && showDayOfWeekLimitHours.value === false && showPayPerHour.value === false">
      <v-card class="mt-4">
        <v-card-title :class='appColor + " white--text headline text-left"'>
          {{ appName }}
        </v-card-title>
      </v-card>
      <v-divider/>
      <div class="mt-6 mb-6">
        <v-expansion-panels
          focusable
          popout
          >
          <v-expansion-panel
            @click="onClickShiftPanel"
            >
            <v-expansion-panel-header>
              <v-container>
                <v-row>
                  <v-col><v-icon :color="shiftColor">mdi-calendar</v-icon><span class="ml-2">シフト確認</span></v-col>
                </v-row>
              </v-container>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-container class="mt-4">
                <v-row>
                  <v-col cols="10">
                    シフト確認や変更を行います。
                  </v-col>
                  <v-col cols="2">
                    <v-btn color="black" outlined small @click="listShift">
                      <v-icon color="grey" >mdi-refresh</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
              <v-container>
                <v-row
                  class="pa-0 mt-2"
                  v-if="showListShiftProgress"
                >
                  <v-col cols="2">
                    <v-progress-circular
                      indeterminate
                      color="indigo"
                    ></v-progress-circular>
                  </v-col>
                  <v-spacer></v-spacer>
                </v-row>
                <v-row
                  class="pa-1"
                  justify="space-between"
                >
                  <v-col cols="12">
                    <v-treeview
                      rounded
                      hoverable
                      activatable
                      transition
                      :items="shifts"
                    >
                      <template slot="label" slot-scope="{ item }">
                        <v-container>
                          <v-row
                            no-gutters
                            >
                            <v-col cols="2">
                              <v-icon :color="shiftColor">
                                mdi-calendar
                              </v-icon>
                            </v-col>
                            <v-col cols="10" class="text-wrap">
                              {{ item.name }}
                            </v-col>
                          </v-row>
                          <v-row
                            v-if="isMobile"
                            align="center"
                            no-gutters
                            >
                            <v-col
                              cols="2"
                              class=""
                              >
                              <v-btn
                                icon
                                color="blue"
                                @click.native="onClickShowShift(item)"
                              >
                                <v-icon>mdi-pencil</v-icon>
                              </v-btn>
                            </v-col>
                            <v-col
                              cols="2"
                              class=""
                              >
                              <v-btn
                                icon
                                color="grey"
                                @click.native="onClickShowShift(item)"
                              >
                                <v-icon>mdi-eye-outline</v-icon>
                              </v-btn>
                            </v-col>
                            <v-col
                              cols="8"
                              class=""
                              >
                              <v-sheet
                                class="ml-1 grey--text text--darken-2"
                                color="#ffffe0"
                                rounded
                                shaped
                                evaluation="50"
                                >
                                {{ getPreview(item) }}
                              </v-sheet>
                            </v-col>
                          </v-row>
                          <v-row
                            v-else
                            align="center"
                            no-gutters
                            >
                            <v-spacer/>
                            <v-col
                              cols="3"
                              class=""
                              >
                              <v-btn
                                icon
                                color="blue"
                                @click.native="onClickShowShift(item)"
                              >
                                <v-icon>mdi-pencil</v-icon>
                              </v-btn>
                            </v-col>
                            <v-col
                              cols="1"
                              class=""
                              >
                              <v-btn
                                icon
                                color="grey"
                                @click.native="onClickShowShift(item)"
                              >
                                <v-icon>mdi-eye-outline</v-icon>
                              </v-btn>
                            </v-col>
                            <v-col
                              cols="4"
                              class=""
                              >
                              <v-sheet
                                class="ml-1 grey--text text--darken-2"
                                color="#ffffe0"
                                rounded
                                shaped
                                evaluation="50"
                                >
                                {{ getPreview(item) }}
                              </v-sheet>
                            </v-col>
                          </v-row>
                        </v-container>
                      </template>
                    </v-treeview>
                  </v-col>
                </v-row>
              </v-container>
              <v-container class="mt-1">
                <v-row>
                  <v-col cols="2">
                    <v-btn fab dark small color="green" @click="registerShift1">
                      <v-icon>mdi-calendar-edit</v-icon>
                    </v-btn>
                  </v-col>
                  <v-col cols="10">
                  </v-col>
                </v-row>
              </v-container>

            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel
            @click="onClickUserPanel"
            >
            <v-expansion-panel-header>
              <v-container>
                <v-row>
                  <v-col><v-icon :color="userColor">mdi-account</v-icon><span class="ml-2">アルバイトさん登録</span></v-col>
                </v-row>
              </v-container>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-container class="mt-4">
                <v-row>
                  <v-col cols="10">
                    アルバイトさん登録や変更を行います。
                  </v-col>
                  <v-col cols="2">
                    <v-btn color="black" outlined small @click="listUser">
                      <v-icon color="grey" >mdi-refresh</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
              <v-container>
                <v-row
                  class="pa-0 mt-2"
                  v-if="showListUserProgress"
                >
                  <v-col cols="2">
                    <v-progress-circular
                      indeterminate
                      color="indigo"
                    ></v-progress-circular>
                  </v-col>
                  <v-spacer></v-spacer>
                </v-row>
                <v-row
                  no-gutters
                >
                  <v-col cols="12">
                    <v-treeview
                      rounded
                      hoverable
                      activatable
                      transition
                      :items="users"
                    >
                      <template slot="label" slot-scope="{ item }">
                        <v-container>
                          <v-row
                            v-if="item.enabled"
                            no-gutters
                            >
                            <v-col cols="2">
                              <v-icon :color="userColor">
                                mdi-account
                              </v-icon>
                            </v-col>
                            <v-col cols="10" class="text-wrap">
                              {{ item.name }}
                            </v-col>
                          </v-row>
                          <v-row
                            v-else
                            no-gutters
                            >
                            <v-col cols="2">
                              <v-icon :color="userDisabledColor">
                                mdi-account-cancel
                              </v-icon>
                            </v-col>
                            <v-col cols="10" class="text-wrap line-through">
                              {{ item.name }}
                            </v-col>
                          </v-row>
                          <v-row
                            justify="start"
                            no-gutters
                            >
                            <v-spacer />
                            <v-col cols="3">
                              <v-btn
                                icon
                                color="blue"
                                @click.native="onClickUserEdit1(item)"
                              >
                                <v-icon>mdi-pencil</v-icon>
                              </v-btn>
                            </v-col>
                            <v-col cols="3">
                              <v-btn
                                v-if="item.enabled"
                                icon
                                color="red"
                                @click.native="onClickUserDisable1(item)"
                              >
                                <v-icon>mdi-cancel</v-icon>
                              </v-btn>
                              <v-btn
                                v-else
                                icon
                                color="green"
                                @click.native="onClickUserEnable1(item)"
                              >
                                <v-icon>mdi-hospital-box</v-icon>
                              </v-btn>
                            </v-col>
                            <v-col cols="3">
                              <v-btn
                                icon
                                color="grey"
                                @click.native="onClickUserDelete1(item)"
                              >
                                <v-icon>mdi-trash-can</v-icon>
                              </v-btn>
                            </v-col>
                          </v-row>
                        </v-container>
                      </template>
                    </v-treeview>
                  </v-col>
                </v-row>
              </v-container>
              <v-container class="mt-1">
                <v-row>
                  <v-col cols="2">
                    <v-btn fab dark small color="pink" @click="registerUser1">
                      <v-icon>mdi-account-plus</v-icon>
                    </v-btn>
                  </v-col>
                  <v-col cols="10">
                  </v-col>
                </v-row>
              </v-container>

            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel
            >
            <v-expansion-panel-header>
              <v-container>
                <v-row>
                  <v-col><v-icon :color="settingsColor">mdi-cog</v-icon><span class="ml-2">各種設定</span></v-col>
                </v-row>
              </v-container>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-container class="mt-4">
                <v-row>
                  <v-col cols="10">
                    定休日の設定などを行います。
                  </v-col>
                  <v-spacer/>
                </v-row>
              </v-container>
              <v-container>
                <v-row
                  no-gutters
                >
                  <v-col cols="12">
                    <v-treeview
                      rounded
                      hoverable
                      activatable
                      transition
                      :items="settings"
                    >
                      <template slot="label" slot-scope="{ item }">
                        <v-container>
                          <v-row
                            align="center"
                            no-gutters
                            >
                            <v-col cols="2">
                              <v-icon :color="item.color">
                                {{ item.icon }}
                              </v-icon>
                            </v-col>
                            <v-col cols="7" class="text-wrap">
                              {{ item.name }}
                            </v-col>
                            <v-col cols="3">
                              <v-btn
                                icon
                                color="blue"
                                @click.native="item.click(item)"
                              >
                                <v-icon>mdi-pencil</v-icon>
                              </v-btn>
                            </v-col>
                          </v-row>
                        </v-container>
                      </template>
                    </v-treeview>
                  </v-col>
                </v-row>
              </v-container>
            </v-expansion-panel-content>
          </v-expansion-panel>

        </v-expansion-panels>
      </div>
    </v-container>

    <v-container justify="center">
      <v-row justify="center">
        <v-dialog
          v-model="showShift.value"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
          <Shift :show-shift="showShift" :user-info="userInfo" :debug="debug" />
        </v-dialog>
      </v-row>

      <v-row justify="center">
        <v-dialog
          v-model="showRegularHoliday.value"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
          <RegularHoliday :show-regular-holiday="showRegularHoliday" :debug="debug" />
        </v-dialog>
      </v-row>

      <v-row justify="center">
        <v-dialog
          v-model="showLimitHours.value"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
          <LimitHours :show-limit-hours="showLimitHours" :debug="debug" />
        </v-dialog>
      </v-row>

      <v-row justify="center">
        <v-dialog
          v-model="showDayOfWeekLimitHours.value"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
          <DayOfWeekLimitHours :show-day-of-week-limit-hours="showDayOfWeekLimitHours" :debug="debug" />
        </v-dialog>
      </v-row>

      <v-row justify="center">
        <v-dialog
          v-model="showPayPerHour.value"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
          <PayPerHour :show-pay-per-hour="showPayPerHour" :debug="debug" />
        </v-dialog>
      </v-row>

      <v-row justify="center">
        <v-dialog
          v-model="showDebugMonitor"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
          <v-card
            class="mx-auto"
          >
            <v-toolbar
              dark
              :color="debugColor"
            >
              <v-btn
                icon
                dark
                @click="showDebugMonitor = false"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <v-toolbar-title>デバッグ</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-row
                v-for="(item, i) in errorLogs"
                :key="i"
                >
                <v-col>{{ item }}</v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-row>

      <v-dialog
        v-model="showRegisterShift"
        max-width="400px"
        @keydown.esc="showRegisterShift = false"
      >
        <v-card>
          <v-card-title>
            <v-container class="mt-4">
              <v-row>
                <v-col cols="9">
                  どなたのシフトを開きますか？
                </v-col>
                <v-col cols="2">
                  <v-btn color="black" outlined small @click="listUser">
                    <v-icon color="grey" >mdi-refresh</v-icon>
                  </v-btn>
                </v-col>
                <v-col cols="1">
                </v-col>
              </v-row>
            </v-container>
          </v-card-title>
          <v-container>
            <v-row
              class="pa-0 mt-2"
              v-if="showListUserProgress"
            >
              <v-col cols="1">
              </v-col>
              <v-col cols="2">
                <v-progress-circular
                  indeterminate
                  color="indigo"
                ></v-progress-circular>
              </v-col>
              <v-col cols="9">
              </v-col>
              <v-spacer></v-spacer>
            </v-row>
          </v-container>
          <v-card-text>
            <v-list
              nav
              dense
            >
              <v-list-item-group
                color="primary"
              >
                <v-list-item
                  v-for="(item, i) in users"
                  :key="i"
                >
                  <v-list-item-icon>
                    <v-icon color="pink">mdi-account</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content @click="onClickShowShift(item)">
                    <v-list-item-title v-text="item.name"></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
              text
              @click="showRegisterShift = false"
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

      <div class="text-center">
        <v-bottom-sheet
          v-model="showRegisterUser"
          inset
          max-width="80%"
        >
          <div
            class="text-center information-window-v-sheet"
          >
            <v-card
              v-if="showRegisterUser"
              class="information-window-v-card">
              <v-btn
                class="mt-6"
                text
                color="error"
                @click="showRegisterUser = !showRegisterUser"
                :disabled="showProgress"
              >
                X
              </v-btn>
              <div class="my-3">
                バイトさん新規登録
              </div>
              <div class="pa-2">
                <v-form
                  ref="form"
                  v-model="valid"
                  lazy-validation
                >
                  <v-text-field
                    v-model="userId"
                    label="ログインID（ex:yamada.tarou）"
                    inputmode="email"
                    v-on:keyup.enter="registerUser2"
                    :disabled="showProgress"
                    required
                  ></v-text-field>

                  <v-text-field
                    v-model="username"
                    label="お名前（ex:山田太郎）"
                    v-on:keyup.enter="registerUser2"
                    :disabled="showProgress"
                    required
                  ></v-text-field>

                  <v-text-field
                    v-model="password"
                    label="パスワード（ex:123456）"
                    v-on:keyup.enter="registerUser2"
                    :disabled="showProgress"
                    inputmode="email"
                    required
                  ></v-text-field>

                  <v-btn
                    color="success"
                    class="mr-4"
                    v-on:keyup.enter="registerUser2"
                    :disabled="showProgress"
                    @click="registerUser2"
                  >
                    登録
                  </v-btn>
                </v-form>
              </div>
            </v-card>
          </div>
        </v-bottom-sheet>
      </div>

      <div class="text-center">
        <v-bottom-sheet
          v-model="showEditUser"
          inset
          max-width="80%"
        >
          <div
            class="text-center information-window-v-sheet"
          >
            <v-card
              v-if="showEditUser"
              class="information-window-v-card">
              <v-btn
                class="mt-6"
                text
                color="error"
                @click="showEditUser = !showEditUser"
              >
                X
              </v-btn>
              <div class="my-3">
                バイトさん更新
              </div>
              <div class="pa-2">
                <v-form
                  ref="form"
                  v-model="valid"
                  lazy-validation
                >
                  <v-text-field
                    v-model="userId"
                    disabled
                    label="ログインID（ex:yamada.tarou）"
                    inputmode="email"
                    required
                  ></v-text-field>

                  <v-text-field
                    v-model="username"
                    label="お名前（ex:山田太郎）"
                    v-on:keyup.enter="onClickUserEdit2"
                    :disabled="showProgress"
                    required
                  ></v-text-field>

                  <v-checkbox
                    v-model="editpassword"
                    label="パスワードを変更する"
                    :disabled="showProgress"
                    value="1"
                  ></v-checkbox>

                  <v-text-field
                    v-if="editpassword"
                    v-model="password"
                    label="旧パスワード（ex:123456）"
                    v-on:keyup.enter="onClickUserEdit2"
                    inputmode="email"
                    :disabled="showProgress"
                    required
                  ></v-text-field>

                  <v-text-field
                    v-if="editpassword"
                    v-model="newpassword"
                    label="新パスワード（ex:abcdef）"
                    v-on:keyup.enter="onClickUserEdit2"
                    inputmode="email"
                    :disabled="showProgress"
                    required
                  ></v-text-field>

                  <v-btn
                    color="success"
                    class="mr-4"
                    :disabled="showProgress"
                    @click="onClickUserEdit2"
                  >
                    更新
                  </v-btn>
                </v-form>
              </div>
            </v-card>
          </div>
        </v-bottom-sheet>
      </div>

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

      <v-speed-dial
        direction="top"
        transition="slide-y-reverse-transition"
        class="bottom-btn no-print"
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
          v-if="debug.value"
          fab
          dark
          small
          :color="debugColor"
          @click="onClickShowDebug"
        >
          <v-icon>mdi-bug</v-icon>
        </v-btn>
        <v-btn
          fab
          dark
          small
          color="pink"
          @click="registerUser1"
        >
          <v-icon>mdi-account-plus</v-icon>
        </v-btn>
        <v-btn
          fab
          dark
          small
          color="green"
          @click="registerShift1"
        >
          <v-icon>mdi-calendar-search</v-icon>
        </v-btn>
      </v-speed-dial>
    </v-container>
    <v-progress-linear
      indeterminate
      color="primary"
      v-show="showProgress"
      dense
      height="8"
      class="fixed-bottom"
    ></v-progress-linear>
  </v-app>
</template>
<script>
import Vue from 'vue'
import Amplify, { API, Auth } from 'aws-amplify'
import Shift from '@/components/Shift' // eslint-disable-line no-unused-vars
import UniShift from '@/components/UniShift' // eslint-disable-line no-unused-vars
import RegularHoliday from '@/components/RegularHoliday' // eslint-disable-line no-unused-vars
import LimitHours from '@/components/LimitHours' // eslint-disable-line no-unused-vars
import DayOfWeekLimitHours from '@/components/DayOfWeekLimitHours' // eslint-disable-line no-unused-vars
import PayPerHour from '@/components/PayPerHour' // eslint-disable-line no-unused-vars
import moment from 'moment' // eslint-disable-line no-unused-vars
import $ from 'jquery' // eslint-disable-line no-unused-vars
const awsExports = require('@/aws-exports').default
Amplify.configure(awsExports)
import Notifications from 'vue-notification'
Vue.use(Notifications)
var id = 0
function generateId() { return id++ }
export default {
  name: 'Index',
  components: {
    Shift, RegularHoliday, LimitHours, DayOfWeekLimitHours, PayPerHour,
  },
  data () {
    return {
      appName: ``,
      appColor: ``,
      isMobile: false,

      uniqueId: generateId(),
      showInfo: false,
      showDebug: false,
      showDebugMonitor: false,
      debugColor: '#1AED1A',
      errorLogs: [],

      infoMessage: [],
      debugMessage: [],
      onInfoClick: (() => {}),

      users: [],
      shifts: [],
      settings: [
        { id: 0, name: `定休日設定`, icon: `mdi-sleep`, color:`orange`, click: (item) => { this.onClickShowRegularHoliday(item) } },
        { id: 1, name: `曜日別固定上限時間設定`, icon: `mdi-calendar-week`, color:`cyan`, click: (item) => { this.onClickShowDayOfWeekLimithours(item) } },
        { id: 2, name: `日別上限時間設定(曜日別よりこちらが優先されます)`, icon: `mdi-clock-time-eight-outline`, color:`purple`, click: (item) => { this.onClickShowLimithours(item) } },
        { id: 3, name: `時給設定`, icon: `mdi-currency-cny`, color:`lime darken-3`, click: (item) => { this.onClickShowPayPerHour(item) } },
      ],
      preview: {},

      userInfo: {},

      showSearch: false,
      showShift: { value: false },
      showUniShift: { value: false },
      showRegularHoliday: { value: false },
      showLimitHours: { value: false },
      showDayOfWeekLimitHours: { value: false },
      showPayPerHour: { value: false },

      onClickDangerOK: undefined,
      onClickWarnOK: undefined,
      onClickInfoOK: undefined,

      showRegisterShift: false,

      editpassword: false,
      selectedUserItem: undefined,
      shiftColor: 'green',
      userColor: 'pink',
      settingsColor: 'darkgrey',
      userDisabledColor: 'grey',
      shiftPanel: undefined,
      userPanel: undefined,
      showAlertDanger: false,
      showAlertWarn: false,
      showAlertInfo: false,
      showListUserProgress: false,
      showListShiftProgress: false,
      showProgress: false,
      showError: false,
      showRegisterUser: false,
      showEditUser: false,
      errorMessage: [],
      alertMessage: [],
      userId: undefined,
      username: undefined,
      password: undefined,
      newpassword: undefined,
      userListInitialized: false,
      shiftListInitialized: false,

      debug: { value: false },

      focusListener: undefined,
    }
  },
  async created () {
    this.appName = process.env.VUE_APP_NAME
    this.appColor = process.env.VUE_APP_COLOR
    const self = this
    this.debug.value = (await this.isDev())
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
    this.eventBusOn('show-error', obj => { // eslint-disable-line no-unused-vars
      this.showError = obj.show
      this.errorMessage = obj.message
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
    this.eventBusOn('close-shift', () => { // eslint-disable-line no-unused-vars
      this.showShift.value = false
    })
    this.eventBusOn('close-unishift', () => { // eslint-disable-line no-unused-vars
      this.showUniShift.value = false
    })
    this.eventBusOn('close-regular-holiday', () => { // eslint-disable-line no-unused-vars
      this.showRegularHoliday.value = false
    })
    this.eventBusOn('close-limit-hours', () => { // eslint-disable-line no-unused-vars
      this.showLimitHours.value = false
    })
    this.eventBusOn('close-day-of-week-limit-hours', () => { // eslint-disable-line no-unused-vars
      this.showDayOfWeekLimitHours.value = false
    })
    this.eventBusOn('close-pay-per-hour', () => { // eslint-disable-line no-unused-vars
      this.showPayPerHour.value = false
    })
    this.eventBusOn('put-error-log', log => { // eslint-disable-line no-unused-vars
      this.errorLogs.push(log)
    })
    this.eventBusOn('show-debug', async (obj) => { // eslint-disable-line no-unused-vars
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
    this.eventBusOn('show-info', obj => { // eslint-disable-line no-unused-vars
      this.showInfo = obj.show
      this.infoMessage = obj.message != undefined ? obj.message : this.infoMessage
      this.onInfoClick = obj.data != undefined && obj.data.click != undefined ? obj.data.click : this.onInfoClick
    })
    window.onbeforeprint = function() {
      $(".v-dialog__content.v-dialog__content--active").each((index, element) => { // eslint-disable-line no-unused-vars
        $(element).css('position', 'inherit')
      })
      $(".v-dialog--fullscreen").each((index, element) => { // eslint-disable-line no-unused-vars
        $(element).css('position', 'absolute')
        $(element).css('overflow', 'visible')
      })
    }
    window.onafterprint = function() {
      $(".v-dialog__content.v-dialog__content--active").each((index, element) => { // eslint-disable-line no-unused-vars
        $(element).css('position', '')
      })
      $(".v-dialog--fullscreen").each((index, element) => { // eslint-disable-line no-unused-vars
        $(element).css('position', 'fixed')
        $(element).css('overflow', 'auto')
      })
    }

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

    window.removeEventListener('resize', this.onResize, { passive: true })
  },
  computed: {
  },
  methods: {
    onResize () {
      this.isMobile = window.innerWidth < 600
    },
    getPreview (item) {
      let aPreview = this.preview[item.userId]
      if (aPreview) {
        let start = moment(aPreview.start)
        let end   = moment(aPreview.end)
        let diff = end.diff(start, 'hours')
        return `明日${start.format('H')}時～${end.format('H')}時(${diff})`
      }
      return ``
    },
    async showDebugFunc (obj) {
      if (this.debug.value === false) return
      if (obj.show) {
        if (obj.message) {
          for (let messe of obj.message) {
            this.$notify({
              title: `${messe} / ${(await this.getUserEnv())} / id: ${this.uniqueId}`,
              text: ``,
              duration: 3000,
              group: 'notifications',
              type: `warn`,
              closeOnClick: true,
            })
          }
        }
      }
    },
    onClickShowDebug () {
      this.showDebugMonitor = true
    },
    registerShift1 () {
      this.showRegisterShift = true
      if (!this.userListInitialized) {
        this.listUser()
      }
      this.userListInitialized = true
    },
    onClickShowShift (item) { // eslint-disable-line no-unused-vars
      this.userInfo = { userId: item.userId, username: item.username }
      this.showShift.value = true
      this.eventBusEmit('reload-shift', { today: moment().format('yyyy-MM-DD'), userInfo: this.userInfo } )
    },
    onClickShowUniShift (item) { // eslint-disable-line no-unused-vars
      this.userInfo = { userId: item.userId, username: item.username }
      this.showUniShift.value = true
      this.eventBusEmit('reload-uni-shift', { today: moment().format('yyyy-MM-DD'), userInfo: this.userInfo } )
    },
    onClickShowRegularHoliday (item) { // eslint-disable-line no-unused-vars
      this.showRegularHoliday.value = true
      this.eventBusEmit('reload-regular-holiday', { today: moment().format('yyyy-MM-DD') } )
    },
    onClickShowLimithours (item) { // eslint-disable-line no-unused-vars
      this.showLimitHours.value = true
      this.eventBusEmit('reload-limit-hours', { today: moment().format('yyyy-MM-DD') } )
    },
    onClickShowDayOfWeekLimithours (item) { // eslint-disable-line no-unused-vars
      this.showDayOfWeekLimitHours.value = true
      this.eventBusEmit('reload-day-of-week-limit-hours', { today: moment().format('yyyy-MM-DD') } )
    },
    onClickShowPayPerHour (item) { // eslint-disable-line no-unused-vars
      this.showPayPerHour.value = true
      this.eventBusEmit('reload-pay-per-hour', { today: moment().format('yyyy-MM-DD') } )
    },
    async onClickUserEdit1 (item) {
      this.selectedUserItem = item
      this.showEditUser = true
      this.userId = item.userId
      this.username = item.username
      this.editpassword = undefined
      this.password = this.newpassword = undefined
    },
    async onClickUserEdit2 () {
      this.eventBusEmit('show-alert-info', {
        show: true, message: [ `${this.selectedUserItem.name}を変更します。` ], ok: this.onClickUserEdit3
      })
    },
    async onClickUserEdit3 () {
      this.showProgress = true
      this.showAlertInfo = false
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userId: this.selectedUserItem.userId,
          username: this.username,
          editpassword: this.editpassword,
          oldpassword: this.password,
          newpassword: this.newpassword,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/update_user`, params).then(response => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.showEditUser = false
        this.selectedUserItem.username = this.username
        this.selectedUserItem.name = `${this.username} (${this.selectedUserItem.userId})`
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.eventBusEmit('show-error', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    async onClickUserDelete1 (item) {
      this.selectedUserItem = item
      this.eventBusEmit('show-alert-danger', {
        show: true, message: [ `${item.name}を完全に削除します。`, `（シフトデータは残ります。）` ], ok: this.onClickUserDelete2
      })
    },
    async onClickUserDelete2 () {
      this.showProgress = true
      this.showAlertDanger = false
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userId: this.selectedUserItem.userId,
        }
      }
      API.del((await this.apiNameForLoginUser()), `/delete_user`, params).then(response => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.users = this.users.filter(item => item.userId != this.selectedUserItem.userId)
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.eventBusEmit('show-error', { show: true, message: [ `削除に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    async onClickUserEnable1 (item) {
      this.selectedUserItem = item
      this.eventBusEmit('show-alert-info', {
        show: true, message: [ `${item.name}を有効にします。` ], ok: this.onClickUserEnable2
      })
    },
    async onClickUserEnable2 () {
      this.showProgress = true
      this.showAlertInfo = false
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userId: this.selectedUserItem.userId,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/enable_user`, params).then(response => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.selectedUserItem.enabled = true
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.eventBusEmit('show-error', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    async onClickUserDisable1 (item) {
      this.selectedUserItem = item
      this.eventBusEmit('show-alert-warn', {
        show: true, message: [ `${item.name}を無効にします。` ], ok: this.onClickUserDisable2
      })
    },
    async onClickUserDisable2 () {
      this.showProgress = true
      this.showAlertWarn = false
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userId: this.selectedUserItem.userId,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/disable_user`, params).then(response => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.selectedUserItem.enabled = false
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.showProgress = false
        this.eventBusEmit('show-error', { show: true, message: [ `更新に失敗しました！!`, `やり直してください。` ] } )
        console.log('error', error)
      })
    },
    async onClickShiftPanel () {
      if (!this.shiftListInitialized) {
        this.listShift()
      }
      this.shiftListInitialized = true
    },
    async onClickUserPanel () {
      if (!this.userListInitialized) {
        this.listUser()
      }
      this.userListInitialized = true
    },
    async listShift () {
      this.showListShiftProgress = true
      API.get((await this.apiNameForLoginUser()), `/list_shift`, { headers: (await this.getAuthHeader())}).then(response => { // eslint-disable-line no-unused-vars
        console.log(response);
        let data = response.data
        this.shifts = []
        this.preview = response.preview
        data.forEach(user => {
          let userId = user.Username
          let username = user.UsernameJa
          this.shifts.push({
            id: userId,
            name: `${username} (${userId})`,
            username: username,
            userId: userId,
          })
        })
        this.showListShiftProgress = false
      }).catch((error) => { // eslint-disable-line no-unused-vars
        console.log('error', error)
        this.eventBusEmit('show-error', { show: true, message: [ `検索に失敗しました！!`, `やり直してください。` ] } )
        // this.showListUserProgress = false
      })
    },
    async listUser () {
      this.showListUserProgress = true
      API.get((await this.apiNameForLoginUser()), `/list_user`, { headers: (await this.getAuthHeader())}).then(response => { // eslint-disable-line no-unused-vars
        console.log(response);
        let data = response.data
        this.users = []
        data.forEach(user => {
          let enabled = user.Enabled
          let userCreateDate = user.UserCreateData
          let userLastModifiedDate = user.UserLastModifiedDate
          let userId = user.Username
          let username = user.UsernameJa
          this.users.push({
            id: userId,
            name: `${username} (${userId})`,
            username: username,
            userId: userId,
            enabled: enabled,
            createdAt: moment(userCreateDate).format('yyyy年MM月DD hh時mm分ss秒'),
            updatedAt: moment(userLastModifiedDate).format('yyyy年MM月DD hh時mm分ss秒'),
          })
        })
        this.showListUserProgress = false
      }).catch((error) => { // eslint-disable-line no-unused-vars
        console.log('error', error)
        this.eventBusEmit('show-error', { show: true, message: [ `検索に失敗しました！!`, `やり直してください。` ] } )
        // this.showListUserProgress = false
      })
    },
    registerUser1 () {
      this.userId = this.username = this.editpassword = this.password = this.newpassword = undefined
      this.showRegisterUser = true
    },
    async registerUser2 () {
      this.showProgress = true
      const params = {
        headers: (await this.getAuthHeader()),
        body: {
          userId: this.userId,
          username: this.username,
          password: this.password,
        }
      }
      API.post((await this.apiNameForLoginUser()), `/register_user`, params).then(response => { // eslint-disable-line no-unused-vars
        this.showRegisterUser = false
        this.showProgress = false
        this.users.push({
          id: this.userId,
          name: `${this.username} (${this.userId})`,
          username: this.username,
          userId: this.userId,
          enabled: true,
        })
      }).catch((error) => { // eslint-disable-line no-unused-vars
        this.showRegisterUser = false
        this.showProgress = false
        this.eventBusEmit('show-error', { show: true, message: [ `登録に失敗しました！!`, `しばらく経ってからやり直してください。` ] } )
        console.log('error', error)
      })
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
.z-index-top {
  z-index: 20003;
}
.bottom-btn {
  position: fixed;
  bottom: 0px;
  right: 16px;
  margin: 0 0 16px 16px;
}
.line-through {
  text-decoration: line-through;
}
</style>
<style lang="scss">
@media print {
  .no-print {
    display: none;
  }
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