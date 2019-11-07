/*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
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
    let rounds = competition.rounds
    competitionService.postCompetition(competition)
    .then(competition => {
      // because of async api the commit wont wait on rounds addition
      // se when submiting round - retrieve competition again and update store
      commit('addCompetition', competition)
      rounds.forEach(function (round, i) {
        round.ord = i + 1;  // could be there before
        round.is_open = true;  // could be there before
        round.competition = competition.id;
        competitionService.postRound(round)
        .then(() => {
          // here we could also return round and append it to competition rounds
          competitionService.fetchCompetitions(competition.id)
          .then(competition => {
            commit('updateCompetition', competition)
          })
        })
      })
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
    state.competitions.unshift(competition)
  },
  updateCompetition(state, competition) {
    const index = state.competitions.findIndex(obj => obj.id === competition.id);
    if (index !== -1)state.competitions.splice(index, 1, competition)
  },
  deleteCompetition(state, compId) {
    state.competitions = state.competitions.filter(obj => obj.id !== compId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
