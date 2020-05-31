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
    return eventService.fetchEvents(eId)
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
          // TODO if different server calls time differently -- the last call
          // might not return correct (latest) event instance?
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
  delEvent({ commit }, eId) {
    eventService.delEvent(eId)
    .then(() => {
      commit('delEvent', eId)
    })
  },

  addRound({ commit }, round) {
    eventService.postRound(round)
    .then(round => {
      commit('updateRound', round)
    })
  },
  putRound({ commit }, round) {
    eventService.putRound(round.id, round)
    .then(round => {
      commit('updateRound', round)
    })
  },
  delRound({ commit }, attr) {
    eventService.delRound(attr.rId)
    .then(() => {
      commit('delRound', attr)
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
    return eventService.putParticipant(attr.pId, attr.participant)
    .then(participant => {
      eventService.fetchEvents(participant.event)
      .then(event => {
        commit('updateEvent', event)
      })
    }).catch(error => {
      console.log(error.response.data)
    })
  },

  getScoreCardsUserGroup({ commit }, attr) {
    return eventService.fetchScoreCards(attr)
    .then(scorecards => {
      commit('setScoreCards', scorecards)
    })
  },
  resetScoreCardsUserGroup({ commit }) {
    commit('setScoreCards', [])
  },
  getScoreCardsAdmin({ commit }, attr) {
    // this could become useful for third party scoring i.e. official scorer or admin in case of shootoff for example
    return eventService.fetchScoreCards(attr)
    .then(scorecards => {
      commit('setScoreCards', scorecards)
    })
  },

  putArrow({ commit }, attr) {
    // commit to be submitted arrow to local store
    commit('updateArrow', {scId: attr.scId, arrow: attr.arrow})
    eventService.putArrow(attr.arrow.id, attr.arrow)
    .then(arrow => {
      commit('updateArrow', {scId: attr.scId, arrow: arrow})
    }).catch(error => {
      // server returned error, store error state to store
      let arrow = attr.arrow
      arrow.error = true
      arrow.loading = false
      commit('updateArrow', {scId: attr.scId, arrow: arrow})
      console.log(error.response.data)
    })
  },
  putArrowEdit({ commit }, attr) {
    // commit to be submitted arrow to local store
    commit('updateArrowEdit', {eId: attr.eId, pId: attr.pId, scId: attr.scId, arrow: attr.arrow})
    eventService.putArrow(attr.arrow.id, attr.arrow)
    .then(arrow => {
      commit('updateArrowEdit', {eId: attr.eId, pId: attr.pId, scId: attr.scId, arrow: arrow})
    }).catch(error => {
      // server returned error, store error state to store
      let arrow = attr.arrow
      arrow.error = true
      arrow.loading = false
      commit('updateArrowEdit', {eId: attr.eId, pId: attr.pId, scId: attr.scId, arrow: arrow})
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
  delEvent(state, eId) {
    state.events = state.events.filter(obj => obj.id !== eId)
  },

  updateRound(state, round) {
    const ei = state.events.findIndex(obj => obj.id === round.event)
    if (ei !== -1) {
      const index = state.events[ei].rounds.findIndex(obj => obj.id === round.id);
      if (index !== -1) {
        state.events[ei].rounds.splice(index, 1, round)
      } else {
        state.events[ei].rounds.push(round)
      }
    }
  },
  delRound(state, attr) {
    const ei = state.events.findIndex(obj => obj.id === attr.eId)
    if (ei !== -1) {
      const ri = state.events[ei].rounds.findIndex(obj => obj.id === attr.rId)
      if (ri !== -1) {
        state.events[ei].rounds.splice(ri, 1)
      }
    }
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
  updateArrowEdit(state, attr) {
    const ei = state.events.findIndex(obj => obj.id === attr.eId)
    if (ei !== -1) {
      const pi = state.events[ei].participants.findIndex(obj => obj.id === attr.pId)
      if (pi !== -1) {
        const sci = state.events[ei].participants[pi].scorecards.findIndex(obj => obj.id === attr.scId)
        if (sci !== -1) {
          const ai = state.events[ei].participants[pi].scorecards[sci].arrows.findIndex(obj => obj.id === attr.arrow.id)
          if (ai !== -1) {
            state.events[ei].participants[pi].scorecards[sci].arrows.splice(ai, 1, attr.arrow)
          }
        }
      }
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
