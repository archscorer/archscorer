<template>
  <v-list>
    <v-subheader v-if="events.length === 0">No events found in the database</v-subheader>
    <v-list-item v-for="event in events" :key="'event' + event.id">
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
            <v-btn color="primary" :to="{ name: 'event', params: { 'id': event.id}}">Enter</v-btn>
          </v-card-actions>
        </v-card>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    computed: {
      ...mapState({
        events: state => state.events.events,
      })
    },
    created() {
      this.$store.dispatch('events/getEvents')
    }
  }
</script>
