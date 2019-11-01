import competitionService from '@/services/competitionService'

const state = {
  competitions: []
}

const getters = {
  competitions: state => {
    return state.competitions
  }
}

const actions = {
  getCompetitions({ commit }) {
    competitionService.fetchCompetitions()
    .then(competitions => {
      commit('setCompetitions', competitions)
    })
  },
  addCompetition({ commit }, competition) {
    competitionService.postCompetition(competition)
    .then(() => {
      commit('addCompetition', competition)
    })
  },
  deleteCompetition({ commit }, compId) {
    competitionService.deleteCompetition(compId)
    commit('deleteCompetition', compId)
  }
}

const mutations = {
  setCompetitions(state, competitions) {
    state.competitions = competitions
  },
  addCompetition(state, competition) {
    state.competitions.push(competition)
  },
  deleteCompetition(state, compId) {
    state.competitions = state.competitions.filter(obj => obj.ok !== compId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
