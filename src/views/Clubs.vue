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
        </v-card-text>
      </v-card>
      <v-card v-for="club in clubs" :key="club.id" class="ma-5">
        <v-card-title>
          {{ club.name }}
        </v-card-title>
        <v-card-text>
          <p>There are {{ club.members.length }} members</p>
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
