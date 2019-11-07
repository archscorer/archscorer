<template>
  <v-container>
    <v-row dense>
      <v-col cols="12">
      <v-card>
        <v-card-title>Competitions</v-card-title>
        <v-card-actions>
            <AddCompetiton/>
        </v-card-actions>
      </v-card>
      </v-col>
      <v-col cols="12">
      <v-card>
        <v-card-title>Browse</v-card-title>
        <ListCompetitions/>
      </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import AddCompetiton from '@/components/AddCompetition.vue'
  import ListCompetitions from '@/components/ListCompetitions.vue'

  export default {
    name: 'Competitions',
    components: {
      AddCompetiton,
      ListCompetitions
    },
    data: () => ({
      //
    })
  };
</script>

<style>
  .v-input__prepend-outer {
    margin-top: 0.55rem;
  }
</style>
