<template>
  <v-container v-if="s">
    <v-card>
      <v-card-title>{{ s.name }}</v-card-title>
      <v-card-text>
        <p v-html="series_desciption"></p>
        <template v-if="s_table.body.length">
          <h3>Stages:</h3>
          <v-data-table
            dense
            :mobile-breakpoint="300"
            :headers="s_table.header"
            :items="s_table.body"
            hide-default-header
            hide-default-footer>
            <template v-slot:item.event="{ item }">
              <router-link :to="{ name: 'event', params: { 'id': item.eId }}">{{ item.event }}</router-link>
            </template>
          </v-data-table>
        </template>
      </v-card-text>
      <seriesSummary/>
    </v-card>
  </v-container>
  <v-overlay v-else>
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-overlay>
</template>

<script>
  import seriesSummary from '@/components/series/seriesSummary.vue'
  import DOMPurify from 'dompurify'
  import { mapState } from 'vuex'

  export default {
    // name: 'Event',
    components: {
      seriesSummary,
    },
    data: () => ({
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
      series_desciption() {
        // TODO this is probably temp fix. See event description for additional details
        return DOMPurify.sanitize(this.s.description.split('\n\n').join('</p><p>').split('\n').join('<br/>'))
      },
      s() {
        return this.$store.getters['series/seriesById'](parseInt(this.$route.params.id))
      },
      s_table() {
        if (this.s && this.s.stages) {
          return {
            header: [
              { text: 'Event', value: 'event' },
              { text: 'Date', value: 'date' },
              { text: 'Participants', value: 'participants'}
            ],
            body: this.s.stages.reverse().map(stage => {
              let p_count = stage.participants.length
              return {
                event: stage.name,
                eId: stage.id,
                date: stage.date_start,
                participants: (p_count && p_count > 1 ? p_count + ' participants' : '')
              }
            })
          }
        } else {
          return {
            header: [],
            body: []
          }
        }
      }
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('series/updateSeries', parseInt(this.$route.params.id)).catch(() => {
        this.$router.push('/series')
      })
    }
  }
</script>

<style>
  th.stage-header {
    max-width: 90px;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>
