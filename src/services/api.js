import axios from 'axios'

export default axios.create({
  baseURL: '/api',
  withCredentials: true,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  }
})
