<template>
  <v-card class="mt-5">
    <v-card-text>
      List of your past events with scores will appear here
      <v-data-table
        dense
        :mobile-breakpoint="300"
        :headers="p_table_header"
        :items="p_table"
        :items-per-page="50"
        multi-sort
      >
      <template v-slot:item.event="props">
        {{ props.item.event }} (<router-link :to="{ name: 'event', params: { 'id': props.item.eId}}">link</router-link>)
      </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState } from 'vuex'
  import rankingService from '@/services/rankingService'

  export default {
    // name: 'Series',
    components: {
    },
    data: () => ({
      //
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
        participants: state => state.events.participants,
        events: state => state.events.events,
        courses: state => state.courses.courses
      }),
      p_table_header() {
        return [
          { text: 'Event', value: 'event' },
          { text: 'Date', value: 'date', width: '120px'},
          { text: 'Round', value: 'round' },
          { text: 'Course', value: 'course'},
          { text: 'Score', value: 'score' }
        ]
      },
      p_table() {
        let p_table = []
        if (this.participants.length) {
          for (let p of this.participants) {
            let e = this.events.find(obj => obj.id === p.event)
            if (e) {
              let units = []
              for (let sc of p.scorecards) {
                let r = e.rounds.find(obj => obj.id === sc.round)
                let c = this.courses.find(obj => obj.id === r.course)
                let r_label = r.label
                let c_name = c.name
                let score = rankingService.sum(sc.arrows.map(a => a.score))
                if (c.type === 's') {
                  continue
                }
                if (c.type === 'u') {
                  let ui = units.findIndex(obj => obj.id === c.id)
                  if (ui === -1) {
                    units.push({id: c.id, score: score, round: r_label})
                    continue
                  } else {
                    r_label = units[ui].round + ' + ' + r_label
                    c_name = '2 x ' + c_name
                    score = units[ui].score + score
                    units.splice(ui, 1)
                  }
                }
                p_table.push({
                  'eId': e.id,
                  'event': e.name,
                  'date': e.date_start,
                  'round': r_label,
                  'course': c_name,
                  'score': score
                })
              }
            }
          }
        }
        return p_table.sort(function (a, b) {
          if (a.date < b.date) {
            return -1
          }
          if (a.date > b.date) {
            return 1
          }
          return 0
        })
      },
    },
    created() {
      for (let pId of this.user.archer.events) {
        if (!this.participants.find(obj => obj.id === pId)) {
          this.$store.dispatch('events/getParticipant', pId)
        }
      }
      this.$store.dispatch('events/getEvents')
    }
  }
</script>
