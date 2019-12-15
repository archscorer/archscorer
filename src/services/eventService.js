import api from '@/services/api'

export default {
  fetchEvents(eId = '') {
    // given argument - if omitter allows to get a list of all events or
    // if defined just single events
    return api.get(`events/${eId ? eId + '/' : ''}`)
              .then(response => response.data)
  },
  postEvent(payload) {
    return api.post(`events/`, payload)
              .then(response => response.data)
  },
  deleteEvent(eId) {
    return api.delete(`events/${eId}/`)
              .then(response => response.data)
  },
  putEvent(eId, payload) {
    return api.put(`events/${eId}/`, payload)
              .then(response => response.data)
  },

  postRound(payload) {
    return api.post(`events/rounds/add/`, payload)
              .then(response => response.data)
  },
  deleteRound(rId) {
    return api.delete(`events/rounds/${rId}/`)
              .then(response => response.data)
  },
  putRound(rId, payload) {
    return api.delete(`events/rounds/${rId}/`, payload)
              .then(response => response.data)
  },

  optsParticipant() {
    return api.options(`events/participants/register/`)
              .then(response => response.data.actions.POST)
  },
  postParticipant(payload) {
    return api.post(`events/participants/register/`, payload)
              .then(response => response.data)
  },
  deleteParticipant(pId) {
    return api.delete(`events/participants/${pId}/`)
              .then(response => response.data)
  },
  putParticipant(pId, payload) {
    return api.put(`events/participants/${pId}/`, payload)
              .then(response => response.data)
  },

  fetchUserGroupScoreCards(payload) {
    return api.post(`events/participants/scorecards/`, payload)
              .then(response => response.data)
  },
  putArrow(aId, payload) {
    return api.put(`events/participants/arrows/${aId}/`, payload)
              .then(response => response.data)
  }
}
