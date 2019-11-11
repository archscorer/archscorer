import api from '@/services/api'

import Cookies from 'js-cookie'

export default {
  fetchCourses(cId = '') {
    // this allows to get a list of all course or just single course
    return api.get(`courses/${cId}`)
              .then(response => response.data)
  },
  postCourse(payload) {
    return api.post(`courses/`, payload, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  },
  deleteCourse(cId) {
    return api.delete(`courses/${cId}`, { headers: {'X-CSRFToken': Cookies.get('csrftoken')} })
              .then(response => response.data)
  }
}
