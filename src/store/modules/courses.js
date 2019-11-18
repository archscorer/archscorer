import courseService from '@/services/courseService'

const state = {
  courses: []
}

const getters = {
  courses: state => {
    return state.courses
  }
}

const actions = {
  getCourses({ commit }, cId = '') {
    courseService.fetchCourses(cId)
    .then(courses => {
      commit('setCourses', courses)
    })
  },
  addCourse({ commit }, course) {
    courseService.postCourse(course)
    .then(course => {
      commit('addCourse', course)
    })
  },
  deleteCourse({ commit }, cId) {
    courseService.deleteCourse(cId)
    commit('deleteCourse', cId)
  }
}

const mutations = {
  setCourses(state, courses) {
    state.courses = courses
  },
  addCourse(state, course) {
    state.courses.unshift(course)
  },
  deleteCourse(state, cId) {
    state.courses = state.courses.filter(obj => obj.id !== cId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
