<template>
  <v-container>
    <v-row dense>
      <v-col cols="12">
      <v-card>
        <v-card-title>Events</v-card-title>
        <v-card-actions>
            <AddCompetiton/>
        </v-card-actions>
      </v-card>
      </v-col>
      <v-col cols="12">
      <v-card>
        <v-card-title>Browse</v-card-title>
        <ListEvents/>
      </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import AddCompetiton from '@/components/EventsAdd.vue'
  import ListEvents from '@/components/EventsList.vue'

  export default {
    name: 'Events',
    components: {
      AddCompetiton,
      ListEvents
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
