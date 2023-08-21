<template>
  <v-card class="mt-5">
    <v-card-title>
      Showing past rounds for {{ target_name }}
      <v-spacer />
      <archerSearch v-model="archer" />
    </v-card-title>
    <v-card-text>
      <v-row dense v-if="classifications.length">
        <v-col>
          Archer has the following classification levels:
          <v-data-table
            dense
            :mobile-breakpoint="300"
            :headers="c_table_header"
            :items="c_table"
            hide-default-footer
          >
          <template v-slot:item.level="props">
            <span class="font-weight-medium">{{ props.item.level }}</span>
          </template>
          </v-data-table>
          <small>
            <p>
              * See <a href="https://www.ifaa-archery.org/documents/rule-book/book-of-rules/" target="_blank">2021 Book of Rules</a> pages 61-62 for more information.
            </p>
          </small>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col>
            <v-switch
              v-model="filter_official"
              dense
              color="primary"
              label="show only official rounds"
              class="switch-label-size"/>
        </v-col>
        <v-col>
              <v-switch
              v-model="filter_best"
              dense
              color="primary"
              label="show only my best rounds"
              class="switch-label-size"/>
        </v-col>
      </v-row>
      <v-data-table
        dense
        :mobile-breakpoint="300"
        :headers="p_table_header"
        :items="p_table"
        :items-per-page="5"
        multi-sort
      >
      <template v-slot:item.event="props">
        <router-link :to="{ name: 'event', params: { 'id': props.item.eId }}">{{ props.item.event }}</router-link>
      </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapState } from 'vuex'

  import archerSearch from '@/components/archer/archerSearch.vue'
  import rankingService from '@/services/rankingService'

  export default {
    components: {
      archerSearch
    },
    data: () => ({
      archer: null,
      target_name: '',
      filter_official: null,
      filter_best: null,
    }),
    watch: {
      archer: function(current_archer) {
        if (current_archer && current_archer.events) {
          this.target_name = this.archer.full_name
          this.$store.dispatch('events/getParticipants', {aId: current_archer.id})
          this.$store.dispatch('user/getArcherClassification', {aId: current_archer.id, date: new Date().toISOString().slice(0, 10)})
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user,
        participants: state => state.events.participants,
        events: state => state.events.events,
        courses: state => state.courses.courses,
        classifications: state => state.user.classifications,
      }),
      p_table_header() {
        return [
          { text: 'Event', value: 'event' },
          { text: 'Date', value: 'date', width: '120px'},
          { text: 'Class', value: 'class'},
          { text: 'Format', value: 'format'},
          { text: 'Score', value: 'score'}
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
                let c_name =  c.name
                if (c.type === 's') {
                  continue
                }
                if (c.type === 'u') {
                  let ui = units.findIndex(obj => obj.id === c.id)
                  if (ui === -1) {
                    units.push({id: c.id, score: score})
                    continue
                  } else {
                    score = units[ui].score + score
                    units.splice(ui, 1)
                  }
                }
                if (!score) {
                  continue
                }
                if (this.filter_official && !e.records) {
                  continue
                }
                p_table.push({
                  'eId': e.id,
                  'event': e.name,
                  'date': e.date_start,
                  'class': rankingService.getClass(p, e.ignore_gender),
                  'format': c_name.replace(/ (Round|Unit)( (Unm|M)arked Distances)? \(.*?\)/, '$2'),
                  'score': score
                })
              }
            }
          }
        }
        if (this.filter_best) {
          // show only the top score for each class / format combination
          p_table = p_table.reduce((acc, cur) => {
            let ci = acc.findIndex(obj => obj.class === cur.class && obj.format === cur.format)
            if (ci === -1) {
              acc.push(cur)
            } else {
              if (acc[ci].score < cur.score) {
                acc[ci] = cur
              }
            }
            return acc
          }, [])
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
      c_table_header() {
        return [
          { text: 'Age Group', value: 'age_group'},
          { text: 'Style', value: 'style'},
          { text: 'Level', value: 'level'},
          { text: 'Date', value: 'date'},
          { text: 'Valid for', value: 'valid_for'},
        ]
      },
      c_table() {
        let c_table = []
        if (this.classifications.length) {
          for (let c of this.classifications) {
            c_table.push({
              'date': c.date,
              'age_group': c.age_group,
              'style': c.style,
              'level': c.level,
              'valid_for': (c.valid_for > 0 ? c.valid_for + (c.valid_for > 1 ? ' days': ' day') : 'ends today')
            })
          }
        }
        return c_table.sort(function (a, b) {
          if (a.date < b.date) {
            return 1
          }
          if (a.date > b.date) {
            return -1
          }
          return 0
        })
      }
    },
    created() {
      this.archer = this.user.archer
      this.$store.dispatch('events/getEvents')
    }
  }
</script>

<style scoped>
  .switch-label-size >>> .v-label {
    font-size: 14px;
  }
</style>