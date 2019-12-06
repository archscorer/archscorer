import userService from '@/services/userService'

const state = {
  user: {
    id: null,
    email: '',
    archer: {
      id: null,
    }
  }
}

const getters = {
  user: state => {
    return state.user
  }
}

const actions = {
  userLogout({ commit }) {
    commit('logout')
  },
  checkUser({ commit }) {
    userService.getUser()
    .then(user => {
      commit('setUser', user)
    }).catch(() => {})
  },
  updateArcher({ commit }, archer) {
    if (archer.id !== null) {
      userService.putArcher(archer.id, archer)
      .then(archer => {
        commit('updateArcher', archer)
      })
    } else {
      userService.postArcher(archer)
      .then(archer => {
        commit('updateArcher', archer)
      })
    }
  }
}

const mutations = {
  setUser(state, user) {
    state.user = user[0]
  },
  logout(state) {
    state.user = {
      id: null,
      email: '',
      archer: {
        id: null,
      }
    }
  },
  updateArcher(state, archer) {
    state.user.archer = archer
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
