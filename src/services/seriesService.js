import api from '@/services/api'

export default {
  fetchSeries(sId = '') {
    // this allows to get a list of all club or just single club
    return api.get(`series/${sId ? sId + '/' : ''}`)
              .then(response => response.data)
  },
  postSeries(payload) {
    return api.post(`series/`, payload)
              .then(response => response.data)
  },
  deleteSeries(sId) {
    return api.delete(`series/${sId}/`)
              .then(response => response.data)
  }
}
