<template>
  <v-container>
    <v-card class="my-2">
      <v-card-actions>
        <eventParticipantRegister/>
      </v-card-actions>
    </v-card>
    <v-card>
      <v-tabs
        v-model="tab"
        grow
      >
        <v-tab
          v-for="label in tabs"
          :key="label"
        >
          {{ label }}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item>
          <eventResults/>
        </v-tab-item>
        <v-tab-item>
          <eventParticipantList/>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import eventParticipantRegister from '@/components/event/eventParticipantRegister.vue'
  import eventResults from '@/components/event/eventResults.vue'
  import eventParticipantList from '@/components/event/eventParticipantList.vue'

  export default {
    // name: 'Event',
    watch: {
      // $route(to, from) {
      //   // this does not seem to do what I expect
      //   // it is called when addressbar change is made, but router link click
      //   // does not call this code
      //   // console.log('oh no', to, from)
      // }
    },
    components: {
      eventParticipantRegister,
      eventResults,
      eventParticipantList,
    },
    data: () => ({
      tab: null,
      tabs: ['Results', 'Participants']
    }),
    created() {
      //do something after creating vue instance
      this.$store.dispatch('events/getEvents')
    }
  }
</script>

<style>
</style>
