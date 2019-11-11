<template>
  <v-dialog v-model="dialog" max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" v-on="on">Register</v-btn>
    </template>
    <v-card>
      <v-card-title>Register to "{{ event.name }}"</v-card-title>
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
            <v-col cols="5">
              <v-text-field
                v-model="archer.full_name"
                label="Your full name"
              >
              </v-text-field>
            </v-col>
            <v-col cols="2">
              <v-select
                v-model="archer.gender"
                :items="[{'text': 'Male', 'value': 'M'}, {'text': 'Female', 'value': 'F'}]"
                label="Gender"
              ></v-select>
            </v-col>
            <v-col cols="5">
              <v-select
                v-model="archer.club"
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
                v-model="archer.email"
                label="Contact email address"
              >
              </v-text-field>
            </v-col>
            <v-col cols="5">
              <v-text-field
                v-model="archer.phone"
                label="Contact phone number"
              >
              </v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="archer.nat_id"
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
          @click="addParticipant(collectParticipant()); dialog = false"
          :disabled="!valid">Register</v-btn>
      </v-card-actions>
    </v-card>
    <v-card>
      <v-card-title>
      Registered Archers
      <v-spacer></v-spacer>
      <v-text-field
        v-model="p_search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
      <v-data-table
        dense
        :headers="p_table_header"
        :items="p_table"
        :search="p_search"
        :items-per-page="50"
      ></v-data-table>
    </v-card>
  </v-dialog>
</template>


<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState, mapActions } from 'vuex'

  export default {
    // name: "listCompetitonRegister",
    props: {
      event: Object
    },
    data: () => ({
      dialog: false,
      valid: false,

      archer: {
        'full_name': '',
        'gender': '',
        'club': '',
        'email': '',
        'phone': '',
        'nat_id': '',
      },
      participant: {
        'event': null,
        'archer': null,
        'style': '',
        'age_group': '',
        'comments': '',
        'eats': false
      },
      p_search: '',
      p_table_header: [
        { text: 'Name', value: 'name' },
        { text: 'Class', value: 'class' },
        { text: 'Club', value: 'club' },
        { text: 'Eats', value: 'eats' }
      ],
      // TODO write validators for form fields: style, age, gender, full_name, email
      // TODO quicklink to register me (skip archer fields or autofill them)
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
        pModel: state => state.events.participantModel,
        clubs: state => state.clubs.clubs,
      }),
      p_table() {
        return this.event.participants.map(function(p) {
          return {
            name: p.archer.full_name,
            class: p.age_group + p.archer.gender + p.style,
            club: p.archer.club,
            eats: (p.eats ? "Yes" : "No")
          }
        })
      },
    },
    methods: {
      ...mapActions('events', [
        'addParticipant',
        'delParticipant',
      ]),
      collectParticipant() {
        this.participant.archer = this.archer;
        this.participant.event = this.event.id;
        return this.participant
      },
    },
    created() {
      this.$store.dispatch('events/getParticipantOpts'),
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>
