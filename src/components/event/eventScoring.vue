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
          return-object
          @change="resetScoreCards(); round = {id: null}">
        </v-select>
        <v-select
          label="Select round for scoring."
          v-model="round"
          :items="event_rounds"
          @input="get_scorecards(event.id, round.id)"
          return-object></v-select>
        <v-switch
          v-if="course.halves"
          v-model="halves"
          :label="halves ? 'Sum half' : 'Sum total'"
        />
      </v-card-title>
      <v-divider/>
      <template v-if="round.id !== null">
        <v-pagination
          v-model="end_view_pager"
          :length="course.ends ? course.ends.length : 0"
          :total-visible="14"
          circle
          @click.prevent=""></v-pagination>
        <v-sheet v-if="scorecards_loading" class="text-center py-10">
          <v-progress-circular indeterminate size="64" color="secondary"></v-progress-circular>
        </v-sheet>
        <eventScoringEnd v-else
                         :event="event"
                         :round="round"
                         :end="course.ends[end_view]"
                         :halves="halves"
                         :scorecards="scorecards"
                         @end_nav="update_end_view"/>
      </template>
    </template>
    <v-snackbar v-model="snack" :timeout="5000" :color="snackColor">
      {{ snackText }}
      <v-btn text @click="snack = false">Close</v-btn>
    </v-snackbar>
  </v-card>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
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
      currentRound: null,
      course: {ends: []},
      round: {id: null},
      halves: false,
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
      },
      end_view: function(val) {
        if (val < 0) {
          this.end_view = this.course.ends.length - 1
        }
        if (val > this.course.ends.length - 1) {
          this.end_view = 0
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
      ...mapActions('events', [
        'resetScoreCards',
        'getScoreCards'
      ]),
      get_course(cId) {
        // course layout determines the order of ends and scoring
        this.course = this.courses.find(obj => obj.id === cId)
        this.halves = this.course.halves
        this.end_view = (this.user_group.group_target < this.course.ends.length ? this.user_group.group_target - 1 : 0)
        // TODO: if course name or whatever matches indoor, then end_view should remain 0
      },
      get_scorecards(eId, rId) {
        if (this.user_group.id === null) {
          this.user_group = this.p_user[0]
        }
        // before getting new set, the current set should be destroyed
        this.resetScoreCards()
        this.currentRound = rId
        this.scorecards_loading = true
        // ask for scorecards. Creating new ones will take time, therefore catch
        // timeout and let user know of it
        let request = {eId: eId,
                       rId: rId,
                       pId: this.user_group.id }
        if ([this.event.creator, ...this.event.admins].includes(this.user.email)) {
          Object.assign(request, {group: this.user_group.group,
                                  group_target: this.user_group.group_target})
        }
        this.getScoreCards(request)
        .then(() => {
          this.scorecards_loading = false
          this.get_course(this.round.course)
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
