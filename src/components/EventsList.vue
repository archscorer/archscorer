<template>
  <v-list>
    <v-subheader v-if="events.length === 0">No events found in the database</v-subheader>
    <v-list-item v-for="(event, index) in events" :key="index">
      <v-list-item-content>
        <v-list-item-title v-text="event.name"></v-list-item-title>
        <v-list-item-subtitle>
          <template v-if="event.date_start != event.date_end">
            from {{ event.date_start }} to {{ event.date_end }}
          </template>
          <template v-else>
            on {{ event.date_start }}
          </template>
        </v-list-item-subtitle>
        <v-card>
          <v-card-actions>
            <ListEventsRegister v-bind:comp_id="event.id"/>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="deleteEvent(event.id)">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
  import ListEventsRegister from '@/components/EventsListRegister.vue'
  import { mapState, mapActions } from 'vuex'

  export default {
    components: {
      ListEventsRegister
    },
    computed: {
      ...mapState({
        events: state => state.events.events
      })
    },
    methods: {
      ...mapActions('events', [
        'deleteEvent'
      ])
    },
    created() {
      this.$store.dispatch('events/getEvents')
    }
  }
</script>