<template>
  <v-container>
    <v-card class="my-2">
      <v-card-actions>
        <eventParticipantRegister/>
        <v-spacer />
        <v-btn v-if="user.email === (event ? event.creator: '')" color="error" @click="deleteEvent(event.id); $router.push('/events')">Delete</v-btn>
      </v-card-actions>
    </v-card>
    <v-card>
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
          <eventScoring/>
        </v-tab-item>
        <v-tab-item>
          <eventParticipantList/>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script>
  import eventParticipantList from '@/components/event/eventParticipantList.vue'
  import eventParticipantRegister from '@/components/event/eventParticipantRegister.vue'
  import eventResults from '@/components/event/eventResults.vue'
  import eventScoring from '@/components/event/eventScoring.vue'
  import { mapState, mapActions } from 'vuex'

  export default {
    // name: 'Event',
    components: {
      eventParticipantList,
      eventParticipantRegister,
      eventResults,
      eventScoring,
    },
    data: () => ({
      tab: null,
      tabs: ['Results', 'Scoring', 'Participants']
    }),
    watch: {
      event: {
        handler() {
          if (this.event.is_open) this.tab = 2
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
    },
    methods: {
      ...mapActions('events', [
        'deleteEvent'
      ])
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('events/updateEvent', parseInt(this.$route.params.id))
    }
  }
</script>

<style>
</style>
