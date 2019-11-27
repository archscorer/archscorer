<template>
  <v-card v-if="event">
    <v-card-title v-if="user.id === null">
      <p>You need to be logged in for scoring</p>
    </v-card-title>
    <v-card-title v-else-if="is_user_regitered() !== true">
      <p>It looks like you are not part of this event. Maybe you should register first</p>
    </v-card-title>
    <template v-else>
      <v-card-title>
        Round <v-spacer/>
        <template v-for="round in event.rounds">
          <v-btn @click="get_scorecards(event.id, round.id); get_course(round.course)" :key="round.id">{{ round.ord }}</v-btn>
        </template>
      </v-card-title>
      <v-divider/>
      <v-pagination
        v-model="end_view_pager"
        :length="course.ends ? course.ends.length : 0"
        :total-visible="14"
        circle></v-pagination>
      <v-window v-model="end_view"
        :show-arrows="false">
        <v-window-item
          v-for="end in course.ends"
          :key="'e' + currentRound + ':' + end.id"
          ref="end"
        >
          <eventScoringEnd :event="event"
                           :end="end"
                           :scorecards="scorecards"
                           @end_nav="update_end_view"/>
        </v-window-item>
      </v-window>
    </template>
  </v-card>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState} from 'vuex'
  import eventScoringEnd from '@/components/event/eventScoringEnd.vue'

  export default {

    components: {
      eventScoringEnd
    },
    data: () => ({
      end_view: null,
      arrow_inc: 0,
      currentRound: null,
    }),
    watch: {
      course: {
        deep: true,
        handler() {
          this.$nextTick(() => {
            if (this.course.ends.length) this.$refs.end[this.end_view].isActive = true
          })
        }
      },
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
      is_user_regitered() {
        let p_user = this.event.participants.find(obj => obj.archer.id === this.user.archer.id)
        if (p_user) {
          if (this.end_view === null) {
            this.end_view = p_user.start_group - 1
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
        this.currentRound = rId

        this.$store.dispatch('events/getUserGroupScoreCards', {eId: eId, rId: rId})
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
</style>
