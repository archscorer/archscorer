<template>
  <v-card class="mt-5">
    <v-card-title>Records
      <v-spacer />
      <v-text-field
        v-model="r_search"
        append-icon="mdi-magnify"
        label="Search"
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
        <template v-slot:header.class="{ header }">
          {{ header.text }}
          <v-menu offset-y :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon small :color="classs ? 'primary' : ''">
                  mdi-filter
                </v-icon>
              </v-btn>
            </template>
            <div style="background-color: white; width: 280px">
              <v-text-field v-model="classs" class="pa-4" type="text" label="Enter the class"></v-text-field>
              <v-btn @click="classs = ''" small text color="primary" class="ml-2 mb-2">Clean</v-btn>
            </div>
          </v-menu>
        </template>
        <template v-slot:header.score="{ header }">
          {{ header.text }}
          <v-menu offset-y :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon small :color="scoreFrom ? 'primary' : ''">
                  mdi-filter
                </v-icon>
              </v-btn>
            </template>
            <div style="background-color: white; width: 280px">
              <v-menu
                v-model="start_score"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="scoreFrom" class="pa-4" type="number" label="Enter the min score"></v-text-field>
                </template>
              </v-menu>
              <v-menu
                v-model="end_score"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="scoreTo" class="pa-4" type="number" label="Enter the max score"></v-text-field>
                </template>
              </v-menu>
              <v-btn @click="scoreFrom = 0, scoreTo = 10000" small text color="primary" class="ml-2 mb-2">Clean</v-btn>
            </div>
          </v-menu>
        </template>
        <template v-slot:header.archer="{ header }">
          {{ header.text }}
          <v-menu offset-y :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon small :color="archer ? 'primary' : ''">
                  mdi-filter
                </v-icon>
              </v-btn>
            </template>
            <div style="background-color: white; width: 280px">
              <v-text-field v-model="archer" class="pa-4" type="text" label="Enter the archer name"></v-text-field>
              <v-btn @click="archer = ''" small text color="primary" class="ml-2 mb-2">Clean</v-btn>
            </div>
          </v-menu>
        </template>
        <template v-slot:header.event="{ header }">
          {{ header.text }}
          <v-menu offset-y v-model="event_dialog" :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon small :color="event ? 'primary' : ''">
                  mdi-filter
                </v-icon>
              </v-btn>
            </template>
            <div style="background-color: white; width: 280px">
              <v-text-field v-model="event" class="pa-4" type="text" label="Enter the event name"></v-text-field>
              <v-btn @click="event = ''" small text color="primary" class="ml-2 mb-2">Clean</v-btn>
              <v-btn text small color="primary" class="ml-2 mb-2" @click="event_dialog = false">Close</v-btn>
            </div>
          </v-menu>
        </template>
        <template v-slot:header.scope="{ header }">
          {{ header.text }}
          <v-menu offset-y :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon small :color="scope ? 'primary' : ''">
                  mdi-filter
                </v-icon>
              </v-btn>
            </template>
            <div style="background-color: white; width: 280px">
              <v-text-field v-model="scope" class="pa-4" label="Enter the date from"></v-text-field>
              <v-btn @click="scope = ''" small text color="primary" class="ml-2 mb-2">Clean</v-btn>
            </div>
          </v-menu>
        </template>
        <template v-slot:header.date="{ header }">
          {{ header.text }}
          <v-menu v-model="date_menu" offset-y :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon small :color="date ? 'primary' : ''">
                  mdi-filter
                </v-icon>
              </v-btn>
            </template>
            <div style="background-color: white" class="pa-5">
              <v-menu
                v-model="start_date"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="from_date"
                    label="From date"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="from_date"
                  @input="start_date = false"
                ></v-date-picker>
              </v-menu>
              <v-menu
                v-model="end_date"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="to_date"
                    label="To date"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="to_date"
                  @input="end_date = false"
                ></v-date-picker>
              </v-menu>
              <v-btn text small color="primary" class="ml-2 mb-2" @click="date_menu = false">OK</v-btn>
            </div>
          </v-menu>
        </template>
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
      classs: '',
      scoreFrom: 0,
      scoreTo: 100000,
      start_score: false,
      end_score: false,
      archer: '',
      event: '',
      scope: '',
      date_menu: false,
      start_date: false,
      end_date: false,
      from_date: (new Date( '01 02 1900')).toISOString().substr(0, 10),
      to_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
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
                      this.classs != null &&
                      value.toString().toLowerCase().indexOf(this.classs.toLowerCase()) !== -1
            },
            width: '100px' },
          { text: 'Score', value: 'score',
            filter: value => {
              return value != null &&
                      this.scoreFrom != null &&
                      this.scoreTo != null &&
                      value > parseInt(this.scoreFrom) && value <= parseInt(this.scoreTo)
            }
          },
          { text: 'Archer', value: 'archer',
            filter: value => {
              return value != null &&
                      this.archer != null &&
                      value.toString().toLowerCase().indexOf(this.archer.toLowerCase()) !== -1
            },
            width: '175px' },
          { text: 'Event', value: 'event',
            filter: value => {
              return value != null &&
                      this.event != null &&
                      value.toString().toLowerCase().indexOf(this.event.toLowerCase()) !== -1
            }
          },
          { text: 'national/EU/W', value: 'scope',
            filter: value => {
              return value != null &&
                      this.scope != null &&
                      value.toString().toLowerCase().indexOf(this.scope.toLowerCase()) !== -1
            }
          },
          { text: 'Date', value: 'date',
            filter: value => {
              return value != null &&
                      this.from_date != null &&
                      this.to_date != null &&
                      value > this.from_date && value < this.to_date
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
