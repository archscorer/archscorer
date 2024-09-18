import api from '@/services/api'

export default {
  getUser() {
    return api.get(`user/`)
              .then(response => {
                // every time user object is updated update csrftoken as well
                api.defaults.headers.common['X-CSRFToken'] = response.data[0].csrftoken
                return response.data
              })
    //
  },
  putArcher(aId, payload) {
    return api.put(`archer/${aId}/`, payload)
              .then(response => response.data)
  },
  searchArcher(payload) {
    return api.post(`archer/search/`, payload)
              .then(response => response.data)
  },
  getArcherClassification(attr) {
    return api.post(`archer/archer_classification/`, attr)
              .then(response => response.data)
  }
}
