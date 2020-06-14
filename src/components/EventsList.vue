<template>
  <v-container>
    <v-list subheader dense v-for="(e_group, label) in events_list"
      :key="label"
      :color="(label === 'ongoing' ? '#EBF5FB': '')"
      >
      <v-subheader class="overline font-weight-black" v-if="e_group.length">{{ label }} events</v-subheader>
      <v-list-item v-for="event in e_group"
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
            / {{ Array.isArray(event.participants) ? event.participants.length : event.participants }} participant(s)
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-chip v-if="event.type !== 'private'" v-text="event.type" :color="chip_color(event.type)"></v-chip>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    computed: {
      ...mapState({
        events: state => state.events.events,
        user: state => state.user.user,
      }),
      events_list() {
        let e_list = {
          upcoming: [],
          ongoing: [],
          past: []
        }
        if (this.events) {
          for (let event of this.events) {
            if (new Date(event.date_start) > new Date()) {
              let diffDays = Math.ceil(Math.abs(new Date(event.date_start) - new Date()) / (1000 * 60 * 60 * 24));
              event.name = event.name + (diffDays > 1 ? ' (in ' + diffDays + ' days)' : ' (tomorrow)')
              e_list.upcoming.push(event)
            } else if (new Date(event.date_end).setHours(23, 59) < new Date()) {
              e_list.past.push(event)
            } else {
              e_list.ongoing.push(event)
            }
          }
        }
        return e_list
      }
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
