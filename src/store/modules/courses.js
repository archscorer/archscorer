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
    return courseService.fetchCourses(cId)
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
    if (Array.isArray(courses)) {
      state.courses = courses
    } else {
      // courses is not an array, it must be object ?
      let id = courses.id ? courses.id : false
      if (id) {
        let index = state.courses.findIndex(obj => obj.id === id);
        if (index !== -1) {
          state.courses.splice(index, 1, courses)
        } else {
          state.courses.push(courses)
        }
      } // do nothing
    }
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
