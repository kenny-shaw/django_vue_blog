import Vue from 'vue'
import Vuex from 'vuex'
import Cookie from 'vue-cookies'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: Cookie.get('username'),
    token: Cookie.get('token'),
    userid: Number(Cookie.get('userid'))
  },
  mutations: {
    saveToken: (state, userToken) => {
      state.username = userToken.username
      state.token = userToken.token
      state.userid = userToken.userid
      Cookie.set('username', userToken.username, '3d')
      Cookie.set('token', userToken.token, '3d')
      Cookie.set('userid', userToken.userid, '3d')
    },
    clearToken: state => {
      state.username = null
      state.token = null
      state.userid = null
      Cookie.remove('username')
      Cookie.remove('token')
      Cookie.remove('userid')
    }
  },
  actions: {},
  modules: {}
})
