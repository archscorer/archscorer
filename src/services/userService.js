import api from '@/services/api'

import axios from 'axios'
import Cookies from 'js-cookie'

const apiAuth = axios.create({
  timeout: 5000,
  headers: {
    'Content-Type': 'multipart/form-data'
  },
  withCredentials: true
})

export default {
  postAuth(action, next = '', payload = {}) {
    return apiAuth.post(`/api-auth/${action}/${next}`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
                  .then(response => {
                    return response.data
                  })
  },
  getUser() {
    return api.get(`user`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  getArcher() {
    return api.get(`archer`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  postArcher(payload) {
    return api.post(`archer`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  }
}
