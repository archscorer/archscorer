import api from '@/services/api'

export default {
  fetchRecords() {
    return api.get(`records/`)
              .then(response => response.data)
  }
}
