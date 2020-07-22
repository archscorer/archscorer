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
      <UserPastEvents v-if="user.id !== null"/>
      <Records/>
    </v-layout>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'

  import UserPastEvents from '@/components/statistics/UserPastEvents.vue'
  import Records from '@/components/statistics/Records.vue'

  export default {
    name: 'Statistics',
    components: {
      UserPastEvents,
      Records,
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
