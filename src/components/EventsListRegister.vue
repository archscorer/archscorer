<template>
  <v-dialog v-model="dialog" max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" v-on="on">Register</v-btn>
    </template>
    <v-card>
      <v-card-title>Register to {{ comp_id }}</v-card-title>
      <v-form v-model="valid">
        <v-container>
          <v-row dense>
            <v-col cols="6">
              <v-text-field
                v-model="participant.full_name"
                label="FirstName LastName"
              >
                <template v-slot:prepend>
                  <strong class="primary--text">Name:</strong>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="6">
            </v-col>
          </v-row>
        </v-container>
      </v-form>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false">Close</v-btn>
        <v-btn color="primary"
          @click="dialog = false"
          :disabled="!valid">Register</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


<script>
  import { mapState, mapActions } from 'vuex'
  export default {
    // name: "listCompetitonRegister",
    props: {
      comp_id: Number
    },
    data: () => ({
      dialog: false,
      valid: false,

      participant: {
        'full_name': '',
      }
    }),
    computed: {
      ...mapState({
        user: state => state.user.user
      })
    },
    methods: {
      ...mapActions('events', [
        'deleteEvent'
      ])
    },
    created() {
      // this.$store.dispatch('events/getEvents')
    }
  }
</script>
