import api from '@/services/api'

import Cookies from 'js-cookie'

export default {
  fetchEvents(eId = '') {
    // given argument - if omitter allows to get a list of all events or
    // if defined just single events
    return api.get(`events/${eId ? eId + '/' : ''}`)
              .then(response => response.data)
  },
  postEvent(payload) {
    return api.post(`events/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  deleteEvent(eId) {
    return api.delete(`events/${eId}/`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },

  postRound(payload) {
    return api.post(`events/rounds/add/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  deleteRound(rId) {
    return api.delete(`events/rounds/${rId}/`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },

  optsParticipant() {
    return api.options(`events/participants/register/`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data.actions.POST)
  },
  postParticipant(payload) {
    return api.post(`events/participants/register/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  deleteParticipant(pId) {
    return api.delete(`events/participants/${pId}/`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },

  fetchUserGroupScoreCards(payload) {
    return api.post(`events/participants/scorecards/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  putArrow(aId, payload) {
    return api.patch(`events/participants/arrows/${aId}/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  }
}
