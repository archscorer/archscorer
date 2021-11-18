<template>
  <v-container>
    <v-layout class="d-flex justify-space-around"
      wrap
    >
      <Records/>
    </v-layout>
  </v-container>
</template>

<script>
  import Records from '@/components/statistics/Records.vue'

  export default {
    name: 'StatisticsRecords',
    components: {
      Records,
    },
    data: () => ({
      //
    }),
  };
</script>
