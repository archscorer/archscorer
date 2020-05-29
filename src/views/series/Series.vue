<template>
  <v-container v-if="s">
    <v-layout
      text-center
      wrap
    >
      <v-card>
        <v-card-title v-text="s.name"></v-card-title>
        <v-card-text>
          <p v-text="s.description"></p>
          <seriesSummary/>
        </v-card-text>
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
</style>
