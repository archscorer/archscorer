<template>
  <v-row justify="center">
    <v-col cols="12" sm="10" md="8" lg="6">
      <v-alert type="warning"
        outlined
        class="text-justify">
        For new user associated archer profile is selected based on account email
        address from our database, if one or more exists. If there is more than one
        archer profile associated with given email address (contact email for many
        archers), first (random?) one is bound to given user account. Currently
        you have <b>no</b> way to change that on your own and <b>please don't change
        existing profile, if its intended to somebody else</b>. Contact 'info @ archscorer .
        faae . ee' to reassign correct profile to your account.
      </v-alert>
      <v-card>
        <v-card-title>
          <span class="headline">Archer Profile</span>
        </v-card-title>
        <v-form v-model="valid">
          <archerDetails v-model="user.archer" :clubs="clubs"/>
        </v-form>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn :disabled="!valid" color="primary" @click="putArcher(user.archer); $router.go(-1)">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
  import archerDetails from '@/components/archer/archerDetails.vue'
  import { mapState, mapActions } from 'vuex'

  export default {

    components: {
      archerDetails,
    },
    data: () => ({
      valid: false,
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
        clubs: state => state.clubs.clubs,
      }),
    },
    methods: {
      ...mapActions('user', [
        'putArcher'
      ]),
    },
    created() {
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>
