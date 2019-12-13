<template>
  <v-container>
    <v-card>
      <v-card-text class="pt-8 mt-5">
        <EventsList/>
        <small><p>events created by you are marked with '*'</p></small>
        <EventsAdd/>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
  import EventsAdd from '@/components/EventsAdd.vue'
  import EventsList from '@/components/EventsList.vue'

  export default {
    name: 'Events',
    components: {
      EventsAdd,
      EventsList
    },
    data: () => ({
      //
    })
  };
</script>
