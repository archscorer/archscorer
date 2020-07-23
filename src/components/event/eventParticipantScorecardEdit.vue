<template>
  <v-card-text>
    <v-row v-if="sc" class="flex-nowrap sc-round">
      <v-col v-for="(half, hi) in round.halves" :key="round.id + '_' + hi">
        <table>
          <thead>
            <tr>
              <th>End</th>
              <th :colspan="round.nr_of_arrows">Arrows</th>
              <th>Sum</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="end in half" :key="end.id">
              <td class="end-ord">
                {{ end.ord }}
              </td>
              <td class="end-arrow" v-for="(a, ai) in sc.arrows.filter(obj => obj.end == end.id)" :key="a.id">
                <v-text-field
                  :value="a.x ? 'X' : a.score == 0 ? 'M': a.score"
                  :loading="a.loading"
                  :background-color="a.x ? '#FFC300' : a.score === 0 ? '#9E9E9E': ''"
                  ref="arrow"
                  readonly outlined dense
                  @focus="handle_focus(end, a, ai)">
                </v-text-field>
              </td>
              <td class="end-sums text-right">
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
    <v-bottom-sheet v-model="sc_entering"
      overlay-opacity="0"
      inset
      :retain-focus="false">
      <v-row v-if="currentFocus" dense justify="center">
        <template v-for="score in sc_eval(currentFocus.end.scoring, currentFocus.end.x)">
          <v-btn :key="'score' + currentFocus.end.id + '_' + score.text"
          class="sc-btn"
          @click.prevent="enter_score(score)">{{ score.text }}</v-btn>
        </template>
      </v-row>
    </v-bottom-sheet>
  </v-card-text>
</template>

<script>
  import rankingService from '@/services/rankingService'
  export default {
    props: {
      round: Object,
    },
    data: () => ({
      currentFocus: null,
      sc_entering: false,
      arrow_inc: 0,
    }),
    watch: {
      round: function () {
        this.currentFocus = null
      }
    },
    computed: {
      sc() {
        return this.$store.getters['events/scorecardById'](this.round.sc)
      },
    },
    methods: {
      handle_focus(end, a, ai) {
        this.currentFocus = {end: end, aId: a.id}
        this.arrow_inc = end.aOrd + ai
        this.sc_entering = true

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
          this.currentFocus = false
          this.sc_entering = false
        } else {
          this.$nextTick(() => {
            let next_arrow = this.$refs.arrow[this.arrow_inc]
            next_arrow.$el.scrollIntoView()
            next_arrow.focus()
          })
        }
      },
      end_score(arrows) {
        return rankingService.sum(arrows.map(a => a.score))
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
</style>
