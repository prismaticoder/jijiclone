import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || '',
    user: localStorage.getItem('user') || ""
  },
  getters: {
    isLoggedIn: state => !!state.token,
  },
  mutations: {
    USER_LOGIN(state, data) {
      state.token = data.token,
      state.user = data.username
    },
    USER_LOGOUT(state) {
      state.token = "",
      state.user = ""
    }
  },
  actions: {
    logout({commit}) {
      return new Promise((resolve) => {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
        commit('USER_LOGOUT')
        resolve()
      })
    },
    loginUser({commit}, data) {
      return new Promise((resolve) => {
        localStorage.setItem('token', data.token)
        localStorage.setItem('user', data.user)
        commit('USER_LOGIN', data)
        resolve()
      })
    }
  },
  modules: {
  }
})
