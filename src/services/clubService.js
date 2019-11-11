import api from '@/services/api'
import Cookies from 'js-cookie'

export default {
  fetchClubs(cId = '') {
    // this allows to get a list of all club or just single club
    return api.get(`clubs/${cId}`)
              .then(response => response.data)
  },
  postClub(payload) {
    return api.post(`clubs/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  deleteClub(cId) {
    return api.delete(`clubs/${cId}`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  }
}
