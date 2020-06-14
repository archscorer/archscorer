<template>
  <v-dialog v-model="dialog" max-width="600px" v-if="!event.archive">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" :text="action === 'Register' ? false : true" v-on="on">{{ action }}</v-btn>
    </template>
    <v-card>
      <v-card-title>{{ action }} to "{{ event.name }}"</v-card-title>
      <v-card-text>
        <v-form v-model="valid">
          <eventParticipantDetails :participant="participant"
            :catering="event.catering"
            :catering_choices="event.catering_choices.split('|')"/>
          <v-container v-if="action !== 'Add Me'">
            <v-row>
              <v-autocomplete
                v-model="archer"
                :search-input.sync="query"
                :items="qresponse_items"
                label="Find archer from database"
                hint="Search is executed from 3 characters"
                placeholder="Start typing .."
                prepend-icon="mdi-database-search"
                return-object
                hide-no-data
                no-filter
                clearable
              >
              </v-autocomplete>
            </v-row>
            <template v-if="archer ? false : true">
              <!-- this should be somehow clear that by using this form form a
                   *new* archer profile is created -->
              <v-alert
                type="info">
                  Use query above to find archer from our database. If query does not find the archer you
                  were looking for you can click <v-btn x-small @click="new_archer = (new_archer ? false : true)">here</v-btn> to add new archer profile
                  to the database!
              </v-alert>
              <archerDetails v-model="participant.archer" :clubs="clubs" v-if="new_archer" />
            </template>
          </v-container>
        </v-form>
        <small><p>fields marked with '*' are mandatory</p></small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false; new_archer = false; archer = null">Close</v-btn>
        <v-btn color="primary"
          @click="addParticipantProxy()"
          :disabled="!valid">{{ action }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState, mapActions } from 'vuex'

  import eventParticipantDetails from '@/components/event/eventParticipantDetails.vue'
  import archerDetails from '@/components/archer/archerDetails.vue'

  export default {
    // name: "listCompetitonRegister",
    components: {
      eventParticipantDetails,
      archerDetails,
    },
    props: {
      action: String,
    },
    data: () => ({
      dialog: false,
      valid: false,
      archer: null,
      query: '',
      new_archer: false,

      participant: {
        event: null,
        archer: {
          full_name: '',
          gender: '',
          club: '',
          email: '',
          phone: '',
        },
        style: '',
        age_group: '',
        comments: '',
        food: false,
        food_choices: [],
      },
      // TODO write validators for form fields: style, age, gender, full_name, email
      // TODO quicklink to register me (skip archer fields or autofill them)
    }),
    watch: {
      query: function(val) {
        if (val && val.length >= 2) {
          this.searchArcher(val)
        } else {
          this.clearSearch([{ header: 'be more specific (at least 2 letters)' }])
        }
      },
      archer: function(obj) {
        if (obj) {
          this.participant.archer = obj
        } else {
          this.participant.archer = {
            full_name: '',
            gender: '',
            club: '',
            email: '',
            phone: '',
          }
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user,
        qresponse: state => state.user.qresponse,
        clubs: state => state.clubs.clubs,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      qresponse_items() {
        return this.qresponse.map(a => {
          if (a.id) {
            // add text field only if we have valid archer object
            let text = a.full_name + ' (' + a.club + ')' + (a.user ? ' - w account' : '') + (a.events ? ' ' + a.events + ' events': '')
            return Object.assign({}, a, { text })
          } else {
            return a
          }
        })
      }
    },
    methods: {
      ...mapActions('events', [
        'addParticipant',
      ]),
      ...mapActions('user', [
        'searchArcher',
        'clearSearch',
      ]),
      addParticipantProxy() {
        this.participant.event = parseInt(this.$route.params.id);
        if (this.action === "Add Me") {
          this.participant.archer = this.user.archer
        }
        this.participant.food_choices = this.participant.food_choices.join('|')
        this.addParticipant(this.participant);
        this.dialog = false
        this.archer = null
        this.query = ''
        this.new_archer = false
        this.valid = false
        this.participant = {
          event: null,
          archer: {
            full_name: '',
            gender: '',
            club: '',
            email: '',
            phone: '',
          },
          style: '',
          age_group: '',
          comments: '',
          food: false,
          food_choices: [],
        }
      },
    },
    created() {
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>

<style scoped>

</style>
