<template>
  <v-sheet>
    <h4> End: {{ end.ord }} {{ end.label ? '(' + end.label + ')' : '' }}
      <small>
        -- Round: {{ round.ord }} {{ round.label ? '(' + round.label + ')': ''}} --
      </small>
    </h4>
    <v-row :class="{'oflow': $vuetify.breakpoint.xsOnly}" class="flex-nowrap" dense
      v-for="(sc, si) in scorecards"
      :key="'sc' + sc.id">
      <v-col cols="2" class="text text-truncate">{{ get_participant(sc.participant).full_name }}</v-col>
      <v-col cols="1" class="score"
        v-for="(a, ai) in sc.arrows.filter(obj => obj.end == end.id)"
        :key="'a' + a.id"
      >
        <v-text-field
          :value="a.x ? 'X' : a.score == 0 ? 'M': a.score"
          :loading="a.loading"
          :background-color="a.x ? '#FFC300' : a.score === 0 ? '#9E9E9E': ''"
          ref="arrow"
          readonly outlined dense
          @focus="currentFocus = [sc.id, a.id]; arrow_inc = si * sc.arrows.filter(obj => obj.end == end.id).length + ai">
        </v-text-field>
      </v-col>
      <v-col cols="1" class="text-cum">
        {{ get_end_score(sc) }}
      </v-col>
      <v-col cols="1" class="text-cum">
        {{ get_cum_score(sc) }}
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="2">
        <v-btn @click="currentFocus = null; $emit('end_nav', '-')" class="arr-btn"><v-icon>mdi-chevron-left</v-icon></v-btn>
      </v-col>
      <v-col cols="8">
        <v-btn v-for="score in sc_eval(end.scoring, end.x)"
          :key="'score' + end.id + '_' + score.text"
          class="sc-btn"
          @click.prevent="enter_score(score)">{{ score.text }}
        </v-btn>
      </v-col>
      <v-col cols="2">
        <v-btn @click="currentFocus = null; $emit('end_nav', '+')" ref="next_end" class="arr-btn"><v-icon>mdi-chevron-right</v-icon></v-btn>
      </v-col>
    </v-row>
    <v-snackbar v-model="snack" :timeout="5000" :color="snackColor">
      {{ snackText }}
      <v-btn text @click="snack = false">Close</v-btn>
    </v-snackbar>
  </v-sheet>
</template>

<script>
  import rankingService from '@/services/rankingService'

  function getScore(sc, e, h) {
    if (e && h === null) {
      return sc.arrows.filter(obj => obj.end === e.id).map(a => a.score)
    }
    if (e && h) {
      // TODO possible breaking issue if all ends in round with halves dont have
      // equal number of arrows. Is not an issue with standard formats
      // TAG custom fun format with 'halves'
      let div = sc.arrows.length / 2 / e.nr_of_arrows
      if (e.ord <= div) {
        return sc.arrows.slice(0, div * e.nr_of_arrows).map(a => a.score)
      }
      return sc.arrows.slice(div * e.nr_of_arrows).map(a => a.score)
    }
    return sc.arrows.map(a => a.score)
  }

  export default {
    props: {
      event: Object,
      round: Object,
      end: Object,
      halves: Boolean,
      scorecards: Array,
    },
    data: () => ({
      arrow_inc: 0,
      currentFocus: null,
      snack: false,
      snackText: '',
      snackColor: 'info',
    }),
    watch: {
      end: function() {
        this.currentFocus = null
        this.$nextTick(() => {
          this.focus_first_empty()
        })
      }
    },
    methods: {
      get_participant(pId) {
        if (this.event) {
          let participant = this.event.participants.find(obj => obj.id === pId)
          if (participant) {
            return participant
          }
        }
        return {archer: {full_name: null}}
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
          let [scId, aId] = this.currentFocus
          let arrow = this.scorecards.find(obj => obj.id === scId)
                              .arrows.find(obj => obj.id === aId)

          arrow.x = sc.text === 'X' ? true : false
          arrow.score = sc.value
          arrow.loading = 'warning'
          this.$store.dispatch('events/putArrow', {scId: scId, arrow: arrow})
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
          this.$nextTick(() => this.$refs.next_end.$refs.link.focus())
        } else {
          this.$nextTick(() => {
            this.$refs.arrow[this.arrow_inc].focus()
          })
        }
      },
      get_end_score(sc) {
        return rankingService.sum(getScore(sc, this.end, null))
      },
      get_cum_score(sc) {
        return rankingService.sum(getScore(sc, this.end, this.halves))
      },
      focus_first_empty() {
        // for this code to actually work it needs to be double $nextTick
        for (let a in this.$refs.arrow) {
          if (this.$refs.arrow[a].value === null) {
              this.$refs.arrow[a].focus()
            break
          }
        }
      }
    },
    mounted() {
      this.$nextTick(() => {
        this.focus_first_empty()
      })
    }
  }
</script>

<style scoped>
  .v-input >>> .v-text-field__details {
    display: none;
  }
  .v-input >>> .v-input__slot {
    min-height: 30px!important;
    max-height: 30px!important;
    padding: 0 5px!important;
  }
  .v-input >>> input {
    max-width: 100%;
    width: 100%;
    text-align: center;
    margin: 0;
  }
  .text {
    margin-top: 0.2rem;
    min-width: 80px;
  }
  .text-cum {
    margin-top: 0.2rem;
    white-space: nowrap;
  }
  .score {
    max-width: 37px;
    min-width: 37px;
    max-height: 30px;
  }
  .oflow {
    overflow-y: hidden;
    overflow-x: scroll;
  }
  .v-sheet {
    text-align: center;
  }
  .sc-btn {
    margin-bottom: 3px;
    margin-right: 2px;
    margin-left: 2px;
    min-width: 66px!important;
    min-height: 58px;
  }
  .arr-btn {
    min-height: 119px;
    min-width: 48px!important;
    padding: 2px 10px!important;
    margin: 5px;
  }
</style>
