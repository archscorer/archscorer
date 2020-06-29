<template>
  <v-container>
    <v-list subheader dense class="my-2" v-for="(e_group, label) in events_list"
      :key="label"
      >
      <v-subheader class="text-overline font-weight-black" v-if="e_group.length">{{ (label === 'ongoing' ? 'Held today' : label + ' events') }}</v-subheader>
      <v-list-item v-for="event in e_group"
        :key="'event' + event.id"
        :to="{ name: 'event', params: { 'id': event.id}}"
        >
        <v-list-item-content>
          <v-list-item-title>{{ event.name }} <span class="text-overline">{{ event.indays ? event.indays : '' }}</span> {{ event.creator == user.email ? '*' : '' }}</v-list-item-title>
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
          <v-chip small v-if="event.type !== 'open'" v-text="event.type" :color="chip_color(event.type)"></v-chip>
          <v-chip small v-for="tag of tags(event)" :key="tag.label" v-text="tag.label" :color="tag.color"></v-chip>
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
              event.indays = (diffDays > 1 ? ' (in ' + diffDays + ' days)' : ' (tomorrow)')
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
        return type === 'private' ? 'primary' : type === 'club' ? 'secondary' : ''
      },
      tags(e) {
        if (e.tags) {
          return e.tags.split(',').map(tag => {
            let [l, c] = tag.split('|')
            return {label: l, color: c}
          })
        }
        return []
      }
    },
    created() {
      this.$store.dispatch('events/getEvents')
    }
  }
</script>
