import api from '@/services/api'

export default {
  getUser() {
    return api.get(`user/`)
              .then(response => response.data)
  },
  postArcher(payload) {
    return api.post(`archer/`, payload)
              .then(response => response.data)
  },
  putArcher(aId, payload) {
    return api.patch(`archer/${aId}/`, payload)
              .then(response => response.data)
  },
  searchArcher(payload) {
    return api.post(`archer/search/`, payload)
              .then(response => response.data)
  }
}
