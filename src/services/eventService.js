import api from '@/services/api'

export default {
  fetchEvents(eId = '') {
    // Either fetch all events or a specific event
    // Here all events is by default all events from beginning from current year
    return api.get(`events/${eId ? eId + '/' : ''}`)
              .then(response => response.data)
  },
  queryEvents(attr) {
    // Query events by year
    return api.get(`events/?` + new URLSearchParams(attr).toString())
              .then(response => response.data)
  },
  postEvent(payload) {
    return api.post(`events/`, payload)
              .then(response => response.data)
  },
  delEvent(eId) {
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
  delRound(rId) {
    return api.delete(`events/rounds/${rId}/`)
              .then(response => response.data)
  },
  putRound(rId, payload) {
    return api.put(`events/rounds/${rId}/`, payload)
              .then(response => response.data)
  },

  fetchParticipant(pId) {
    return api.get(`events/participants/${pId}/`)
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

  fetchScoreCards(payload) {
    return api.post(`events/participants/scorecards/`, payload)
              .then(response => response.data)
  },
  fetchArrows(payload) {
    return api.post(`events/participants/arrows/filter/`, payload)
              .then(response => response.data)
  },
  fetchParticipants(payload) {
    return api.post(`events/participants/filter/`, payload)
              .then(response => response.data)
  },
  putArrow(aId, payload) {
    return api.put(`events/participants/arrows/${aId}/`, payload)
              .then(response => response.data)
  },
  checkScoreCard(payload) {
    return api.post(`events/participants/scorecard_check/`, payload)
              .then(response => response.data)
  },
}
