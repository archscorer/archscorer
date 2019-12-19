<template>
  <v-list>
    <v-subheader v-if="events.length === 0">No events found in the database</v-subheader>
    <v-list-item v-for="event in events"
      :key="'event' + event.id"
      :to="{ name: 'event', params: { 'id': event.id}}"
      >
      <v-list-item-content>
        <v-list-item-title>{{ event.name }} {{ event.creator == user.email ? '*' : '' }}</v-list-item-title>
        <v-list-item-subtitle>
          <template v-if="event.date_start != event.date_end">
            from {{ event.date_start }} to {{ event.date_end }}
          </template>
          <template v-else>
            on {{ event.date_start }}
          </template>
          / {{ event.participants }} participant(s)
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-action>
        <v-chip v-if="event.type !== 'private'" v-text="event.type" :color="chip_color(event.type)"></v-chip>
      </v-list-item-action>
    </v-list-item>
  </v-list>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    computed: {
      ...mapState({
        events: state => state.events.events,
        user: state => state.user.user,
      }),
    },
    methods: {
      chip_color(type) {
        return type === 'open' ? 'primary' : type === 'club' ? 'secondary' : ''
      }
    },
    created() {
      this.$store.dispatch('events/getEvents')
    }
  }
</script>
