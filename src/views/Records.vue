<template>
  <v-container>
    <Records/>
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
