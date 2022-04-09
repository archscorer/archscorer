import eventService from '@/services/eventService'
/*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

const state = {
  events: [],
  participantModel: null,
  scorecards: [],
  participants: [],
}

const getters = {
  events: state => {
    return state.events
  },
  eventById: (state) => (id) => {
    return state.events.find(obj => obj.id === id)
  },
  eventParticipantById: (state) => (eId, pId) => {
    return state.events.find(obj => obj.id === eId)
                .participants.find(obj => obj.id === pId)
  },
  scorecards: state => {
    return state.scorecards
  },
  scorecardById: (state) => (id) => {
    return state.scorecards.find(obj => obj.id === id)
  },
  participants: state => {
    return state.participants
  },
  participantModel: state => {
    return state.participantModel
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
    // TODO attr here is wierd style, event alone should be enough as it always
    // should have .id
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
  getParticipant({ commit }, pId) {
    eventService.fetchParticipant(pId)
    .then(participant => {
      commit('updateParticipant', participant)
    })
  },
  clearParticipants({ commit }) {
    commit('clearParticipants')
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
  getScoreCards({ commit }, attr) {
    return eventService.fetchScoreCards(attr)
    .then(scorecards => {
      commit('setScoreCards', scorecards)
    })
  },
  resetScoreCards({ commit }) {
    commit('setScoreCards', [])
  },
  putArrow({ dispatch, commit }, attr) {
    // commit to be submitted arrow to local store
    commit('updateArrow', {scId: attr.scId, arrow: attr.arrow})
    eventService.putArrow(attr.arrow.id, attr.arrow)
    .then(arrow => {
      commit('updateArrow', {scId: attr.scId, arrow: arrow})
    }).catch(error => {
      // server returned error (most likely timeout or some kind of throttle? try again)
      dispatch('putArrow', attr)
      console.log(error.response ? error.response.data : error)
    })
  },
  checkScoreCard({ commit }, attr) {
    eventService.checkScoreCard(attr)
    .then(response => {
      eventService.fetchEvents(attr.eId)
      .then(event => {
        commit('updateEvent', event)
      })
    }).catch(error => {
      console.log(error.response ? error.response.data : error)
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
  updateParticipant(state, participant) {
    const index = state.participants.findIndex(obj => obj.id === participant.id);
    if (index !== -1) {
      state.participants.splice(index, 1, participant)
    } else {
      state.participants.push(participant)
    }
  },
  clearParticipants(state) {
    state.participants = []
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
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
