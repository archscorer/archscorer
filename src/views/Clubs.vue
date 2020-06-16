<template>
  <v-container v-if="clubs">
    <v-layout
      text-center
      wrap
    >
      <v-card width="100%">
        <v-card-title>FAAE Clubs</v-card-title>
        <v-card-text>
          <p>Club managers, please contact 'info @ archscorer . faae . ee'  to request
            admin access to your club.</p>
        </v-card-text>
      </v-card>
      <v-card v-for="club in clubs" :key="club.id" class="ma-5"
        :to="{ name: 'club', params: { 'id': club.id}}">
        <v-card-title>
          {{ club.name }}
        </v-card-title>
        <v-card-text>
          <p>There are {{ Array.isArray(club.members) ? club.members.length : club.members }} members</p>
        </v-card-text>
      </v-card>
    </v-layout>
  </v-container>
  <v-overlay v-else>
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-overlay>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    computed: {
      ...mapState({
        user: state => state.user.user,
        clubs: state => state.clubs.clubs,
      }),
    },
    created() {
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>
