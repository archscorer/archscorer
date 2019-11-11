import eventService from '@/services/eventService'
/*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

const state = {
  events: [],
  participantModel: null
}

const getters = {
  events: state => {
    return state.events
  }
}

const actions = {
  getEvents({ commit }, eId = '') {
    eventService.fetchEvents(eId)
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
  deleteEvent({ commit }, eId) {
    eventService.deleteEvent(eId)
    .then(() => {
      commit('deleteEvent', eId)
    })
  },
  getParticipantOpts({ commit }) {
    eventService.optsParticipant()
    .then(model => {
      commit('setParticipantModel', model)
    })
  },
  addParticipant({ commit }, participant) {
    eventService.postParticipant(participant)
    .then(participant => {
      eventService.fetchEvents(participant.event.id)
      .then(event => {
        commit('updateEvent', event)
      })
    }).catch(error => {
      // TODO this should not be here
      console.log(error.response.data)
    })
  },
  delParticipant({ commit }, eId, pId) {
    // TODO
    // should check
    // can delete only if user === archer
    // user === competition owner
    eventService.deleteParticipant(pId)
    .then(() => {
      eventService.fetchEvents(eId)
      .then(event => {
        commit('updateEvent', event)
      })
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
    if (index !== -1) state.events.splice(index, 1, event)
  },
  deleteEvent(state, eId) {
    state.events = state.events.filter(obj => obj.id !== eId)
  },
  setParticipantModel(state, model) {
    state.participantModel = model
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
