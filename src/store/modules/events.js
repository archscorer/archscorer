import eventService from '@/services/eventService'

const state = {
  events: []
}

const getters = {
  events: state => {
    return state.events
  }
}

const actions = {
  getEvents({ commit }) {
    eventService.fetchEvents()
    .then(events => {
      commit('setEvents', events)
    })
  },
  addEvent({ commit }, event) {
    let rounds = event.rounds
    eventService.postEvent(event)
    .then(event => {
      // because of async api the commit wont wait on rounds addition
      // se when submiting round - retrieve event again and update store
      commit('addEvent', event)
      rounds.forEach(function (round, i) {
        round.ord = i + 1;  // could be there before
        round.is_open = true;  // could be there before
        round.event = event.id;
        eventService.postRound(round)
        .then(() => {
          // here we could also return round and append it to event rounds
          eventService.fetchEvents(event.id)
          .then(event => {
            commit('updateEvent', event)
          })
        })
      })
    })
  },
  deleteEvent({ commit }, compId) {
    eventService.deleteEvent(compId)
    .then(() => {
      commit('deleteEvent', compId)      
    })
  }
}

const mutations = {
  setEvents(state, events) {
    state.events = events
  },
  addEvent(state, event) {
    state.events.unshift(event)
  },
  updateEvent(state, event) {
    const index = state.events.findIndex(obj => obj.id === event.id);
    if (index !== -1)state.events.splice(index, 1, event)
  },
  deleteEvent(state, compId) {
    state.events = state.events.filter(obj => obj.id !== compId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
