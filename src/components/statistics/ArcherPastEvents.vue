<template>
  <v-card class="mt-5">
    <v-card-title>
      Showing past rounds for {{ target_name }}
      <v-spacer />
      <archerSearch v-model="archer" />
    </v-card-title>
    <v-card-text>
      <v-data-table
        dense
        :mobile-breakpoint="300"
        :headers="p_table_header"
        :items="p_table"
        :items-per-page="5"
        multi-sort
      >
      <template v-slot:item.event="props">
        {{ props.item.event }} (<router-link :to="{ name: 'event', params: { 'id': props.item.eId }}">link</router-link>)
      </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapState } from 'vuex'

  import archerSearch from '@/components/archer/archerSearch.vue'

  export default {
    components: {
      archerSearch
    },
    data: () => ({
      archer: null,
      target_name: '',
    }),
    watch: {
      archer: function(current_archer) {
        if (current_archer && current_archer.events) {
          this.target_name = this.archer.full_name
          this.$store.dispatch('events/clearParticipants')
          for (let pId of current_archer.events) {
            if (!this.participants.find(obj => obj.id === pId)) {
              this.$store.dispatch('events/getParticipant', pId)
            }
          }
        }
      }
    },
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
                let score = sc.score
                let [r_label, c_name] = [r.label, c.name]
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
                if (!score) {
                  continue
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
            return 1
          }
          if (a.date > b.date) {
            return -1
          }
          return 0
        })
      },
    },
    created() {
      this.archer = this.user.archer
      this.$store.dispatch('events/getEvents')
    }
  }
</script>
