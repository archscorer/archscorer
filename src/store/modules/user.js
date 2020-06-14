import userService from '@/services/userService'

const state = {
  user: {
    id: null,
    email: '',
    archer: {
      id: null,
    }
  },
  qresponse: [],
}

const getters = {
  user: state => {
    return state.user
  },
  qresponse: state => {
    return state.qresponse
  }
}

const actions = {
  checkUser({ commit }) {
    userService.getUser()
    .then(user => {
      commit('setUser', user)
    }).catch(() => {})
  },
  putArcher({ commit }, archer) {
    userService.putArcher(archer.id, archer)
    .then(archer => {
      commit('updateArcher', archer)
    })
  },
  searchArcher({ commit }, query) {
    userService.searchArcher({query: query})
    .then(response => {
      commit('setQresponse', response)
    })
  },
  clearSearch({ commit }, message) {
    commit('setQresponse', message)
  }
}

const mutations = {
  setUser(state, user) {
    state.user = user[0]
  },
  updateArcher(state, archer) {
    state.user.archer = archer
  },
  setQresponse(state, response) {
    state.qresponse = response
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
