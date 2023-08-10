<template>
  <v-container>
    <v-card>
      <v-card-text>
        <p>Work in progress. Ideas what kind of statistics or graphs to collect
          or show would be most wolcome.</p>
      </v-card-text>
    </v-card>
    <ArcherPastRounds v-if="user.id !== null"/>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'

  import ArcherPastRounds from '@/components/statistics/ArcherPastRounds.vue'

  export default {
    name: 'ArcherRounds',
    components: {
      ArcherPastRounds,
    },
    data: () => ({
      //
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
    },
  };
</script>
