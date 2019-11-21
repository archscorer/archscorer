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
  userLogout({ commit }) {
    commit('delUser')
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
