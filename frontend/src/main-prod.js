import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
// 配置按需导入element-ui
// import './plugins/element.js'
// 导入全局样式表
import './assets/css/global.css'
// 引入图标
import './assets/icon/iconfont.css'
// 引入显示类，用于窗口大小满足一定条件时，元素的隐藏或显示
import 'element-ui/lib/theme-chalk/display.css'
// 导入moment时间模块
import moment from 'moment'
// 导入mavonEditor模块
import 'mavon-editor/dist/css/index.css'
import mavonEditor from 'mavon-editor'
// 导入NProgress对应的JS和CSS
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
Vue.prototype.$moment = moment
// 这里是进行了汉化
moment.locale('zh-cn')
// 注册mavonEditor
Vue.use(mavonEditor)
// 在vue的全局变量中设置了$axios=axios
// 以后每个组件使用时：this.$axios
axios.defaults.baseURL = 'http://101.132.74.181:8080/api/v1/'
// 在request拦截器中，展示进度条 NProgress.start()
axios.interceptors.request.use(config => {
  NProgress.start()
  return config
})
// 在response拦截器中，隐藏进度条 NProgress.done()
axios.interceptors.response.use(config => {
  NProgress.done()
  return config
})
Vue.prototype.$axios = axios

Vue.config.productionTip = false

// router拦截器
router.beforeEach((to, from, next) => {
  // 如果该路由需要登录，并且没有登录，则会跳转到登录界面
  if (to.meta.requireAuth) {
    if (store.state.token) {
      next()
    } else {
      next({ name: 'login', query: { nextUrl: to.fullPath } })
    }
  } else {
    // 如果已登录，无法再次跳转到登录界面
    if (store.state.token && to.name === 'login') {
      return next({ path: from.path })
    }
    next()
  }
})
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
