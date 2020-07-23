<template>
  <v-card class="mt-5">
    <v-card-title>Records
      <v-spacer />
      <v-text-field
        v-model="r_search"
        append-icon="mdi-magnify"
        label="Filter"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-card-text>
      <v-data-table
        dense
        :mobile-breakpoint="300"
        :headers="r_table_header"
        :search="r_search"
        :items="r_table"
        :items-per-page="50"
        multi-sort
      >
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState } from 'vuex'

  export default {
    // name: 'Series',
    components: {
    },
    data: () => ({
      r_search: ''
    }),
    computed: {
      ...mapState({
        records: state => state.statistics.records
      }),
      r_table_header() {
        return [
          { text: 'Round', value: 'round' },
          { text: 'Class', value: 'class' },
          { text: 'Score', value: 'score' },
          { text: 'Archer', value: 'archer'},
          { text: 'Event', value: 'event' },
          { text: 'EE/EU/W', value: 'scope' },
          { text: 'Date', value: 'date', width: '120px'},
        ]
      },
      r_table() {
        if (this.records.length) {
          return this.records.map(record => {
            record.class = record.age_group + record.gender + record.style
            return record
          })
        }
        return []
      },
    },
    created() {
      this.$store.dispatch('statistics/getRecords')
    }
  }
</script>
