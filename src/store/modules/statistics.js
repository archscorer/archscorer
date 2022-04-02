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
  },
  addRecord({ commit }, record) {
    statisticsService.postRecord(record)
    .then(record => {
      commit('addRecord', record)
    })
  },
  putRecord({ commit }, record) {
    statisticsService.putRecord(record.id, record)
    .then(record => {
      commit('updateRecord', record)
    })
  },
}

const mutations = {
  setRecords(state, records) {
    state.records = records
  },
  updateRecord(state, record) {
    const ci = state.records.findIndex(obj => obj.id === record.id);
    if (ci !== -1) {
      state.records.splice(ci, 1, record)
    } else {
      state.records.push(record)
    }
  },
  addRecord(state, record) {
    state.records.unshift(record)
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
