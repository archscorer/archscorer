<template>
  <v-container>
    <v-row v-for="(round, ri) in get_rounds()" :key="ri">
      <v-card flat v-if="round.halves">
        <v-card-title>
          {{ round.ord }}. {{ round.label }}
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col v-for="(half, hi) in round.halves" :key="hi">
              <table>
                <thead>
                  <tr>
                    <th>End</th>
                    <th :colspan="round.nr_of_arrows">Arrows</th>
                    <th>Sum</th>
                    <th>Cum</th>
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
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <template v-if="edit">
            <v-btn color="primary" text @click="edit_sc(round)">edit</v-btn>
          </template>
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
      v-model="edit_dialog"
    >
      <v-card>
        <v-card-title v-if="edit_round">
          {{ edit_round.ord }}. {{ edit_round.label }}
        </v-card-title>
        <eventParticipantScorecardEdit :round="edit_round"/>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="edit_dialog = false">Close</v-btn>
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
  import {mapState} from 'vuex'

  function sum(arr) {
    return arr.reduce((sum, x) => sum + x);
  }

  export default {

    components: {
      eventParticipantScorecardEdit
    },
    props: {
      participant: Object,
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
    },
    methods: {
      get_rounds() {
        // round object for scorecard, return list of modified round objects
        let rounds = [...this.rounds]
        return rounds.map(r => {
          let sc = this.participant.scorecards.find(obj => obj.round === r.id)
          if (!sc) {
            return r
          }
          let course = this.courses.find(obj => obj.id === r.course)
          // in some cases course is not loaded, probably related to dev hotreload
          // but nevertheless, if couse is not loaded -- request it from backend
          if (!course) {
            this.$store.dispatch('courses/getCourses', r.course)
            return null
          }
          let ends = course.ends
          // max number of arrows for round ends
          let aNr = 0
          let cum = 0
          let halves = []
          let sc_ends = []
          for (let e of ends) {
            // end arrows
            let eAr = sc.arrows.filter(obj => obj.end === e.id)
            let eSum = 0
            if (eAr !== null) {
              eSum = sum( eAr.map(a => a.score ))
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
          return Object.assign({}, r, {nr_of_arrows: aNr, halves: halves, sc: sc})
        })
      },
      edit_sc(r) {
        let course = this.courses.find(obj => obj.id === r.course)
        if (!course) {
          // in case courses have not been leaded
          this.$store.dispatch('courses/getCourses', r.course)
        }
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
        this.edit_dialog = true
      },
      get_scorecards(rId) {
        this.$store.dispatch('events/resetScoreCardsUserGroup')
        this.scorecards_loading = true
        // ask for scorecards. Creating new ones will take time, therefore catch
        // timeout and let user know of it
        // NOTE currently UserGroup and Admin modules are the same, but subject to alteration in the future
        this.$store.dispatch('events/getScoreCardsAdmin', {eId: this.participant.event,
                                                           rId: rId,
                                                           group: this.participant.group,
                                                           group_target: this.participant.group_target})
        .then(() => {
          this.scorecards_loading = false
          this.$store.dispatch('events/updateEvent', this.participant.event)
          this.snack = true
          this.snackColor = 'info'
          this.snackText = 'Reopen scorecard dialog for the changes to take effect!'
        }).catch(err => {
          this.scorecards_loading = false
          if (err.code === 'ECONNABORTED') {
            this.snack = true
            this.snackColor = 'error'
            this.snackText = 'Operation timed out. Try again in few seconds.'
          }
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
  th {
    padding: 0 5px;
  }
</style>
