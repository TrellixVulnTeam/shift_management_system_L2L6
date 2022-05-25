<template>
  <div id="app">
    <router-view/>
  </div>
</template>
<script>
import { API } from 'aws-amplify'
export default {
  name: 'App',
  created: function () {
    if (!process.env.NODE_ENV.endsWith('-prod')) return
    var requested = false
    const self = this
    const checkAppWasUpdated = function () {
      if (requested) return
      requested = true
      API.get(process.env.VUE_APP_API_NAME, '/app_hash', { queryStringParameters: { origin: location.href } }).then(response => {
        self.eventBusEmit('show-debug', { show: true, message: [`app_hash: ${response.hash.substring(0, 8)} / version: 1.2`] })
        console.log(response)
        console.log(`CHECK_XXXXXXXXX__XXX ${self.lsget('app_hash')} / ${response.hash}`);
        if (self.lsget('app_hash') != undefined && self.lsget('app_hash') !== response.hash) {
          const reload = function () {
            self.lsset('app_hash', response.hash)
            location.reload(true)
          }
          self.eventBusEmit('show-info', {
            show: true,
            message: [ `データが更新されました !!`, `ページをリロードしてください。` ],
            data: {
              click: reload,
            }
          })
        } else {
          self.lsset('app_hash', response.hash)
        }
        requested = false
      }).catch(error => {
        console.log('error', error)
        requested = false
      })
    }
    if (true) { // eslint-disable-line no-constant-condition
      var hidden, visibilityState, visibilityChange; // eslint-disable-line no-unused-vars

      if (typeof document.hidden !== "undefined") {
        hidden = "hidden", visibilityChange = "visibilitychange", visibilityState = "visibilityState";
      } else if (typeof document.msHidden !== "undefined") {
        hidden = "msHidden", visibilityChange = "msvisibilitychange", visibilityState = "msVisibilityState";
      }

      var document_hidden = document[hidden];

      document.addEventListener(visibilityChange, function() {
        if(document_hidden != document[hidden]) {
          if(document[hidden]) {
            // Document hidden
          } else {
            // Document shown
            checkAppWasUpdated()
          }

          document_hidden = document[hidden];
        }
      });
    }
    this.eventBusOn('check-app-was-updated', () => { // eslint-disable-line no-unused-vars
      checkAppWasUpdated()
    })
  }
}
</script>
<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>