import axios from 'axios'
import Cookies from 'js-cookie'

const apiAuth = axios.create({
  baseURL: '/api-auth',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken')
  }
})

export default {
  postAuth(action, payload = {}) {
    return apiAuth.post(`${action}/`, payload)
  }
}
