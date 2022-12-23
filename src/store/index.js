import { createStore } from 'vuex'
import series from './modules/series'
import statistics from './modules/statistics'
import events from './modules/events'
import courses from './modules/courses'
import clubs from './modules/clubs'
import user from './modules/user'

export default createStore({
  modules: {
    series,
    statistics,
    events,
    courses,
    clubs,
    user,
  }
})
