<template>
  <v-card-text>
    <v-row>
      <v-col v-for="(half, hi) in round.halves" :key="round.id + '_' + hi">
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
              <td class="end-arrow" v-for="(a, ai) in round.sc.arrows.filter(obj => obj.end == end.id)" :key="a.id">
                <v-select
                  v-model="a.score"
                  :items="sc_eval(end.scoring)"
                  append-icon=""
                  :loading="a.loading"
                  :error="a.error"
                  :background-color="a.x ? '#FFC300' : a.score === 0 ? '#9E9E9E': ''"
                  ref="arrow"
                  readonly outlined dense
                  @focus="currentFocus = {end: end, aId: a.id}; arrow_inc = end.aOrd + ai">
                </v-select>
              </td>
              <td class="end-sums text-right">
                <!-- TODO -->
              </td>
              <td class="end-sums text-right">
                <!-- TODO -->
              </td>
            </tr>
          </tbody>
        </table>
      </v-col>
    </v-row>
    <v-row v-if="currentFocus">
      <template v-for="score in sc_eval(currentFocus.end.scoring, currentFocus.end.x)">
        <v-btn :key="'score' + currentFocus.end.id + '_' + score.text"
        class="sc-btn"
        @click.prevent="enter_score(score)">{{ score.text }}</v-btn>
      </template>
    </v-row>
  </v-card-text>
</template>

<script>
  export default {

    props: {
      round: Object,
    },
    data: () => ({
      currentEnd: null,
      currentFocus: null,
      arrow_inc: 0,
    }),
    methods: {
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
          let arrow = this.round.sc.arrows.find(obj => obj.id === this.currentFocus.aId)
          arrow.x = sc.text === 'X' ? true : false
          arrow.score = sc.value
          arrow.loading = 'warning'
          this.$store.dispatch('events/putArrowEdit', {eId: parseInt(this.$route.params.id),
                                                       pId: this.round.sc.participant,
                                                       scId: this.round.sc.id,
                                                       arrow: arrow})
          this.$refs.arrow[this.arrow_inc].blur()
        } else {
          this.arrow_inc = this.$refs.arrow.length + 1
        }
        this.arrow_inc++
        if (this.arrow_inc >= this.$refs.arrow.length + 2) {
          this.snackText = "Focus on arrow you want to update or go to next end!"
          this.snack = true
        } else if (this.arrow_inc >= this.$refs.arrow.length) {
          // so that no scores would be changed if clicked again
          this.currentFocus = false
          // we have finished all arrows, focus on arrow key to next page
          // this.$nextTick(() => this.$refs.next_end.$refs.link.focus())
        } else {
          this.$nextTick(() => {
            this.$refs.arrow[this.arrow_inc].focus()
          })
        }
      },
    },
  }
</script>

<style scoped>
  .v-input >>> .v-text-field__details {
    display: none;
  }
  .v-input >>> .v-select__selection {
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
    max-height: 37px;
  }
  .sc-btn {
    margin-bottom: 3px;
    margin-right: 3px;
    min-width: 67px!important;
    min-height: 58px;
  }
</style>
