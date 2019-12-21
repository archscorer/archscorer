<template>
  <v-sheet light>
    <h4> End: {{ end.ord }} {{ end.label ? '(' + end.label + ')' : '' }}
      <small>
        -- Round: {{ round.ord }} {{ round.label ? '(' + round.label + ')': ''}} --
      </small>
    </h4>
    <v-row class="oflow flex-nowrap" dense
      v-for="(sc, si) in scorecards"
      :key="'sc' + sc.id">
      <v-col cols="2" class="text text-truncate">{{ get_participant(sc.participant).archer.full_name }}</v-col>
      <v-col cols="1" class="score"
        v-for="(a, ai) in sc.arrows.filter(obj => obj.end == end.id)"
        :key="'a' + a.id"
      >
        <v-select
          v-model="a.score"
          :items="sc_eval(end.scoring)"
          append-icon=""
          :loading="a.loading"
          :error="a.error"
          :background-color="a.x ? '#FFC300' : a.score === 0 ? '#9E9E9E': ''"
          ref="arrow"
          readonly outlined dense
          @focus="currentFocus = [sc.id, a.id]; arrow_inc = si * sc.arrows.filter(obj => obj.end == end.id).length + ai">
        </v-select>
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
        <v-btn @click="currentFocus = null; $emit('end_nav', '-')" icon><v-icon>mdi-chevron-left</v-icon></v-btn>
      </v-col>
      <v-col cols="8">
        <template v-for="score in sc_eval(end.scoring, end.x)">
          <v-btn :key="'score' + end.id + '_' + score.text"
          class="sc-btn"
          @click.prevent="enter_score(score)">{{ score.text }}</v-btn>
        </template>
      </v-col>
      <v-col cols="2">
        <v-btn @click="currentFocus = null; $emit('end_nav', '+')" ref="next_end" icon><v-icon>mdi-chevron-right</v-icon></v-btn>
      </v-col>
    </v-row>
    <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
      {{ snackText }}
      <v-btn text @click="snack = false">Close</v-btn>
    </v-snackbar>
  </v-sheet>
</template>

<script>

  function sum(arr) {
    return arr.reduce((sum, x) => sum + x);
  }

  function getScore(sc, e) {
    if (e) {
      return sc.arrows.filter(obj => obj.end === e.id).map(a => {return a.score ? a.score : 0})
    }
    return sc.arrows.map(a => {return a.score ? a.score : 0})
  }

  export default {

    props: {
      event: Object,
      round: Object,
      end: Object,
      scorecards: Array,
      isActive: Boolean,
    },
    data: () => ({
      arrow_inc: 0,
      currentFocus: null,
      snack: false,
      snackText: '',
      snackColor: 'info',
    }),
    watch: {
      isActive: function(val) {
        if (val === true && this.currentFocus === null) {
          this.$nextTick(() => {
            this.focus_first_empty()
          })
        }
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
        return sum(getScore(sc, this.end))
      },
      get_cum_score(sc) {
        return sum(getScore(sc))
      },
      focus_first_empty() {
        // for this code to actually work it needs to be double $nextTick
        for (let a in this.$refs.arrow) {
          if (this.$refs.arrow[a].value === null) {
            this.$nextTick(() => {
              this.$refs.arrow[a].focus()
            })
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
  .v-text-field--outlined.v-input--dense.v-text-field--outlined >>> .v-input__control > .v-input__slot {
    min-height: 30px;
    max-height: 30px;
    padding: 0 5px;
  }
  .v-input >>> .v-select__selection {
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
    margin-right: 3px;
    min-width: 67px!important;
    min-height: 58px;
  }
</style>
