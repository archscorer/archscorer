<template>
  <v-card>
    <v-card-title v-if="user.id === null">
      <p>You need to be logged in for scoring</p>
    </v-card-title>
    <v-card-title v-else-if="is_user_regitered() !== true">
      <p>It looks like you are not part of this event. Maybe you should register first</p>
    </v-card-title>
    <v-card-title v-else>
      Round <v-spacer/>
      <template v-for="round in event.rounds">
        <v-btn @click="get_scorecards(event.id, round.id); get_course(round.course)" :key="round.id">{{ round.ord }}</v-btn>
      </template>
    </v-card-title>
    <v-divider/>
    <v-carousel v-model="end_slide"
      :show-arrows="false">
      <v-carousel-item
        v-for="end in course.ends"
        :key="'e' + end.id"
      >
        <v-sheet light>
          <h4> End: {{ end.ord }} {{ end.label ? '(' + end.label + ')' : '' }} </h4>
          <v-form>
            <v-row class="oflow flex-nowrap" dense
              v-for="(sc, si) in scorecards"
              :key="'sc' + sc.id">
              <v-col cols="2" class="text">{{ get_participant(sc.participant).archer.full_name }}</v-col>
              <v-col cols="1" class="score"
                v-for="(a, ai) in sc.arrows.filter(obj => obj.end == end.id)"
                :key="'a' + a.id"
              >
                <v-text-field dense outlined
                  v-model="a.score"
                  ref="arrow"
                  readonly
                  @focus="currentFocus = [sc.id, a.id]; arrow_inc = si * sc.arrows.filter(obj => obj.end == end.id).length + ai">
                </v-text-field>
              </v-col>
            </v-row>
          </v-form>
          <v-row dense>
            <v-col cols="2">
              <v-btn @click="end_slide--; slide_switch()" icon><v-icon>mdi-chevron-left</v-icon></v-btn>
            </v-col>
            <v-col cols="8">
              <template v-for="score in sc_eval(end.scoring)">
                <v-btn :key="'score' + end.id + '_' + score"
                @mousedown="enter_score(score)">{{ score }}</v-btn>
              </template>
            </v-col>
            <v-col cols="2">
              <v-btn @click="end_slide++; slide_switch()" ref="next_end" icon><v-icon>mdi-chevron-right</v-icon></v-btn>
            </v-col>
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>
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
  </v-card>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState} from 'vuex'

  // function sum(arr) {
  //   return arr.reduce((sum, x) => sum + x);
  // }
  //
  // function getScore(r, p) {
  //   let r_sc = p.scorecards.find(obj => obj.round === round.id)
  //   return r_sc ?  r_sc.arrows.map(a => a.score) : [0]
  // }
  //
  // function cSumSc( a, b ) {
  //   if ( a.sum > b.sum ){
  //     return -1;
  //   }
  //   if ( a.sum < b.sum ){
  //     return 1;
  //   }
  //   return 0;
  // }


  export default {

    data: () => ({
      end_slide: null,
      arrow_inc: 0,
      currentFocus: null,
      snackbar: false,
      message: '',
    }),
    watch: {
      course: {
        deep: true,
        handler() {
          // console.log('course has changed')
        }
      },
      scorecards: {
        deep: true,
        handler() {
          // console.log('scorecards have changed')
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user,
        course: state => state.courses.courses,
        scorecards: state => state.events.scorecards
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
    },
    methods: {
      is_user_regitered() {
        let p_user = this.event.participants.find(obj => obj.archer.id === this.user.archer.id)
        if (p_user) {
          if (this.end_slide === null) {
            this.end_slide = p_user.start_group - 1            
          }
          return true
        } else {
          return false
        }
      },
      get_course(cId) {
        this.$store.dispatch('courses/getCourses', cId)
      },
      get_scorecards(eId, rId) {
        this.$store.dispatch('events/getUserGroupScoreCards', {eId: eId, rId: rId})
      },
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
        let allowed_scores = eval(arr)
        allowed_scores.push('M')
        return allowed_scores
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
        if (this.arrow_inc >= this.$refs.arrow.length + 3) {
          this.message = "Focus on arrow you want to update or go to next end!"
          this.snackbar = true
        } else if (this.arrow_inc >= this.$refs.arrow.length) {
          // so that no scores would be changed if clicked again
          this.currentFocus = false
          // we have finished all arrows, focus on arrow key to next page
          this.$nextTick(() => this.$refs.next_end[0].$refs.link.focus())
        } else {
          this.$nextTick(() => this.$refs.arrow[this.arrow_inc].focus())
        }
      },
      slide_switch() {
        this.currentFocus = null
        this.$refs.arrow = []
        this.$refs.next_end = []
      }
    },
  }
</script>

<style scoped>
  .col > .v-input {
    max-height: 35px;
    margin-bottom: 5px;
  }
  .v-input >>> input {
    text-align: center;
  }
  .text {
    margin-top: 0.55rem;
    white-space: nowrap;
    min-width: 80px;
    overflow: hidden;
  }
  .score {
    max-width: 50px;
    min-width: 45px;
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
