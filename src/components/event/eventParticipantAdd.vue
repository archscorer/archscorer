<template>
  <v-dialog v-model="dialog" max-width="600px" v-if="!event.archive">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" :text="action === 'Register' ? false : true" v-on="on">{{ action }}</v-btn>
    </template>
    <v-card>
      <v-card-title>{{ action }} to "{{ event.name }}"</v-card-title>
      <v-card-text>
        <v-form v-model="valid">
          <eventParticipantDetails :participant="participant" :catering="event.catering"/>
          <v-container v-if="action !== 'Add Me'">
            <v-row>
              <v-autocomplete
                v-model="archer"
                :search-input.sync="query"
                :items="qresponse_items"
                item-value="id"
                label="Existing Archers"
                placeholder="Start typing to query"
                prepend-icon="mdi-database-search"
                return-object
                hide-no-data
                no-filter
                clearable
              >
            </v-autocomplete>
            </v-row>
            <template v-if="archer ? false : true">
              <span class="archer-warn">Use form below only if archer could not be found from database!</span>
              <v-row>
                <v-col cols="4">
                  <v-text-field
                    v-model="participant.archer.full_name"
                    label="Your full name*"
                    :rules="[v => !!v || 'This field is required']"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-select
                    v-model="participant.archer.gender"
                    :items="[{'text': 'Male', 'value': 'M'}, {'text': 'Female', 'value': 'F'}]"
                    label="Gender*"
                    :rules="[v => !!v || 'Choice must be made :)']"
                  ></v-select>
                </v-col>
                <v-col cols="4">
                  <v-select
                    v-model="participant.archer.club"
                    :items="clubs ? clubs : []"
                    label="Choose Club*"
                    :rules="[v => !!v || 'Choose ..no club.. if other options are not suitable']"
                    item-text="name"
                    item-value="id"
                  ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <v-text-field
                    v-model="participant.archer.email"
                    label="Contact email address*"
                    :rules="[v => !!v || 'This field is required']"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    v-model="participant.archer.phone"
                    label="Contact phone number"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    v-model="participant.archer.nat_id"
                    label="Archer national ID"
                    hint="FAAE ID in Estonia - first 7 digits from your national ID code."
                  >
                  </v-text-field>
                </v-col>
              </v-row>
            </template>
          </v-container>
        </v-form>
        <small><p>fields marked with '*' are mandatory</p></small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false">Close</v-btn>
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

  export default {
    // name: "listCompetitonRegister",
    components: {
      eventParticipantDetails,
    },
    props: {
      action: String,
    },
    data: () => ({
      dialog: false,
      valid: false,
      archer: null,
      query: '',

      participant: {
        'event': null,
        'archer': {
          'full_name': '',
          'gender': '',
          'club': '',
          'email': '',
          'phone': '',
        },
        'style': '',
        'age_group': '',
        'comments': '',
        'food': false
      },
      // TODO write validators for form fields: style, age, gender, full_name, email
      // TODO quicklink to register me (skip archer fields or autofill them)
    }),
    watch: {
      query: function(val) {
        if (val && val.length >= 2) {
          this.searchArcher(val)
        } else {
          this.clearSearch([{ header: 'be more specific' }])
        }
      },
      archer: function(obj) {
        if (obj) {
          this.participant.archer = obj
        } else {
          this.participant.archer = {
            'full_name': '',
            'gender': '',
            'club': '',
            'email': '',
            'phone': '',
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
            let text = a.full_name + ' (' + a.club + ')' + (a.user ? ' - has account' : '')
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
        this.addParticipant(this.participant);
        this.dialog = false
      },
    },
    created() {
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>

<style scoped>

</style>
