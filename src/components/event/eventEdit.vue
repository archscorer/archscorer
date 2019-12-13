<template>
  <v-dialog v-model="dialog" fullscreen hide-overlay>
    <template v-slot:activator="{ on }">
      <v-btn color="warning" v-on="on">Edit Event</v-btn>
    </template>
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Edit {{ event.name }}</v-toolbar-title>
        <v-spacer />
        <v-toolbar-items>
          <v-btn dark text @click="dialog = false">Save</v-btn>
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
          <v-btn color="primary" text>Save Changes</v-btn>
          <v-spacer />
          <v-btn color="error"
                 @click="deleteE(event.id)">Delete Event</v-btn>
        </v-card-actions>
      </v-card>
      <v-card class="ma-5">
        <v-card-title>Manage Rounds</v-card-title>
        <v-card-text>
          <v-row dense v-for="(round, index) in event.rounds" :key="index">
            <v-col cols="5">
              <v-text-field
                v-model="event.rounds[index].label"
                label="Round description"
              >
                <template v-slot:prepend>
                  <strong class="primary--text">{{ index + 1}}.</strong>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="4">
              <v-autocomplete
                v-model="event.rounds[index].course"
                :rules="[v => !!v || 'Round course is mandatory']"
                autocomplete
                :items="courses"
                label="Round type"
                item-text="name"
                item-value="id"
              ></v-autocomplete>
            </v-col>
            <v-col cols="2">
              <v-switch
                v-model="event.rounds[index].is_open"
                :label="event.rounds[index].is_open ? 'Open' : ''"
              ></v-switch>
            </v-col>
            <v-col cols="1">
              <v-btn text class="lowered" color="error" @click="delRound(index)" icon><v-icon size="30">mdi-minus</v-icon></v-btn>
            </v-col>
          </v-row>
          <v-row dense>
            <v-col cols="11">
            </v-col>
            <v-col cols="1">
              <v-btn text color="primary" @click="addRound" icon><v-icon size="35">mdi-plus</v-icon></v-btn>
            </v-col>
          </v-row>
        </v-card-text>
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
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
        courses: state => state.courses.courses,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
    },
    methods: {
      ...mapActions('events', [
        'deleteEvent',
      ]),
      addRound() {
        this.event.rounds.push({label: '', course: null, is_open: true})
      },
      delRound(index) {
        this.event.rounds.splice(index, 1)
      },
      deleteE(eId) {
        confirm('Event "' + this.event.name + '" will be removed permanently') &&
        this.deleteEvent(eId) &&
        this.$router.push('/events')
      }
    },
    created() {
      this.$store.dispatch('courses/getCourses')
    }
  }
</script>

<style scoped>
  .lowered {
    margin-top: 0.55rem;
  }
</style>
