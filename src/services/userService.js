import api from '@/services/api'

export default {
  getUser() {
    return api.get(`user/`)
              .then(response => response.data)
  },
  getArcher() {
    return api.get(`archer/`)
              .then(response => response.data)
  },
  postArcher(payload) {
    return api.post(`archer/`, payload)
              .then(response => response.data)
  }
}
