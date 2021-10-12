<template>
  <v-container v-if="event" :class="{'px-0': $vuetify.breakpoint.xsOnly}">
    <v-tabs v-model="tab" grow>
      <v-tab v-for="label in tabs" :key="label">
        {{ label }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab" touchless>
      <v-tab-item>
        <v-sheet class="py-5">
          <h1 v-text="event.name"></h1>
          <v-subheader>Event details</v-subheader>
            <template>
              <v-tabs v-model="description">
                <v-tab v-for="description in event.descriptions">
                  {{ description.language }}
                </v-tab>
              </v-tabs>
            </template>
          <v-tabs-items v-model="description" touchless>
            <v-tab-item v-for="description in event.descriptions">
              <div class="ma-5">{{ description.description }}</div>
              <v-card flat>
                <v-card-text></v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-sheet>
        <v-list dense>
          <v-subheader>Rounds</v-subheader>
          <v-list-item v-for="round in event.rounds" :key="'round_' + round.id">
            <v-list-item-title>
              {{ round.ord }}. {{ round.label }} ({{ round.course_details.name }})
            </v-list-item-title>
          </v-list-item>
        </v-list>
        <eventParticipantList :p_user="p_user"/>
      </v-tab-item>
      <v-tab-item>
        <eventResults/>
      </v-tab-item>
      <v-tab-item v-if="!event.archive">
        <eventScoring :p_user="p_user"/>
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
      description: []
    }),
    watch: {
      tab: {
        handler () {
          if (this.tab === 1) this.$store.dispatch('events/updateEvent', parseInt(this.$route.params.id))
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      tabs() {
        if (this.event && this.event.archive) {
          return ['Overview', 'Results']
        }
        return ['Overview', 'Results', 'Scoring']
      },
      p_user() {
        let p_user = null
        if (Array.isArray(this.event.participants)) {
          if ([this.event.creator, ...this.event.admins].includes(this.user.email)) {
            p_user = this.event.participants
          } else {
            p_user = this.event.participants.filter(obj => obj.archer.id === this.user.archer.id)
          }
          p_user = p_user.map(p => {
            return Object.assign(p, {text: p.group_target + (p.group ? ' ('+ p.group +')' : '') })
          })
        }
        return p_user ? p_user : null
      },
      event_desciption() {
        // TODO this is probably temp fix. some kind of html editor like https://www.vuetoolbox.com/projects/tiptap
        // or already ready made solution https://github.com/iliyaZelenko/tiptap-vuetify
        return this.event.description.split('\n\n').join('</p><p>').split('\n').join('<br/>')
      },
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('events/updateEvent', parseInt(this.$route.params.id)).catch(() => {
        this.$router.push('/events')
      })
    }
  }
</script>

<style>
  th.round-header {
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>
