<template>
  <v-dialog v-model="dialog" fullscreen hide-overlay>
    <template v-slot:activator="{ on }">
      <v-btn color="warning" v-on="on" @click="e_update(); e_edit()">Edit Event</v-btn>
    </template>
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Edit {{ event.name }}</v-toolbar-title>
        <v-spacer />
        <v-toolbar-items>
          <v-btn dark text @click="putEvent({eId: event.id, event: event}); dialog = false">Save</v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-card class="ma-5">
        <v-card-title>General Info</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="4">
              <v-text-field
                v-model="event.name"
                :rules="[v => !!v || 'This field is required']"
                label="Event name"></v-text-field>
            </v-col><v-col cols="4">
              <v-menu
                v-model="date_start_menu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="270px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="event.date_start"
                    label="Start date"
                    prepend-icon="mdi-calendar"
                    :rules="[v => !!v || 'Start date is required']"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="event.date_start" @input="date_start_menu = false"></v-date-picker>
              </v-menu>
            </v-col><v-col cols="4">
              <v-menu
                v-model="date_end_menu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="270px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="event.date_end"
                    label="End date"
                    prepend-icon="mdi-calendar"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="event.date_end" @input="date_end_menu = false"></v-date-picker>
              </v-menu>
            </v-col>
          </v-row><v-row>
            <v-col cols="12">
              <v-textarea
                outlined
                v-model="event.description"
                label="Event details"
                auto-grow
              ></v-textarea>
            </v-col>
          </v-row><v-row>
            <v-col cols="6">
              <v-autocomplete
                v-model="event.type"
                autocomplete
                :items="event_type_choices"
                label="Event visibility class"
              ></v-autocomplete>
              <!-- here will be conditional helpful texts -->
            </v-col>
            <v-col cols="6">
              <v-switch
                v-model="event.is_open"
                :label="event.is_open ? 'Others can register' : 'Event is private'"
              ></v-switch>
              <v-switch
                v-model="event.catering"
                :label="event.catering ? 'Offer catering' : 'No catering'"
              ></v-switch>
              <v-switch
                v-model="event.archive"
                color="error"
                :label="event.archive ? 'Event is read-only' : 'Event can be edited'"
              ></v-switch>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="error"
                 @click="deleteE(event.id)">Delete Event</v-btn>
          <v-btn color="primary"
                 @click="putEvent({eId: event.id, event: event})">Save Changes</v-btn>
        </v-card-actions>
      </v-card>
      <v-card class="ma-5">
        <v-card-title>Manage Rounds</v-card-title>
        <v-card-text>
          <v-row dense v-for="(round, index) in event.rounds" :key="index">
            <v-col cols="4">
              <v-text-field
                v-model="event.rounds[index].label"
                label="Round description"
                @input="event.rounds[index].is_changed = true"
              >
                <template v-slot:prepend>
                  <strong class="lowered">{{ index + 1}}.</strong>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="4">
              <v-autocomplete
                v-model="event.rounds[index].course"
                :rules="[v => !!v || 'Round course is mandatory']"
                autocomplete
                :disabled="round.scorecards.length ? true : false"
                :items="courses"
                label="Round type"
                item-text="name"
                item-value="id"
                @input="event.rounds[index].is_changed = true"
              ></v-autocomplete>
            </v-col>
            <v-col cols="2">
              <v-switch
                v-model="event.rounds[index].is_open"
                :label="event.rounds[index].is_open ? 'Open' : 'Closed'"
                :error="event.rounds[index].is_open ? false : true"
                @change="event.rounds[index].is_changed = true"
              ></v-switch>
            </v-col>
              <template v-if="event.rounds[index].id">
              <v-btn v-if="event.rounds[index].is_changed"
                class="lowered"
                color="primary"
                @click="putRound(event.rounds[index])">Update</v-btn>
              </template>
              <v-btn v-else
                class="lowered"
                :disabled="event.rounds[index].course ? false : true"
                color="primary"
                @click="addRound(Object.assign(event.rounds[index], {ord: index+1, event: event.id})); event.rounds.splice(index, 1)">Confirm</v-btn>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="error" @click="deleteR()" >Remove last</v-btn>
          <v-btn color="primary" @click="newRound">Add new</v-btn>
        </v-card-actions>
      </v-card>
    </v-card>
  </v-dialog>
</template>

<script>

  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({
      dialog: false,
      date_start_menu: false,
      date_end_menu: false,
      event_type_choices: [
        { text: 'Private', value: 'private' },
        { text: 'Club - visible to all members', value: 'club' },
        { text: 'Open - visible to all', value: 'open' }
      ],
      event: {},
    }),
    watch: {
      p_event: {
        deep: true,
        handler() {
          this.e_edit()
        }
      },
      'event.archive': function(val) {
        if (val) {
          this.event.is_open = false
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user,
        courses: state => state.courses.courses,
      }),
      p_event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
    },
    methods: {
      ...mapActions('events', [
        'delEvent',
        'putEvent',
        'addRound',
        'delRound',
        'putRound',
      ]),
      newRound() {
        let lastCourse = null
        let lastLabel = ''
        let lastRound = this.event.rounds.slice(-1)[0]
        if (lastRound) {
          if (lastRound.course) {
            lastCourse = lastRound.course
          }
          if (lastRound.label) {
            lastLabel = lastRound.label
          }
        }
        this.event.rounds.push({label: lastLabel, course: lastCourse, is_open: true, scorecards: []})
      },
      deleteE(eId) {
        confirm('Event "' + this.event.name + '" will be removed permanently') &&
        this.delEvent(eId) &&
        this.$router.push('/events')
      },
      deleteR() {
        let lastRound = this.event.rounds.slice(-1)[0]
        if (lastRound.scorecards.length > 0) {
          confirm('Round "' + lastRound.ord + '. ' + lastRound.label +
          '" has been used already. Removing it will also delete ' +
          lastRound.scorecards.length + ' scorecard(s)') &&
          this.delLastRound()
        } else {
          this.delLastRound()
        }
      },
      delLastRound() {
        let r = this.event.rounds.pop()
        if (r.id) {
          this.delRound({eId: this.event.id, rId: r.id})
        }
      },
      e_edit() {
        // for edit dialog create clone of stored event, so closing wihtout saving would
        // not affect store state.
        this.event = Object.assign({}, this.p_event)
        this.event.rounds = [...this.event.rounds]
      },
      e_update() {
        // trigger event update before you start editing, so you would edit the right model
        this.$store.dispatch('events/updateEvent', parseInt(this.$route.params.id))
      }
    },
    created() {
      this.$store.dispatch('courses/getCourses')
    }
  }
</script>

<style scoped>
  .lowered {
    margin-top: 0.3rem;
  }
</style>