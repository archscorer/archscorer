import Vue from 'vue'
import Vuex from 'vuex'
import competitions from './modules/competitions'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    competitions
  }
})
