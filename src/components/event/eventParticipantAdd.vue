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
        <v-form ref="add_participant_form" autocomplete="off" v-model="valid">
          <v-container v-if="action !== 'Add Me'">
            <v-row>
              <archerSearch v-model="archer" />
            </v-row>
            <template v-if="archer ? false : true">
              <!-- this should be somehow clear that by using this form a
                   *new* archer profile is created -->
              <v-alert
                type="info">
                  Or click <v-btn x-small @click="new_archer = (new_archer ? false : true)">here</v-btn> to add new archer profile
                  to the database!
              </v-alert>
              <template v-if="new_archer">
                <v-alert
                type="warning">
                This form is for adding *NEW* archers only! If you have competed before, use 'Find archer' search above.
              </v-alert>
              <archerDetails v-model="participant.archer" :clubs="clubs" />              
              </template>
            </template>
          </v-container>
          <eventParticipantDetails 
            :action="action"
            :participant="participant"
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
          if (this.event.use_level_class) {
            this.$store.dispatch('user/getArcherClassification', {aId: obj.id, date: this.event.date_start})
          }
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
            }
          }
        }
      },
      watch_classification: {
        handler() {
          const styles = ['FS-R','FS-C','FU','BB-R','BB-C','BL','BU','BH-C','BH-R','LB','TR']
          const age_groups = ['S', 'V', 'C']
          if (this.participant.style && this.participant.age_group) {
            let style = this.participant.style
            let age_group = this.participant.age_group
            let c = this.classifications.find(c => c.style === style && c.age_group === age_group)
            if (c) {
              this.participant.level_class = c.level
            } else {
              if (styles.includes(this.participant.style) && !age_groups.includes(this.participant.age_group)) {
                this.participant.level_class = 'a'
              } else {
                this.participant.level_class = ' '
              }
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
        classifications: state => state.user.classifications
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      watch_classification() {
        if (this.event && 
            this.event.use_level_class &&
            this.participant.archer && 
            this.participant.archer.events && 
            this.classifications.length) {
            let events = this.participant.archer.events
            let classes = this.classifications.map(c => {
              return c.style + '_' + c.age_group + ':' + c.level
            }).join(',')
          return events[events.length - 1] + '|' + this.participant.style + '|' + this.participant.age_group + '|' + classes
        }
        return {}
      }
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
