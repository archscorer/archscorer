<template>
  <v-container>
    <v-layout class="d-flex justify-space-around"
      wrap
    >
      <v-card>
        <v-card-text>
          <p>Work in progress. Ideas what kind of statistics or graphs to collect
            or show would be most wolcome.</p>
        </v-card-text>
      </v-card>
      <ArcherPastEvents v-if="user.id !== null"/>
    </v-layout>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'

  import ArcherPastEvents from '@/components/statistics/ArcherPastEvents.vue'

  export default {
    name: 'ArcherEvents',
    components: {
      ArcherPastEvents,
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
