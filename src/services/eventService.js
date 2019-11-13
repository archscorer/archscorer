import api from '@/services/api'

import Cookies from 'js-cookie'

export default {
  fetchEvents(compId = '') {
    // given argument - if omitter allows to get a list of all events or
    // if defined just single events
    return api.get(`events/${compId}`)
              .then(response => response.data)
  },
  postEvent(payload) {
    return api.post(`events/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  deleteEvent(compId) {
    return api.delete(`events/${compId}`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  postRound(payload) {
    return api.post(`rounds/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  deleteRound(rId) {
    return api.delete(`rounds/${rId}`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  optsParticipant() {
    return api.options(`participants/register/`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data.actions.POST)
  },
  postParticipant(payload) {
    return api.post(`participants/register/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  deleteParticipant(pId) {
    return api.delete(`participants/${pId}`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  }
}
