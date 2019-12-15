import eventService from '@/services/eventService'
/*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

const state = {
  events: [],
  participantModel: null,
  scorecards: []
}

const getters = {
  events: state => {
    return state.events
  },
  eventById: (state) => (id) => {
    return state.events.find(obj => obj.id === id)
  }
}

const actions = {
  getEvents({ commit }) {
    eventService.fetchEvents()
    .then(events => {
      commit('setEvents', events)
    })
  },
  updateEvent({ commit }, eId) {
    eventService.fetchEvents(eId)
    .then(event => {
      commit('updateEvent', event)
    })
  },
  addEvent({ commit }, event) {
    let rounds = event.rounds
    eventService.postEvent(event)
    .then(event => {
      // because of async api the commit wont wait on rounds addition
      // so when submiting round - retrieve event again and update store
      commit('addEvent', event)
      rounds.forEach(function (round, i) {
        round.ord = i + 1;  // could be there before
        round.event = event.id;
        eventService.postRound(round)
        .then(() => {
          // here we could also return round and append it to event rounds
          eventService.fetchEvents(event.id)
          .then(event => {
            commit('updateEvent', event)
          })
        }).catch(error => {
          console.log(error.response.data)
        })
      })
    })
  },
  putEvent({ commit }, attr) {
    eventService.putEvent(attr.eId, attr.event)
    .then(event => {
      commit('updateEvent', event)
    }).catch(error => {
      console.log(error.response.data)
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
      eventService.fetchEvents(participant.event)
      .then(event => {
        commit('updateEvent', event)
      })
    }).catch(error => {
      // TODO this should not be here
      console.log(error.response.data)
    })
  },
  delParticipant({ commit }, attr) {
    // TODO on django API side
    // should check
    // can delete only if user === archer
    // user === event owner
    eventService.deleteParticipant(attr.pId)
    .then(() => {
      eventService.fetchEvents(attr.eId)
      .then(event => {
        commit('updateEvent', event)
      })
    }).catch(error => {
      // TODO this should not be here
      console.log(error.response.data)
    })
  },
  putParticipant({ commit }, attr) {
    eventService.putParticipant(attr.pId, attr.participant)
    .then(participant => {
      eventService.fetchEvents(participant.event)
      .then(event => {
        commit('updateEvent', event)
      })
    }).catch(error => {
      console.log(error.response.data)
    })
  },

  getUserGroupScoreCards({ commit }, attr) {
    return eventService.fetchUserGroupScoreCards(attr)
    .then(scorecards => {
      commit('setScoreCards', scorecards)
    })
  },
  resetUserGroupScoreCards({ commit }) {
    commit('setScoreCards', [])
  },
  putArrow({ commit }, attr) {
    eventService.putArrow(attr.arrow.id, attr.arrow)
    .then(arrow => {
      commit('updateArrow', {scId: attr.scId, arrow: arrow})
    }).catch(error => {
      console.log(error.response.data)
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
    if (index !== -1) {
      state.events.splice(index, 1, event)
    } else {
      state.events.push(event)
    }
  },
  deleteEvent(state, eId) {
    state.events = state.events.filter(obj => obj.id !== eId)
  },

  setParticipantModel(state, model) {
    state.participantModel = model
  },

  setScoreCards(state, scorecards) {
    state.scorecards = scorecards
  },
  updateArrow(state, attr) {
    const sci = state.scorecards.findIndex(obj => obj.id === attr.scId)
    if (sci !== -1) {
      const ai = state.scorecards[sci].arrows.findIndex(obj => obj.id === attr.arrow.id)
      if (ai !== -1) {
        state.scorecards[sci].arrows.splice(ai, 1, attr.arrow)
      }
    }
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
