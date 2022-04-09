import api from '@/services/api'

export default {
  fetchRecords() {
    return api.get(`records/`)
              .then(response => response.data)
  },
  postRecord(payload) {
    return api.post(`records/`, payload)
              .then(response => response.data)
  },
  putRecord(rId, payload) {
    return api.put(`records/${rId}/`, payload)
              .then(response => response.data)
  }
}
