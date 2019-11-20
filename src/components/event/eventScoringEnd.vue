<template>
  <v-sheet light>
    <h4> End: {{ end.ord }} {{ end.label ? '(' + end.label + ')' : '' }}</h4>
    <v-row class="oflow flex-nowrap" dense
      v-for="(sc, si) in scorecards"
      :key="'sc' + sc.id">
      <v-col cols="2" class="text">{{ get_participant(sc.participant).archer.full_name }}</v-col>
      <v-col cols="1" class="score"
        v-for="(a, ai) in sc.arrows.filter(obj => obj.end == end.id)"
        :key="'a' + a.id"
      >
        <v-select
          v-model="a.score"
          :items="sc_eval(end.scoring)"
          append-icon=""
          ref="arrow"
          readonly outlined dense
          @focus="currentFocus = [sc.id, a.id]; arrow_inc = si * sc.arrows.filter(obj => obj.end == end.id).length + ai">
        </v-select>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="2">
        <v-btn @click="currentFocus = null; $emit('end_nav', '-')" icon><v-icon>mdi-chevron-left</v-icon></v-btn>
      </v-col>
      <v-col cols="8">
        <template v-for="score in sc_eval(end.scoring)">
          <v-btn :key="'score' + end.id + '_' + score.text"
          @click="enter_score(score.value)">{{ score.text }}</v-btn>
        </template>
      </v-col>
      <v-col cols="2">
        <v-btn @click="currentFocus = null; $emit('end_nav', '+')" ref="next_end" icon><v-icon>mdi-chevron-right</v-icon></v-btn>
      </v-col>
    </v-row>
    <v-snackbar
      v-model="snackbar"
    >
      {{ message }}
      <v-btn
        text
        @click="snackbar = false; message = ''"
      >
        Close
      </v-btn>
    </v-snackbar>
  </v-sheet>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

  export default {

    props: {
      event: Object,
      end: Object,
      scorecards: Array,
    },
    data: () => ({
      arrow_inc: 0,
      currentFocus: null,
      snackbar: false,
      message: '',
    }),
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
      sc_eval(arr) {
        let scores_choices = eval(arr).map(function(v) {
          return {'text': v, 'value': v}
        })
        scores_choices.push({'text': 'M', 'value': 0})
        return scores_choices
      },
      enter_score(sc) {
        event.preventDefault()
        if (this.currentFocus === null) {
          this.$refs.arrow[0].focus()
          this.arrow_inc = 0
        }
        if (this.currentFocus) {
          let [scId, aId] = this.currentFocus
          let arrow = this.scorecards.find(obj => obj.id === scId)
                              .arrows.find(obj => obj.id === aId)
          arrow.score = sc
          this.$store.dispatch('events/putArrow', {scId: scId, arrow: arrow})
        }
        this.arrow_inc++
        if (this.arrow_inc >= this.$refs.arrow.length + 2) {
          this.message = "Focus on arrow you want to update or go to next end!"
          this.snackbar = true
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
    },
  }
</script>

<style scoped>
  .v-text-field--outlined.v-input--dense.v-text-field--outlined >>> .v-input__control > .v-input__slot {
    min-height: 30px;
    max-height: 31px;
    padding: 0 5px;
  }
  .v-input >>> .v-select__selection {
    width: 85%;
    text-align: center;
  }
  .text {
    margin-top: 0.2rem;
    white-space: nowrap;
    min-width: 80px;
    overflow: hidden;
  }
  .score {
    max-width: 45px;
    min-width: 45px;
    max-height: 30px;
  }
  .oflow {
    overflow-y: hidden;
    overflow-x: scroll;
  }
  .v-sheet {
    text-align: center;
  }
  .v-btn {
    margin-bottom: 3px;
    margin-right: 3px;
  }
</style>
