<template>
  <v-dialog v-model="dialog" max-width="650px">
    <template v-slot:activator="{ on }">
      <v-btn icon @click="get_participant()" small v-on="on">
        <v-icon size="16">mdi-book-open-outline</v-icon>
      </v-btn>
    </template>
    <v-card v-if="participant !== null">
      <v-toolbar flat>
        <v-toolbar-title>{{ participant.full_name }} {{ participant.class}}</v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="dialog = false">
            <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-subtitle>{{ event.name }}</v-card-subtitle>
      <v-card-text>
        <v-overlay
          absolute="absolute"
          :value="loading"
        >
          <v-progress-circular
            :size="50"
            color="secondary"
            indeterminate/>
        </v-overlay>
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
                          <template v-if="end.arrows.length">
                            <!-- for very wierd reason 'a' is starting from 1, not 0 like within <script> -->
                            {{ end.arrows[a-1].x ? 'X' : end.arrows[a-1].p === 0 ? 'M' : end.arrows[a-1].p }}
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
              <eventParticipantScorecardEdit :participant="participant" :round="round" @update="update_participant_sc"/>
              <v-btn color="green" text v-if="!round.checked" @click="check_scorecard({eId: eId, scId: round.sc})">sign</v-btn>
            </v-card-actions>
          </v-card>
          <template v-else>
            <v-alert type="info" prominent v-if="edit">
              <v-row align="center">
                <v-col class="grow">{{participant.full_name}} has no scorecard for {{ round.ord }}. {{ round.label }} round!</v-col>
                <v-col class="shrink" ><v-btn @click="get_scorecards(round.id)">Add</v-btn></v-col>
              </v-row>
            </v-alert>
          </template>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer/>
        <v-btn text @click="dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

  import eventParticipantScorecardEdit from '@/components/event/eventParticipantScorecardEdit.vue'
  import { mapState, mapGetters, mapActions } from 'vuex'

  function sum(arr) {
    return Array.isArray(arr) && arr.length ? arr.reduce((sum, x) => sum + x) : null;
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
      dialog: false,
      loading: false,
      participant: null,
    }),
    computed: {
      ...mapState({
        courses: state => state.courses.courses,
        arrows: state => state.events.arrows
      }),
      ...mapGetters('events', [
        'eventParticipantById',
        'scorecardById'
      ]),
      event() {
        return this.$store.getters['events/eventById'](this.eId)
      },
    },
    methods: {
      ...mapActions('events', [
        'getScoreCards',
        'getArrows',
        'checkScoreCard',
        'updateEvent'
      ]),
      update_participant_sc() {
        this.loading = true
        this.updateEvent(this.participant.event).then(() => {
          this.get_participant()
          this.loading = false
        })
      },
      check_scorecard(attr) {
        this.checkScoreCard(attr).then(() => {
          this.update_participant_sc()
        })
      },
      get_scorecards(rId) {
        this.getScoreCards({eId: this.participant.event,
                            rId: rId,
                            session: this.participant.session,
                            target: this.participant.target})
                   .then(() => {
                     this.update_participant_sc()
                   })
      },
      get_participant() {
        this.participant = this.eventParticipantById(this.eId, this.pId)
        this.getArrows({'pId': this.pId})
      },
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
          let [h, t] = [0, 0]
          for (let e of ends) {
            // end arrows
            let eAr = this.arrows.filter(obj => obj.sc === sc.id)
                                 .filter(obj => obj.e === e.id)
            let eSum = 0
            if (eAr !== null) {
              eSum = sum( eAr.map(a => {
                if (a.p in stats) {
                  stats[a.p] += 1
                } else {
                  stats[a.p] = 1
                }
                if (a.x) {
                  if ('x' in stats) {
                    stats.x += 1
                  } else {
                    stats.x = 1
                  }
                }
                // hit percentage
                if (a.p !== null) {
                  if (a.p !== 0) {
                    h += 1
                  }
                  t += 1
                }
                return a.p
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
          stats['%'] = (t !== 0 ? (h/t * 100).toFixed(1) : null)
          halves.push(sc_ends)
          return Object.assign({}, r, {nr_of_arrows: aNr, halves: halves, sc: sc.id, checked: sc.checked, stats: stats})
        })
      },
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
