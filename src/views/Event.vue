<template>
  <v-container>
    <v-card class="my-2">
      <v-card-actions>
        <eventParticipantRegister v-bind:id="parseInt($route.params.id)"/>
      </v-card-actions>
    </v-card>
    <eventParticipantList v-bind:id="parseInt($route.params.id)"/>
  </v-container>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import eventParticipantRegister from '@/components/event/eventParticipantRegister.vue'
  import eventParticipantList from '@/components/event/eventParticipantList.vue'

  export default {
    // name: 'Event',
    watch: {
      $route(to, from) {
        // this does not seem to do what I expect
        // it is called when addressbar change is made, but router link click
        // does not call this code
        console.log('oh no', to, from)
      }
    },
    components: {
      eventParticipantRegister,
      eventParticipantList,
    },
    data: () => ({
      //
    }),
    created() {
      //do something after creating vue instance
      this.$store.dispatch('events/getEvents')
    }
  }
</script>

<style>
</style>
