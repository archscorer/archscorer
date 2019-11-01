<template>
  <v-container>
      <v-card class="my-2">
        <v-card-title>Create New</v-card-title>
      </v-card>
      <v-card class="my-2">
        <v-card-title>Browse</v-card-title>
        <v-list>
          <v-subheader v-if="competitions.length === 0">No competitions found in the database</v-subheader>
          <v-list-item
          v-for="(competition, i) in competitions"
          :key="i"
        >
          <v-list-item-content>
            <v-list-item-title v-text="item.name"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </v-list>
      </v-card>
  </v-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  data: () => ({
    //
  }),
  computed: mapState({
    competitions: state => state.competitions.competitions
  }),
  methods: mapActions('competitions', [
    'addCompetiton',
    'deleteCompetition'
  ]),
  created() {
    this.$store.dispatch('competitions/getCompetitions')
  }
};
</script>
