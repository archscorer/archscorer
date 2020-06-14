import clubService from '@/services/clubService'
import userService from '@/services/userService'

const state = {
  clubs: []
}

const getters = {
  clubs: state => {
    return state.clubs
  },
  clubById: (state) => (id) => {
    return state.clubs.find(obj => obj.id === id)
  }
}

const actions = {
  getClubs({ commit }) {
    clubService.fetchClubs()
    .then(clubs => {
      commit('setClubs', clubs)
    })
  },
  updateClub({ commit }, cId) {
    return clubService.fetchClubs(cId)
    .then(club => {
      commit('updateClub', club)
    })
  },
  addClub({ commit }, club) {
    clubService.postClub(club)
    .then(club => {
      commit('addClub', club)
    })
  },
  putClub({ commit }, club) {
    clubService.putClub(club.id, club)
    .then(club => {
      commit('updateClub', club)
    })
  },
  deleteClub({ commit }, cId) {
    clubService.deleteClub(cId)
    commit('deleteClub', cId)
  },

  putMember({ commit }, archer) {
    if (archer.id !== null) {
      userService.putArcher(archer.id, archer)
      .then(archer => {
        commit('updateMember', archer)
      })
    } else {
      delete archer.id
      userService.postArcher(archer)
      .then(archer => {
        commit('updateMember', archer)
      })
    }
  },
  delMember({ commit }, attr) {
    userService.delArcher(attr.aId)
    commit('deleteMember', attr)
  }
}

const mutations = {
  setClubs(state, clubs) {
    state.clubs = clubs
  },
  updateClub(state, club) {
    const ci = state.clubs.findIndex(obj => obj.id === club.id);
    if (ci !== -1) {
      state.clubs.splice(ci, 1, club)
    } else {
      state.clubs.push(club)
    }
  },
  addClub(state, club) {
    state.clubs.unshift(club)
  },
  deleteClub(state, cId) {
    state.clubs = state.clubs.filter(obj => obj.id !== cId)
  },
  updateMember(state, member) {
    const ci = state.clubs.findIndex(obj => obj.id === member.club);
    if (ci !== -1) {
      const mi = state.clubs[ci].members.findIndex(obj => obj.id === member.id)
      if (mi !== -1) {
        state.clubs[ci].members.splice(mi, 1, member)
      } else {
        state.clubs[ci].members.push(member)
      }
    }
  },
  deleteMember(state, attr) {
    const ci = state.clubs.findIndex(obj => obj.id === attr.cId);
    if (ci !== -1) {
      state.clubs[ci].members = state.clubs[ci].members.filter(obj => obj.id !== attr.aId)
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
