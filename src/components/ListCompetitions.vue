<template>
  <v-list>
    <v-subheader v-if="competitions.length === 0">No competitions found in the database</v-subheader>
    <v-list-item v-for="(competition, index) in competitions" :key="index">
      <v-list-item-content>
        <v-list-item-title v-text="competition.name"></v-list-item-title>
        <v-list-item-subtitle>
          <template v-if="competition.date_start != competition.date_end">
            from {{ competition.date_start }} to {{ competition.date_end }}
          </template>
          <template v-else>
            on {{ competition.date_start }}
          </template>
        </v-list-item-subtitle>
        <v-card>
          <v-card-actions>
            <ListCompetitionsRegister v-bind:comp_id="competition.id"/>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="deleteCompetition(competition.id)">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
  import ListCompetitionsRegister from '@/components/ListCompetitionsRegister.vue'
  import { mapState, mapActions } from 'vuex'

  export default {
    components: {
      ListCompetitionsRegister
    },
    computed: {
      ...mapState({
        competitions: state => state.competitions.competitions
      })
    },
    methods: {
      ...mapActions('competitions', [
        'deleteCompetition'
      ])
    },
    created() {
      this.$store.dispatch('competitions/getCompetitions')
    }
  }
</script>
