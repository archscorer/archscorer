<template>
  <v-container v-if="event">
    <v-tabs v-model="tab" grow>
      <v-tab v-for="label in tabs" :key="label">
        {{ label }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <eventResults/>
      </v-tab-item>
      <v-tab-item>
        <eventScoring :p_user="p_user"/>
      </v-tab-item>
      <v-tab-item>
        <eventParticipantList :p_user="p_user"/>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
  <v-overlay v-else>
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-overlay>
</template>

<script>
  import eventParticipantList from '@/components/event/eventParticipantList.vue'
  import eventResults from '@/components/event/eventResults.vue'
  import eventScoring from '@/components/event/eventScoring.vue'
  import { mapState } from 'vuex'

  export default {
    // name: 'Event',
    components: {
      eventParticipantList,
      eventResults,
      eventScoring,
    },
    props: {
      action: String,
    },
    data: () => ({
      tab: null,
      tabs: ['Results', 'Scoring', 'Participants']
    }),
    computed: {
      ...mapState({
        user: state => state.user.user
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      p_user() {
        let p_user = null
        if (Array.isArray(this.event.participants)) {
          p_user = this.event.participants.find(obj => obj.archer.id === this.user.archer.id)
        }
        return p_user ? p_user : null
      },
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('events/updateEvent', parseInt(this.$route.params.id))
      if (this.action === 'register') this.tab = 2
    }
  }
</script>

<style>
</style>
