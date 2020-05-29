import seriesService from '@/services/seriesService'

const state = {
  series: []
}

const getters = {
  series: state => {
    return state.series
  },
  seriesById: (state) => (id) => {
    return state.series.find(obj => obj.id === id)
  }
}

const actions = {
  getSeries({ commit }) {
    seriesService.fetchSeries()
    .then(series => {
      commit('setSeries', series)
    })
  },
  updateSeries({ commit }, sId) {
    return seriesService.fetchSeries(sId)
    .then(series => {
      commit('updateSeries', series)
    })
  },
  addSeries({ commit }, series) {
    seriesService.postSeries(series)
    .then(series => {
      commit('addSeries', series)
    })
  },
  deleteSeries({ commit }, cId) {
    seriesService.deleteSeries(cId)
    commit('deleteSeries', cId)
  }
}

const mutations = {
  setSeries(state, series) {
    state.series = series
  },
  addSeries(state, series) {
    state.series.unshift(series)
  },
  updateSeries(state, series) {
    const index = state.series.findIndex(obj => obj.id === series.id);
    if (index !== -1) {
      state.series.splice(index, 1, series)
    } else {
      state.series.push(series)
    }
  },
  deleteSeries(state, cId) {
    state.series = state.series.filter(obj => obj.id !== cId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
