<template>
  <v-container v-if="s">
    <v-layout
      wrap
    >
      <v-card>
        <v-card-title v-text="s.name"></v-card-title>
        <v-card-text>
          <p v-html="series_desciption"></p>
        </v-card-text>
        <seriesSummary/>
      </v-card>
    </v-layout>
  </v-container>
  <v-overlay v-else>
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-overlay>
</template>

<script>
  import seriesSummary from '@/components/series/seriesSummary.vue'
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
        return this.s.description.split('\n\n').join('</p><p>').split('\n').join('<br/>')
      },
      s() {
        return this.$store.getters['series/seriesById'](parseInt(this.$route.params.id))
      },
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
