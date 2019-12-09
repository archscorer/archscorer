<template>
  <v-row justify="center">
    <v-col cols="12" sm="10" md="8" lg="6">
      <v-card>
        <v-card-title>
          <span class="headline">Archer Profile</span>
        </v-card-title>
        <v-form>
          <v-container>
            <v-row>
              <v-col cols="4">
                <v-text-field autofocus
                  v-model="user.archer.full_name"
                  label="Your full name"
                  hint="Your full name can not be empty string!"
                >
                </v-text-field>
              </v-col>
              <v-col cols="4">
                <v-select
                  v-model="user.archer.gender"
                  :items="[{'text': 'Male', 'value': 'M'}, {'text': 'Female', 'value': 'F'}]"
                  label="Gender"
                ></v-select>
              </v-col>
              <v-col cols="4">
                <v-select
                  v-model="user.archer.club"
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
                  v-model="user.archer.email"
                  label="Contact email address"
                >
                </v-text-field>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="user.archer.phone"
                  label="Contact phone number"
                >
                </v-text-field>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="user.archer.nat_id"
                  label="Archer national ID"
                  hint="FAAE ID in Estonia - first 7 digits from your national ID code."
                >
                </v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="updateArcher(user.archer)">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {

    data: () => ({
      //
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
        clubs: state => state.clubs.clubs,
      }),
    },
    methods: {
      ...mapActions('user', [
        'updateArcher'
      ]),
    },
    created() {
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>
