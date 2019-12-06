<template>
  <v-dialog v-model="dialog" max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" v-on="on">Register</v-btn>
    </template>
    <v-card>
      <v-card-title>Register to "{{ event ? event.name : '' }}"</v-card-title>
      <v-form v-model="valid">
        <eventParticipantDetails :participant="participant"/>
        <v-container>
          <v-row>
            <v-col cols="4">
              <v-text-field
                v-model="participant.archer.full_name"
                label="Your full name"
              >
              </v-text-field>
            </v-col>
            <v-col cols="4">
              <v-select
                v-model="participant.archer.gender"
                :items="[{'text': 'Male', 'value': 'M'}, {'text': 'Female', 'value': 'F'}]"
                label="Gender"
              ></v-select>
            </v-col>
            <v-col cols="4">
              <v-select
                v-model="participant.archer.club"
                :items="clubs ? clubs : []"
                label="Choose Club"
                item-text="name"
                item-value="id"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-text-field
                v-model="participant.archer.email"
                label="Contact email address"
              >
              </v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model="participant.archer.phone"
                label="Contact phone number"
              >
              </v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false">Close</v-btn>
        <v-btn color="primary"
          @click="participant.event = parseInt($route.params.id); addParticipant(participant); dialog = false"
          :disabled="!valid">Register</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


<script>
  import { mapState, mapActions } from 'vuex'

  import eventParticipantDetails from '@/components/event/eventParticipantDetails.vue'

  export default {
    // name: "listCompetitonRegister",
    components: {
      eventParticipantDetails,
    },
    data: () => ({
      dialog: false,
      valid: false,

      participant: {
        'event': null,
        'archer': {
          'full_name': '',
          'gender': '',
          'club': '',
          'email': '',
          'phone': '',
          'nat_id': '',
        },
        'style': '',
        'age_group': '',
        'comments': '',
        'eats': false
      },
      // TODO write validators for form fields: style, age, gender, full_name, email
      // TODO quicklink to register me (skip archer fields or autofill them)
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
        clubs: state => state.clubs.clubs,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
    },
    methods: {
      ...mapActions('events', [
        'addParticipant',
      ]),
    },
    created() {
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>
