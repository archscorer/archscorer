<template>
  <v-dialog
    v-if="user.id !== null"
    v-model="dialog"
    max-width="600px"
  >
    <template v-slot:activator="{ on }">
      <v-btn v-on="on"
        color="secondary"
        dark
        absolute
        top
        right
        fab
      ><v-icon>mdi-plus</v-icon></v-btn>
    </template>
    <v-stepper v-model="e1" alt-labels>
      <v-stepper-header>
        <v-stepper-step :complete="e1 > 1" step="1">General info</v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step :complete="e1 > 2" step="2">Rounds
          <small>Manage format</small>
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step step="3">Additional details
          <small>Registration, etc.</small>
        </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-card>
            <v-card-title>Add new archery event</v-card-title>
            <v-container>
              <v-form v-model="valid_e1">
                <v-container>
                  <v-row>
                    <v-col cols="6">
                      <v-text-field
                        v-model="event.name"
                        :rules="nameRules"
                        label="Event name"
                        required></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-menu
                        ref="date_menu"
                        v-model="date_menu"
                        :close-on-content-click="false"
                        :return-value.sync="dates"
                        transition="scale-transition"
                        offset-y
                      >
                        <template v-slot:activator="{ on }">
                          <!-- TODO default should be today and on-click clear v-model -->
                          <!-- TODO start end date separate and toggle multi day event -->
                          <v-text-field
                            v-model="dateRangeText"
                            :rules="dateRules"
                            label="Select date(s)"
                            prepend-icon="mdi-calendar"
                            readonly
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="dates"
                          range
                        >
                          <v-spacer></v-spacer>
                          <v-btn text @click="date_menu = false">Cancel</v-btn>
                          <v-btn color="primary" @click="$refs.date_menu.save(dates)">OK</v-btn>
                        </v-date-picker>
                      </v-menu>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12">
                      <v-textarea
                        outlined
                        v-model="event.description"
                        label="Event details"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-container>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="dialog = false">Close</v-btn>
              <v-btn color="primary"
                @click="e1 = 2"
                :disabled="!valid_e1">Next</v-btn>
            </v-card-actions>
          </v-card>
        </v-stepper-content>
        <v-stepper-content step="2">
          <v-card>
            <v-card-title>Add rounds/course</v-card-title>
            <v-form v-model="valid_e2">
              <v-container>
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
                      :rules="courseRules"
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
                    <v-btn text color="error" @click="delRound(index)" icon><v-icon size="30">mdi-minus</v-icon></v-btn>
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col cols="11">
                  </v-col>
                  <v-col cols="1">
                    <v-btn text color="primary" @click="addRound" icon><v-icon size="35">mdi-plus</v-icon></v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
            <v-card-actions>
              <v-btn @click="e1 = 1">Back</v-btn>
              <v-spacer></v-spacer>
              <v-btn text @click="dialog = false">Close</v-btn>
              <v-btn color="primary"
                @click="e1 = 3"
                :disabled="!valid_e2">Next</v-btn>
            </v-card-actions>
          </v-card>
        </v-stepper-content>
        <v-stepper-content step="3">
          <v-card>
            <v-row>
              <v-col cols="6">
                <v-autocomplete
                  v-model="event.type"
                  autocomplete
                  :items="event_type_choices"
                  label="Event visibility class"
                ></v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-switch
                  v-model="event.is_open"
                  :label="event.is_open ? 'Others can register*' : 'Event is private'"
                ></v-switch>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6"></v-col>
              <v-col cols="6">
                <v-switch
                  v-model="event.catering"
                  :label="event.catering ? 'With catering**' : 'No catering'"
                ></v-switch>
              </v-col>
            </v-row>
            <small>
              <p>* If event visibility is 'Private' and 'Others can register', they can do
                so by event URL. Click 'Finish' first and then you can navigate to the event
                and copy the URL. The 'Open' events are discoverable by anyone in event listing.
                The 'Club' events are discoverable by the club memebers only.</p>
              <p>** If catering is provided, the details (menu) should be added to the description of
                the event.</p>
            </small>
            <v-card-actions>
              <v-btn @click="e1 = 2">Back</v-btn>
              <v-spacer></v-spacer>
              <v-btn text @click="dialog = false">Close</v-btn>
              <v-btn color="primary"
                @click="addEvent(fixEventDates()); dialog = false; e1 = 1">Finish</v-btn>
            </v-card-actions>
          </v-card>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-dialog>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({
      dialog: false,
      e1: 1,

      event: {
        name: '',
        date_start: '',
        date_end: '',
        description: '',
        type: 'private',
        is_open: false,
        rounds: [{label: '', course: null, is_open: true}]
      },

      event_type_choices: [
        {
          text: 'Private',
          value: 'private'
        },
        {
          text: 'Club',
          value: 'club'
        },
        {
          text: 'Open',
          value: 'open'
        }
      ],

      valid_e1: false,

      nameRules: [v => !!v || 'Name is required'],
      dateRules: [v => !!v || 'Start date is required'],
      courseRules: [v => !!v || 'Round course is mandatory'],
      date_menu: false,
      dates: [],  // new Date().toISOString().substr(0, 10)

      valid_e2: false,
    }),
    computed: {
      dateRangeText () {
        return this.dates.join(' ~ ')
      },
      ...mapState({
        courses: state => state.courses.courses,
        user: state => state.user.user
      })
    },
    methods: {
      addRound() {
        this.event.rounds.push({label: '', course: null, is_open: true})
      },
      delRound(index) {
        this.event.rounds.splice(index, 1)
      },
      fixEventDates() {
        this.event.date_start = this.dates[0];
        this.event.date_end = this.dates.slice(-1)[0];
        return this.event
      },
      ...mapActions('events', [
        'addEvent'
      ])
    },
    created() {
      this.$store.dispatch('courses/getCourses')
    }
  }
</script>

<style scoped>
  .v-btn {
    margin-top: 0.55rem;
  }
</style>
