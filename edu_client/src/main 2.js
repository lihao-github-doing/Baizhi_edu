import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

Vue.prototype.$axios = axios;

import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(Element);

Vue.config.productionTip = false

import "./static/css/global.css"

import settings from "./settings"

Vue.prototype.$settings = settings;

import "./static/js/gt.js"

import VideoPlayer from 'vue-video-player'

require('video.js/dist/video-js.css')
require('vue-video-player/src/custom-theme.css')
Vue.use(VideoPlayer)

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
