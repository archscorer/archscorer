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
      <v-row>
        <v-col>
          <v-select
            v-model="group_by"
            dense
            :items="[{ text: '--disabled--', value: null },
                    { text: 'Format', value: 'format'},
                    { text: 'Class', value: 'class'}]"
            label="organise archers by">
          </v-select>
        </v-col>
      </v-row>
      <v-data-table
        dense
        :mobile-breakpoint="300"
        :headers="r_table_header"
        :search="r_search"
        :items="r_table"
        :items-per-page="50"
        :group-by="group_by"
        multi-sort
      >
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    // name: 'Series',
    components: {
    },
    data: () => ({
      r_search: '',
      format: {
        'hunter': 'IFAA Hunter',
        'field': 'IFAA Field',
        'animal': 'IFAA Animal (Marked distances)',
        'flint': 'IFAA Flint Indoor',
        'indoor': 'IFAA Indoor'
      },
      group_by: 'format'
    }),
    computed: {
      ...mapState({
        records: state => state.statistics.records
      }),
      r_table_header() {
        return [
          { text: 'Format', value: 'format' },
          { text: 'Class', value: 'class', width: '100px' },
          { text: 'Score', value: 'score' },
          { text: 'Archer', value: 'archer', width: '175px' },
          { text: 'Event', value: 'event' },
          { text: 'national/EU/W', value: 'scope' },
          { text: 'Date', value: 'date', width: '120px'},
        ]
      },
      r_table() {
        if (this.records.length) {
          return this.records.map(record => {
            return Object.assign(
              { class: record.age_group + record.gender + record.style },
              record,
              { format: this.format[record.format] }
            )
          })
        }
        return []
      },
    }
  }
</script>

<style scoped>
  .v-select {
    max-width: 120px;
  }
</style>
