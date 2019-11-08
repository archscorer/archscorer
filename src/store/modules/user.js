/*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

import userService from '@/services/userService'

const state = {
  user: {
    id: null,
    email: ''
  }
}

const getters = {
  user: state => {
    return state.user
  }
}

const actions = {
  userLogin({ commit }, payload) {
    let formData = new FormData();
    Object.keys(payload).forEach(function (key) {
      formData.append(key, payload[key]);
    });
    userService.postAuth('login', '?next=/api/user/', formData)
    .then((user) => {
      commit('setUser', user)
    })
  },
  userLogout({ commit }) {
    let formData = new FormData();
    userService.postAuth('logout', '?next=/', formData)
    .then(() => {
      commit('delUser')
    })
  },
  checkUser({ commit }) {
    userService.getUser()
    .then(user => {
      commit('setUser', user)
    }).catch(() => {})
  }
}

const mutations = {
  setUser(state, user) {
    state.user = user[0]
  },
  delUser(state) {
    state.user = {
      id: null,
      email: ''
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
