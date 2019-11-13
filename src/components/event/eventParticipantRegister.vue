<template>
  <v-dialog v-model="dialog" max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" v-on="on">Register</v-btn>
    </template>
    <v-card>
      <v-card-title>Register to "{{ event ? event.name : '' }}"</v-card-title>
      <v-form v-model="valid">
        <v-container>
          <v-row dense>
            <v-col cols="4">
              <v-select
                v-model="participant.style"
                :items="pModel ? pModel.style.choices : []"
                label="Style"
                item-text="display_name"
                dense
              ></v-select>
            </v-col>
            <v-col cols="4">
              <v-select
                v-model="participant.age_group"
                :items="pModel ? pModel.age_group.choices : []"
                label="Age Group"
                item-text="display_name"
                dense
              ></v-select>
            </v-col>
            <v-col cols="4">
              <v-switch
                v-model="participant.eats"
                label="Catering"
                color="primary"
              ></v-switch>
            </v-col>
          </v-row>
          <v-row dense>
            <v-col cols="12">
              <v-textarea
                outlined
                v-model="participant.comments"
                label="Comments to organiser(s)"
              ></v-textarea>
            </v-col>
          </v-row>
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
            <v-col cols="4">
              <v-text-field
                v-model="participant.archer.email"
                label="Contact email address"
              >
              </v-text-field>
            </v-col>
            <v-col cols="5">
              <v-text-field
                v-model="participant.archer.phone"
                label="Contact phone number"
              >
              </v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="participant.archer.nat_id"
                label="Archer ID"
                hint="National Archer ID"
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
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState, mapActions } from 'vuex'

  export default {
    // name: "listCompetitonRegister",
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
        pModel: state => state.events.participantModel,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
    },
    methods: {
      ...mapActions('events', [
        'addParticipant',
        'delParticipant',
      ]),
    },
    created() {
      this.$store.dispatch('events/getParticipantOpts'),
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>
