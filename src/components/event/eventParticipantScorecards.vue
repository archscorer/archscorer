<template>
  <v-container>
    <v-row v-for="(round, ri) in get_rounds()" :key="ri">
      <v-card flat v-if="round.halves">
        <v-card-title>
          {{ round.ord }}. {{ round.label }}
        </v-card-title>
        <v-card-text>
          <v-row class="flex-nowrap sc-round">
            <v-col v-for="(half, hi) in round.halves" :key="hi">
              <table>
                <thead>
                  <tr>
                    <th>End</th>
                    <th :colspan="round.nr_of_arrows">Arrows</th>
                    <th>Sum</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="end in half" :key="end.id">
                    <td class="end-ord">
                      {{ end.ord }}
                    </td>
                    <td class="end-arrow" v-for="a in end.nr_of_arrows" :key="'a' + a">
                      <template v-if="end.arrows !== null">
                        <!-- for very wierd reason 'a' is starting from 1, not 0 like within <script> -->
                        {{ end.arrows[a-1].x ? 'X' : end.arrows[a-1].score === 0 ? 'M' : end.arrows[a-1].score }}
                      </template>
                    </td>
                    <!-- some ends might have less arrows, handle the alignment here -->
                    <template v-if="end.nr_of_arrows < round.nr_of_arrows">
                      <td v-for="a in round.nr_of_arrows - end.nr_of_arrows" :key="'empty' + a">
                      </td>
                    </template>
                    <td class="end-sums text-right">
                      {{ end.sum }}
                    </td>
                    <td class="end-sums text-right">
                      {{ end.cum }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="text-no-wrap text-subtitle-1">
              Stats:
            </v-col>
            <v-col>
              <table>
                <thead>
                  <tr>
                    <th v-for="(text, ti) in Object.keys(round.stats)" :key="'sth' + ti">{{ text === '0' ? 'M' : text === 'null' ? 'N/A' : text }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="end-arrow" v-for="(val, vi) in Object.values(round.stats)" :key="'sv' + vi">{{ val }}</td>
                  </tr>
                </tbody>
              </table>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions v-if="edit">
          <v-spacer />
          <v-btn color="primary" text @click="edit_sc(round)">edit</v-btn>
        </v-card-actions>
      </v-card>
      <template v-else>
        <v-alert type="info" prominent v-if="edit">
          <v-row align="center">
            <v-col class="grow">{{participant.archer.full_name}}({{ participant.class }}) has no scorecard for {{ round.ord }}. {{ round.label }} round!</v-col>
            <v-col class="shrink" ><v-btn @click="get_scorecards(round.id)">Add</v-btn></v-col>
          </v-row>
        </v-alert>
      </template>
    </v-row>
    <v-dialog
      max-width="650px"
      v-model="edit_dialog"
    >
      <v-card>
        <v-card-title v-if="edit_round">
          {{ edit_round.ord }}. {{ edit_round.label }}
        </v-card-title>
        <v-card-subtitle>{{ participant.archer.full_name }}</v-card-subtitle>
        <eventParticipantScorecardEdit :round="edit_round"/>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="close_edit()">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snack" :timeout="5000" :color="snackColor">
      {{ snackText }}
      <v-btn text @click="snack = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

  import eventParticipantScorecardEdit from '@/components/event/eventParticipantScorecardEdit.vue'
  import { mapState, mapGetters, mapActions } from 'vuex'

  function sum(arr) {
    return arr.reduce((sum, x) => sum + x);
  }

  export default {

    components: {
      eventParticipantScorecardEdit
    },
    props: {
      eId: Number,
      pId: Number,
      rounds: Array,
      edit: Boolean,
    },
    data: () => ({
      edit_dialog: false,
      edit_round: null,
      scorecards_loading: false,

      snack: false,
      snackText: '',
      snackColor: ''
    }),
    computed: {
      ...mapState({
        courses: state => state.courses.courses,
      }),
      ...mapGetters('events', [
        'eventParticipantById',
        'scorecardById'
      ]),
      participant() {
        return this.eventParticipantById(this.eId, this.pId)
      }
    },
    methods: {
      ...mapActions('events', [
        'getScoreCards',
        'updateEvent'
      ]),
      get_rounds() {
        // round object for scorecard, return list of modified round objects
        let rounds = [...this.rounds]
        return rounds.map(r => {
          let sc = this.participant.scorecards.find(obj => obj.round === r.id)
          if (!sc) {
            return r
          }
          let course = this.courses.find(obj => obj.id === r.course)
          let ends = course.ends
          // max number of arrows for round ends
          let aNr = 0
          let cum = 0
          let halves = []
          let sc_ends = []
          let stats = {}
          for (let e of ends) {
            // end arrows
            let eAr = sc.arrows.filter(obj => obj.end === e.id)
            let eSum = 0
            if (eAr !== null) {
              eSum = sum( eAr.map(a => {
                if (a.score in stats) {
                  stats[a.score] += 1
                } else {
                  stats[a.score] = 1
                }
                if (a.x) {
                  if ('x' in stats) {
                    stats.x += 1
                  } else {
                    stats.x = 1
                  }
                }
                return a.score
              }))
            }
            // update max number
            aNr = e.nr_of_arrows > aNr ? e.nr_of_arrows : aNr
            cum += eSum
            sc_ends.push(Object.assign({}, e, {arrows: eAr, sum: eSum, cum: cum}))
            if (course.halves === true && e.ord === course.ends.length / 2) {
              halves.push([...sc_ends])
              sc_ends = []
            }
          }
          halves.push(sc_ends)
          return Object.assign({}, r, {nr_of_arrows: aNr, halves: halves, sc: sc.id, stats: stats})
        })
      },
      edit_sc(r) {
        let course = this.courses.find(obj => obj.id === r.course)
        let ends = course.ends
        let aOrd = 0
        let halves = []
        let sc_ends = []
        for (let e of ends) {
          // update max number
          sc_ends.push(Object.assign({}, e, {aOrd: aOrd}))
          if (course.halves === true && e.ord === course.ends.length / 2) {
            halves.push([...sc_ends])
            sc_ends = []
          }
          aOrd += e.nr_of_arrows
        }
        halves.push(sc_ends)
        this.edit_round = Object.assign({}, r, {halves: halves})
        let sc = this.scorecardById(r.sc)
        if (!sc) {
          this.getScoreCards({eId: this.participant.event,
                                   rId: r.id,
                                   group: this.participant.group,
                                   group_target: this.participant.group_target})
        }
        this.edit_dialog = true
      },
      get_scorecards(rId) {
        this.getScoreCards({eId: this.participant.event,
                                 rId: rId,
                                 group: this.participant.group,
                                 group_target: this.participant.group_target})
                   .then(() => {
                     this.updateEvent(this.participant.event)
                   })
      },
      close_edit() {
        this.updateEvent(this.participant.event).then(() => {
          this.edit_dialog = false
        })
      }
    },
  }
</script>

<style scoped>
  .end-ord {
    padding: 2px 4px;
  }
  .end-sums {
    padding: 2px 4px;
  }
  .end-arrow {
    padding: 2px 4px;
    border: solid 1px lightgray;
    font-weight: 300;
    text-align: center;
    min-width: 24px;
    height: 28px;
  }
  .sc-round {
    overflow: auto;
  }
  th {
    padding: 0 5px;
  }
</style>
