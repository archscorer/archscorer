import api from '@/services/api'

export default {
  fetchCompetitions() {
    return api.get(`competitions/`)
              .then(response => response.data)
  },
  postCompetition(payload) {
    return api.post(`competitions/`, payload)
              .then(response => response.data)
  },
  deleteCompetition(compId) {
    return api.delete(`competitions/${compId}`)
              .then(response => response.data)
  }
}
