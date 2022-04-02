<template>
  <v-card class="mt-5">
    <v-card-title>Records
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
        :items="r_table"
        :items-per-page="50"
        :group-by="group_by"
        multi-sort
      >
        <template v-slot:header.class="{ header }">
          {{ header.text }}
          <filterRecord v-bind:filter.sync="filters.class"/>
        </template>
        <template v-slot:header.score="{ header }">
          {{ header.text }}
          <v-menu top :close-on-content-click="false" v-model="menu_score">
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon small :color="filters.score.some(el => el !== '') ? 'primary' : ''">
                  mdi-filter
                </v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-text>
                <v-text-field autofocus v-model="filters.score[0]"
                  type="number"
                  label="Scores from"/>
              </v-card-text>
              <v-card-text>
                <v-text-field v-model="filters.score[1]"
                  type="number"
                  label="Scores to"/>
              </v-card-text>
              <v-card-actions>
                <v-btn @click="filters.score = ['', '']" small text color="primary">Clean</v-btn>
                <v-spacer/>
                <v-btn @click="menu_score = false" small text color="secondary">Close</v-btn>
              </v-card-actions>
            </v-card>
          </v-menu>
        </template>
        <template v-slot:header.archer="{ header }">
          {{ header.text }}
          <filterRecord v-bind:filter.sync="filters.archer"/>
        </template>
        <template v-slot:header.event="{ header }">
          {{ header.text }}
          <filterRecord v-bind:filter.sync="filters.event"/>
        </template>
        <template v-slot:header.scope="{ header }">
          {{ header.text }}
          <filterRecord v-bind:filter.sync="filters.scope"/>
        </template>
        <template v-slot:header.date="{ header }">
          {{ header.text }}
          <v-menu top :close-on-content-click="false" v-model="menu_date">
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon small :color="filters.date.some(el => el !== '') ? 'primary' : ''">
                  mdi-filter
                </v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-text>
                <v-menu
                  v-model="menu_date_from"
                  :close-on-content-click="false"
                  top
                  min-width="270px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="filters.date[0]"
                      label="Date from"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="filters.date[0]" @input="menu_date_from = false"></v-date-picker>
                </v-menu>
                <v-menu
                  v-model="menu_date_to"
                  :close-on-content-click="false"
                  top
                  min-width="270px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="filters.date[1]"
                      label="Date to"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="filters.date[1]" @input="menu_date_to = false"></v-date-picker>
                </v-menu>
              </v-card-text>
              <v-card-actions>
                <v-btn @click="filters.date = ['', ''];" small text color="primary">Clean</v-btn>
                <v-spacer/>
                <v-btn @click="menu_date = false" small text color="secondary">Close</v-btn>
              </v-card-actions>
            </v-card>
          </v-menu>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import filterRecord from '@/components/statistics/filterRecord.vue'
  import { mapState } from 'vuex'

  export default {
    // name: 'Series',
    components: {
      filterRecord,
    },
    data: () => ({
      filters: {class: '',
                archer: '',
                event: '',
                scope: '',
                score: ['', ''],
                date: ['', '']},
      menu_score: false,
      menu_date: false,
      menu_date_from: false,
      menu_date_to:false,
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
          { text: 'Format', value: 'format'},
          { text: 'Class', value: 'class',
            filter: value => {
              return value != null &&
                      this.filters.class != null &&
                      value.toString().toLowerCase().indexOf(this.filters.class.toLowerCase()) !== -1
            },
            width: '100px' },
          { text: 'Score', value: 'score',
            filter: value => {
              if (this.filters.score.some(el => el !== '')) {
                if (this.filters.score[0] !== '' && this.filters.score[1] === '') {
                  return value >= parseInt(this.filters.score[0])
                }
                if (this.filters.score[1] !== '' && this.filters.score[0] === '') {
                  return value <= parseInt(this.filters.score[1])
                }
                if (this.filters.score.every(el => el !== '')) {
                  return parseInt(this.filters.score[0]) <= value &&
                          value <= parseInt(this.filters.score[1])
                }
              }
              return value != null
            }
          },
          { text: 'Archer', value: 'archer',
            filter: value => {
              return value != null &&
                      this.filters.archer != null &&
                      value.toString().toLowerCase().indexOf(this.filters.archer.toLowerCase()) !== -1
            },
            width: '175px' },
          { text: 'Event', value: 'event',
            filter: value => {
              return value != null &&
                      this.filters.event != null &&
                      value.toString().toLowerCase().indexOf(this.filters.event.toLowerCase()) !== -1
            }
          },
          { text: 'national/EU/W', value: 'scope',
            filter: value => {
              return value != null &&
                      this.filters.scope != null &&
                      value.toString().toLowerCase().indexOf(this.filters.scope.toLowerCase()) !== -1
            }
          },
          { text: 'Date', value: 'date',
            filter: value => {
              if (this.filters.date.some(el => el !== '')) {
                if (this.filters.date[0] !== '' && this.filters.date[1] === '') {
                  return value >= this.filters.date[0]
                }
                if (this.filters.date[1] !== '' && this.filters.date[0] === '') {
                  return value <= this.filters.date[1]
                }
                if (this.filters.date.every(el => el !== '')) {
                  return this.filters.date[0] <= value &&
                          value <= this.filters.date[1]
                }
              }
              return value != null
            },
            width: '120px'},
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
