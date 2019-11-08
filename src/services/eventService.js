import api from '@/services/api'

export default {
  fetchEvents(compId = '') {
    // given argument - if omitter allows to get a list of all events or
    // if defined just single events
    return api.get(`events/${compId}`)
              .then(response => response.data)
  },
  postEvent(payload) {
    return api.post(`events/`, payload)
              .then(response => response.data)
  },
  deleteEvent(compId) {
    return api.delete(`events/${compId}`)
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
