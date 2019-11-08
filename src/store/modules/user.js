/*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

import userService from '@/services/userService'

const state = {
  user: null
}

const getters = {
  user: state => {
    return state.user
  }
}

const actions = {
  userLogin({ commit }, payload) {
    userService.postAuth('login', payload)
    .then(user => {
      commit('setUser', user)
    })
  },
  userLogout({ commit }) {
    userService.postAuth('logout')
    .then(response => {
      console.log(response)
      commit('delUser')
    })
  }
}

const mutations = {
  setUser(state, user) {
    state.user = user
  },
  delUser(state) {
    state.user = null
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
