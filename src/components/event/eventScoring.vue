<template>
  <v-card v-if="event">
    <v-card-title v-if="user.id === null">
      <p>You need to be logged in for scoring</p>
    </v-card-title>
    <v-card-title v-else-if="p_user === null">
      <small>You need to register to the event first!</small>
    </v-card-title>
    <v-card-title v-else-if="event.archive === true">
      <small>This event in archived and can not be edited!</small>
    </v-card-title>
    <template v-else>
      <v-card-title>
        Round <v-spacer/>
        <v-select
          max-width="250px"
          label="Select round for scoring."
          v-model="round"
          :items="event_rounds"
          @input="get_scorecards(event.id, round.id); get_course(round.course)"
          return-object></v-select>
      </v-card-title>
      <v-divider/>
      <template v-if="round.id !== null">
        <v-pagination
          v-model="end_view_pager"
          :length="course.ends ? course.ends.length : 0"
          :total-visible="14"
          circle></v-pagination>
        <v-window v-model="end_view"
          :show-arrows="false">
          <v-window-item
            v-for="(end, ei) in course.ends"
            :key="'e' + currentRound + ':' + end.id"
            ref="end"
          >
            <v-sheet v-if="scorecards_loading === true" class="text-center py-10">
              <v-progress-circular indeterminate size="64" color="secondary"></v-progress-circular>
            </v-sheet>
            <eventScoringEnd v-else
                             :event="event"
                             :round="round"
                             :end="end"
                             :scorecards="scorecards"
                             :isActive="end_view === ei ? true : false"
                             @end_nav="update_end_view"/>
          </v-window-item>
        </v-window>
      </template>
    </template>
    <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
      {{ snackText }}
      <v-btn text @click="snack = false">Close</v-btn>
    </v-snackbar>
  </v-card>
</template>

<script>
  import { mapState} from 'vuex'
  import eventScoringEnd from '@/components/event/eventScoringEnd.vue'

  export default {

    components: {
      eventScoringEnd
    },
    props: {
      p_user: Object,
    },
    data: () => ({
      end_view: 0,
      arrow_inc: 0,
      currentRound: null,
      course: {ends: []},
      round: {id: null},
      scorecards_loading: false,

      snack: false,
      snackText: '',
      snackColor: ''
    }),
    watch: {
      event: {
        deep: true,
        handler () {
          let r = this.event.rounds.find(obj => obj.id === this.round.id)
          if (r && r.is_open === false) {
            this.round = {id: null}
          }
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user,
        courses: state => state.courses.courses,
        scorecards: state => state.events.scorecards
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      event_rounds() {
        return this.event.rounds.map(r => {
          let text = r.ord + '. ' + r.label + ' (' + r.course_name + ')'
          let disabled = !r.is_open
          return Object.assign({}, r, {text: text, disabled: disabled})
        })
      },
      end_view_pager: {
        get: function() {
          return this.end_view + 1
        },
        set: function(val) {
          this.end_view = val - 1
        }
      }
    },
    methods: {
      get_course(cId) {
        this.$store.dispatch('courses/getCourses', cId)
        .then(() => {
          this.course = this.courses.find(obj => obj.id === cId)
        })
      },
      get_scorecards(eId, rId) {
        // before getting new set, the current set should be destroyed
        this.$store.dispatch('events/resetUserGroupScoreCards')
        this.end_view = this.p_user.start_group - 1
        this.currentRound = rId
        this.scorecards_loading = true
        this.$store.dispatch('events/getUserGroupScoreCards', {eId: eId, rId: rId})
        .then(() => {
          this.scorecards_loading = false
        }).catch(err => {
          this.scorecards_loading = false
          if (err.code === 'ECONNABORTED') {
            this.snack = true
            this.snackColor = 'error'
            this.snackText = 'Operation timed out. Try again in few seconds.'
          }
        })
      },
      update_end_view(e) {
        e === '+' ? this.end_view++ : this.end_view--
      }
    },
  }
</script>

<style scoped>
  .v-pagination >>> * {
    transform: scale(0.75);
  }
  .v-select {
    max-width: 250px;
    margin: 0 25px;
  }
</style>
