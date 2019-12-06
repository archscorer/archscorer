<template>
  <v-container>
    <v-card>
      <v-card-text class="py-8">
        <ListEvents/>
        <small><p>events created by you are marked with '*'</p></small>
        <AddCompetiton/>
      </v-card-text>
    </v-card>
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
