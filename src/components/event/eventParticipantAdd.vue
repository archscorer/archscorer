<template>
  <v-dialog v-model="dialog" max-width="600px" :fullscreen="$vuetify.breakpoint.xsOnly" v-if="!event.archive">
    <template v-slot:activator="{ on }">
      <v-btn color="primary"
        :text="action === 'Register' ? false : true"
        @click="init_participant()"
        v-on="on">{{ action }}</v-btn>
    </template>
    <v-card>
      <v-card-title>{{ action }} to "{{ event.name }}"</v-card-title>
      <v-card-text>
        <v-form ref="add_participant_form" v-model="valid">
          <v-container v-if="action !== 'Add Me'">
            <v-row>
              <archerSearch v-model="archer" />
            </v-row>
            <template v-if="archer ? false : true">
              <!-- this should be somehow clear that by using this form form a
                   *new* archer profile is created -->
              <v-alert
                type="info">
                  Or click <v-btn x-small @click="new_archer = (new_archer ? false : true)">here</v-btn> to add new archer profile
                  to the database!
              </v-alert>
              <archerDetails v-model="participant.archer" :clubs="clubs" v-if="new_archer" />
            </template>
          </v-container>
          <eventParticipantDetails :participant="participant"
            :catering="event.catering"
            :level_class="event.use_level_class"
            :catering_choices="event.catering_choices.split('|')"
            :age_style_choices="event.age_style_used.split(',')"/>
        </v-form>
        <small><p>fields marked with '*' are mandatory</p></small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false; new_archer = false; archer = null">Close</v-btn>
        <v-btn color="primary"
          @click="addParticipantProxy()"
          :disabled="!valid || !participant.archer.full_name">{{ action }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


<script>
  /* eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState, mapActions } from 'vuex'

  import eventParticipantDetails from '@/components/event/eventParticipantDetails.vue'
  import archerDetails from '@/components/archer/archerDetails.vue'
  import archerSearch from '@/components/archer/archerSearch.vue'

  export default {
    // name: "listCompetitonRegister",
    components: {
      eventParticipantDetails,
      archerDetails,
      archerSearch,
    },
    props: {
      action: String,
    },
    data: () => ({
      dialog: false,
      valid: false,
      archer: null,
      new_archer: false,
      participant: {}
      // TODO write validators for form fields: style, age, gender, full_name, email
    }),
    watch: {
      archer: function(obj) {
        if (obj) {
          let pId = obj.events[obj.events.length - 1]
          if (pId) {
            this.$store.dispatch('events/getParticipant', pId)
          }
          this.participant.archer = obj
        } else {
          this.participant.age_group = ''
          this.participant.style = ''
          this.participant.archer = {
            full_name: '',
            gender: '',
            club: '',
            email: '',
            phone: '',
          }
        }
      },
      participants: {
        deep: true,
        handler() {
          // this is prompted by archer watcher after getParticipant has returned
          // data
          if (this.participant.archer && this.participant.archer.events) {
            let events = this.participant.archer.events
            let pId = events[events.length - 1]
            let p = this.participants.find(p => p.id === pId)
            if (p) {
              this.participant.age_group = p.age_group
              this.participant.style = p.style
              this.participant.archer_rep = p.archer_rep
            }
          }
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user,
        clubs: state => state.clubs.clubs,
        participants: state => state.events.participants,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
    },
    methods: {
      ...mapActions('events', [
        'addParticipant',
      ]),
      init_participant() {
        this.query = ''
        this.new_archer = false
        this.archer = null
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
          level_class: '',
          comments: '',
          food: false,
          food_choices: [],
        }
        if (this.action === "Add Me") {
          this.archer = this.user.archer
        }
      },
      addParticipantProxy() {
        this.participant.event = parseInt(this.$route.params.id);
        this.participant.food_choices = this.participant.food_choices.join('|')
        this.addParticipant(this.participant);
        this.dialog = false
      },
    },
  }
</script>
