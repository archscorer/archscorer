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
          <small>Allow registration, etc.</small>
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
                    <v-col cols="4">
                      <v-text-field
                        autofocus
                        v-model="event.name"
                        :rules="[v => !!v || 'Name is required']"
                        label="Event name"></v-text-field>
                    </v-col>
                    <v-col cols="4">
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
                            readonly
                            :rules="[v => !!v || 'Start date is required']"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker v-model="event.date_start" @input="date_start_menu = false"></v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="4">
                      <v-switch v-model="multi_day" v-if="multi_day === false"
                                label="Multiple days?"/>
                      <v-menu
                        v-else
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
                            readonly
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker v-model="event.date_end" @input="date_end_menu = false"></v-date-picker>
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
                  <v-col cols="4">
                    <v-text-field
                      v-model="event.rounds[index].label"
                      label="Round description"
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
                  <v-col cols="2">
                    <v-btn text class="lowered" color="error" @click="delRound(index)" icon fab><v-icon size="30">mdi-minus</v-icon></v-btn>
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col cols="10">
                  </v-col>
                  <v-col cols="2">
                    <v-btn text color="primary" @click="addRound" icon fab><v-icon size="35">mdi-plus</v-icon></v-btn>
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
                  :label="event.is_open ? 'Registration is open*' : 'Registration is closed'"
                ></v-switch>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-alert v-if="event.type === 'open'"
                  border="bottom"
                  type="warning"
                  colored-border
                  elevation="2">
                  <small>
                    <p>
                      'Open' type of event is reserved for official / public archery events
                      only. This type of event can be seen by everybody in the events page.
                    </p>
                  </small>
                </v-alert>
                <v-alert v-if="event.type === 'club'"
                  border="bottom"
                  type="info"
                  colored-border
                  elevation="2">
                  <small>
                    <p>
                      'Club' type of event should be used for club level events. Club members
                      can see this type of events on events page. Archers outside the club
                      can still register by event link.
                    </p>
                  </small>
                </v-alert>
              </v-col>
              <v-col cols="6">
                <v-switch
                  v-model="event.catering"
                  :label="event.catering ? 'With catering**' : 'No catering'"
                ></v-switch>
              </v-col>
            </v-row>
            <small>
              <p>* If event visibility is 'Private' and 'Registration is open', they can do
                so by event URL. Click 'Finish' first and then you can navigate to the event
                and copy the URL. The 'Open' events are discoverable by anyone on the
                <router-link :to="'events'">Events page</router-link>.
                The 'Club' events are discoverable by the club memebers only.</p>
              <p>** If catering is provided, the details (menu) should be added to the description of
                the event.</p>
            </small>
            <v-card-actions>
              <v-btn @click="e1 = 2">Back</v-btn>
              <v-spacer></v-spacer>
              <v-btn text @click="dialog = false">Close</v-btn>
              <v-btn color="primary"
                @click="addEvent(checkEventDates()); dialog = false; e1 = 1">Finish</v-btn>
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
        date_start: new Date().toISOString().substr(0, 10),
        date_end: '',
        description: '',
        type: 'private',
        is_open: false,
        rounds: [{label: '', course: null, is_open: true}]
      },

      event_type_choices: [
        { text: 'Private', value: 'private' },
        { text: 'Club', value: 'club' },
        { text: 'Open', value: 'open' }
      ],

      valid_e1: false,

      date_start_menu: false,
      date_end_menu: false,
      multi_day: false,

      valid_e2: false,
    }),
    watch: {
      multi_day: {
        handler() {
          this.event.date_end = this.event.date_start
        }
      }
    },
    computed: {
      dateRangeText () {
        return this.dates.join(' ~ ')
      },
      ...mapState({
        user: state => state.user.user,
        courses: state => state.courses.courses,
      })
    },
    methods: {
      addRound() {
        this.event.rounds.push({label: '', course: null, is_open: true})
      },
      delRound(index) {
        this.event.rounds.splice(index, 1)
      },
      checkEventDates() {
        if (this.event.date_end === '' || new Date(this.event.date_end) <  new Date(this.event.date_start)) {
          this.event.date_end = this.event.date_start
        }
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
  .lowered {
    margin-top: 0.3rem;
  }
</style>
