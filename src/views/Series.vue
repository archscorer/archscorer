<template>
  <v-container>
    <v-card>
      <v-card-text class="pt-8 mt-5">
        <SeriesList/>
        <small><p>series created by you are marked with '*'</p></small>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
  // import SeriesAdd from '@/components/SeriesAdd.vue'
  import SeriesList from '@/components/SeriesList.vue'

  export default {
    name: 'Series',
    components: {
      SeriesList
    },
    data: () => ({
      //
    })
  };
</script>
