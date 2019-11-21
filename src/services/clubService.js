import api from '@/services/api'

export default {
  fetchClubs(cId = '') {
    // this allows to get a list of all club or just single club
    return api.get(`clubs/${cId ? cId + '/' : ''}`)
              .then(response => response.data)
  },
  postClub(payload) {
    return api.post(`clubs/`, payload)
              .then(response => response.data)
  },
  deleteClub(cId) {
    return api.delete(`clubs/${cId}/`)
              .then(response => response.data)
  }
}
