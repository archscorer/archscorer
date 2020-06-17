<template>
  <v-card v-if="event">
    <v-card-title v-if="event.archive === true">
      <small>This event is archived and can not be edited any more!</small>
    </v-card-title>
    <v-card-title v-else-if="user.id === null">
      <p>You need to be logged in for scoring</p>
    </v-card-title>
    <v-card-title v-else-if="!Array.isArray(p_user) || !p_user.length">
      <small>You need to register to the event first!</small>
    </v-card-title>
    <template v-else>
      <v-card-title>
        Round <v-spacer/>
        <v-select
          v-if="p_user.length > 1"
          label="Select your group to score."
          v-model="user_group"
          :items="p_user"
          item-text="group"
          return-object></v-select>
        <v-select
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
          :show-arrows="false"
          touchless>
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
      p_user: Array,
    },
    data: () => ({
      user_group: {id: null},
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
          if (!r || r.is_open === false) {
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
        // populate items for round selector
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
        // course layout determines the order of ends and scoring
        this.$store.dispatch('courses/getCourses', cId)
        .then(() => {
          this.course = this.courses.find(obj => obj.id === cId)
        })
      },
      get_scorecards(eId, rId) {
        if (this.user_group.id === null) {
          this.user_group = this.p_user[0]
        }
        // before getting new set, the current set should be destroyed
        this.$store.dispatch('events/resetScoreCardsUserGroup')
        this.end_view = this.user_group.group_target - 1
        this.currentRound = rId
        this.scorecards_loading = true
        // ask for scorecards. Creating new ones will take time, therefore catch
        // timeout and let user know of it
        this.$store.dispatch('events/getScoreCardsUserGroup', {eId: eId,
                                                               rId: rId,
                                                               pId: this.user_group.id })
        .then(() => {
          this.scorecards_loading = false
          this.$nextTick(() => {
            this.$refs.end[this.end_view].isActive = true
          })
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
  nav {
    transform: scale(0.9);
  }
  .v-select {
    max-width: 200px;
    margin: 0 20px;
  }
</style>
