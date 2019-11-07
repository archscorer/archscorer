import api from '@/services/api'

export default {
  fetchCompetitions(compId = '') {
    // given argument - if omitter allows to get a list of all competitions or
    // if defined just single competitions
    return api.get(`competitions/${compId}`)
              .then(response => response.data)
  },
  postCompetition(payload) {
    return api.post(`competitions/`, payload)
              .then(response => response.data)
  },
  deleteCompetition(compId) {
    return api.delete(`competitions/${compId}`)
              .then(response => response.data)
  },
  postRound(payload) {
    return api.post(`rounds/`, payload)
              .then(response => response.data)
  },
  deleteRound(rId) {
    return api.delete(`rounds/${rId}`)
              .then(response => response.data)
  }
}
