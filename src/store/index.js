import Vue from 'vue'
import Vuex from 'vuex'
import series from './modules/series'
import statistics from './modules/statistics'
import events from './modules/events'
import courses from './modules/courses'
import clubs from './modules/clubs'
import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    series,
    statistics,
    events,
    courses,
    clubs,
    user,
  }
})
