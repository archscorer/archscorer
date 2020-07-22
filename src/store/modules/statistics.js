import statisticsService from '@/services/statisticsService'

const state = {
  records: []
}

const getters = {
  records: state => {
    return state.records
  }
}

const actions = {
  getRecords({ commit }) {
    statisticsService.fetchRecords()
    .then(records => {
      commit('setRecords', records)
    })
  }
}

const mutations = {
  setRecords(state, records) {
    state.records = records
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
