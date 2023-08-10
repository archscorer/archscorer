<template>
  <v-dialog max-width="650px" v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" text @click="edit_sc(round)" v-on="on">edit</v-btn>
    </template>
    <v-card class="pb-16" v-if="edit_round">
      <v-card-title>
        {{ edit_round.ord }}. {{ edit_round.label }}
      </v-card-title>
      <v-card-subtitle>{{ participant.full_name }}</v-card-subtitle>
      <v-card-text>
        <v-row v-if="sc" class="flex-nowrap sc-round">
          <v-col v-for="(half, hi) in edit_round.halves" :key="edit_round.id + '_' + hi">
            <table>
              <thead>
                <tr>
                  <th>End</th>
                  <th :colspan="edit_round.nr_of_arrows">Arrows</th>
                  <th>Sum</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="end in half" :key="end.id">
                  <td class="end-ord" @click.prevent="currentFocus = null">
                    {{ end.ord }}
                  </td>
                  <td class="end-arrow" v-for="(a, ai) in sc.arrows.filter(obj => obj.end == end.id)" :key="a.id">
                    <v-text-field
                      :value="a.x ? 'X' : a.score == 0 ? 'M': a.score"
                      :loading="a.loading"
                      :color="a.color"
                      :background-color="a.x ? '#FFC300' : a.score === 0 ? '#9E9E9E': ''"
                      ref="arrow"
                      readonly outlined dense
                      @focus="handle_focus(end, a, ai)"
                      @keyup="enter_score_numpad($event)">
                    </v-text-field>
                  </td>
                  <td class="end-sums text-right" @click.prevent="currentFocus = null">
                    {{ end_score(sc.arrows.filter(obj => obj.end == end.id)) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </v-col>
        </v-row>
        <v-sheet v-else class="text-center py-10">
          <v-progress-circular indeterminate size="64" color="secondary"></v-progress-circular>
        </v-sheet>
        <v-sheet class="sc-entering">
          <v-row v-if="currentFocus" dense justify="center">
            <v-col class="text-center">
              <v-btn v-for="score in sc_eval(currentFocus.end.scoring, currentFocus.end.x)"
              :key="'score' + currentFocus.end.id + '_' + score.text"
              class="sc-btn"
              @click.prevent="enter_score(score)">{{ score.text }}</v-btn>
            </v-col>
          </v-row>
        </v-sheet>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="close_edit()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<script>
  import rankingService from '@/services/rankingService'
  import { mapState, mapGetters, mapActions } from 'vuex'

  export default {
    props: {
      participant: Object,
      round: Object,
    },
    data: () => ({
      dialog: false,
      edit_round: null,
      currentFocus: null,
      arrow_inc: 0,
    }),
    watch: {
      round: function () {
        this.currentFocus = null
      }
    },
    computed: {
      ...mapState({
        courses: state => state.courses.courses,
      }),
      ...mapGetters('events', [
        'eventParticipantById',
        'scorecardById'
      ]),
      sc() {
        return this.$store.getters['events/scorecardById'](this.round.sc)
      },
    },
    methods: {
      ...mapActions('events', [
        'getScoreCards',
      ]),
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
                              session: this.participant.session,
                              target: this.participant.target})
        }
      },
      handle_focus(end, a, ai) {
        this.currentFocus = {end: end, aId: a.id}
        this.arrow_inc = end.aOrd + ai
      },
      sc_eval(arr, x) {
        let scores_choices = eval(arr).map(function(v) {
          return {'text': v, 'value': v}
        })
        if (x) scores_choices.unshift({'text': 'X', 'value': scores_choices[0].value})
        scores_choices.push({'text': 'M', 'value': 0})
        return scores_choices
      },
      enter_score(sc) {
        if (this.currentFocus) {
          let arrow = this.sc.arrows.find(obj => obj.id === this.currentFocus.aId)
          arrow.x = sc.text === 'X' ? true : false
          arrow.score = sc.value
          arrow.loading = 'warning'
          this.$store.dispatch('events/putArrow', {scId: this.sc.id, arrow: arrow})
          this.$refs.arrow[this.arrow_inc].blur()
        } else {
          this.arrow_inc = this.$refs.arrow.length + 1
        }
        this.arrow_inc++
        if (this.arrow_inc >= this.$refs.arrow.length) {
          // so that no scores would be changed if clicked again
          this.currentFocus = null
        } else {
          this.$nextTick(() => {
            let next_arrow = this.$refs.arrow[this.arrow_inc]
            next_arrow.$el.scrollIntoView()
            next_arrow.focus()
          })
        }
      },
      enter_score_numpad(e) {
        if (this.currentFocus) {
          let score_ops = eval(this.currentFocus.end.scoring)
          let arrow = this.sc.arrows.find(obj => obj.id === this.currentFocus.aId)
          if (e.key === 'Backspace') {
            if (arrow.score) {
              arrow.x = false
              if (arrow.score > 9) {
                arrow.score = Math.floor(arrow.score / 10)
              } else {
                arrow.score = null
              }
              arrow.color = 'warning'
            }
          } else if (e.key === 'Enter') {
            if (arrow.score === 'x' && this.currentFocus.end.x) {
              this.enter_score({'text': 'X', 'value': score_ops[0]})
            } else if (score_ops.includes(parseInt(arrow.score))) {
              this.enter_score({'text': arrow.score, 'value': parseInt(arrow.score)})
            } else if (arrow.score === '0' || arrow.score === 'm') {
              this.enter_score({'text': 'M', 'value': 0})
            } else {
              arrow.color = 'error'
              /* should also rise error or snackbar to notify of the issue */
            }
          } else if (e.key === 'Tab') {
            /* do nothing, tab is for */
          } else {
            if (arrow.score) {
              arrow.score += e.key
            } else {
              arrow.score = e.key
            }
            arrow.color = 'warning'
          }
        }
      },
      end_score(arrows) {
        return rankingService.sum(arrows.map(a => a.score ? parseInt(a.score) : null))
      },
      close_edit() {
        this.$emit('update')
        this.dialog = false
      }
    },
  }
</script>

<style scoped>
  .v-input >>> .v-text-field__details {
    display: none;
  }
  .v-text-field--outlined.v-input--dense >>> .v-input__control .v-input__slot {
    min-height: 30px;
    max-height: 30px;
    padding: 0 5px;
  }
  .v-input >>> input {
    max-width: 100%;
    width: 100%;
    text-align: center;
    margin: 0;
  }
  .text-cum {
    margin-top: 0.2rem;
    white-space: nowrap;
  }
  .end-arrow {
    max-width: 37px;
    min-width: 37px;
    max-height: 30px;
  }
  .sc-btn {
    margin-bottom: 3px;
    margin-right: 3px;
    min-width: 67px!important;
    min-height: 58px;
  }
  .sc-round {
    overflow: auto;
  }
  th {
    padding: 0 5px;
  }
  .sc-entering {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-width: 450px;
    margin: 0 auto;
    z-index: 99;
  }
</style>
