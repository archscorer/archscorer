import clubService from '@/services/clubService'

const state = {
  clubs: []
}

const getters = {
  clubs: state => {
    return state.clubs
  }
}

const actions = {
  getClubs({ commit }) {
    clubService.fetchClubs()
    .then(clubs => {
      commit('setClubs', clubs)
    })
  },
  addClub({ commit }, club) {
    clubService.postClub(club)
    .then(club => {
      commit('addClub', club)
    })
  },
  deleteClub({ commit }, cId) {
    clubService.deleteClub(cId)
    commit('deleteClub', cId)
  }
}

const mutations = {
  setClubs(state, clubs) {
    state.clubs = clubs
  },
  addClub(state, club) {
    state.clubs.unshift(club)
  },
  deleteClub(state, cId) {
    state.clubs = state.clubs.filter(obj => obj.id !== cId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
