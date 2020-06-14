<template>
  <v-container v-if="clubs">
    <v-layout
      text-center
      wrap
    >
      <v-card>
        <v-card-text>
          <p>This part of the site has not been developed yet. Listed clubs are
            not interactive and currently only show how many members have been assigned
            to them. You can assign yourself to a created club by editing your profile.</p>
          <p>Plan is to give club management to the hands of club management board. User
            can select their club once they create their account or there is archer profile
            created for them. Club managers then can confirm membership and the choice will
            be then locked for user (until kicked from club and/or lifted by managers).</p>
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
