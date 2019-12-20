<template>
  <v-card>
    <v-card-title>
      <v-btn @click="update_r_table()" icon><v-icon>mdi-refresh</v-icon></v-btn>
      <small>Results</small>
      <v-spacer />
      {{ event.name }}
      <v-spacer />
      <v-text-field
        v-model="r_search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :mobile-breakpoint="300"
      dense
      :headers="r_table_header"
      :items="r_table"
      :search="r_search"
      group-by="class"
      multi-sort
      :items-per-page="50"
    >
      <template v-slot:group="props">
        <tr class="v-row-group__header">
          <td :colspan="props.headers.length">{{ props.group }}</td>
        </tr>
        <tr v-for="row in props.items" :key="row.class + ':' + row.name">
          <td v-for="col in props.headers" :key="col.text">
            {{ row[col.value] }}
            <template v-if="'pr'+col.value in row">
              <v-progress-circular
                v-model="row['pr'+col.value]"
                :color="row['pr'+col.value] === 100 ? 'green' : 'error'"
                width="1"
                size="12">
              </v-progress-circular>
            </template>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>

  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

  import { mapState} from 'vuex'

  function sum(arr) {
    return arr.reduce((sum, x) => sum + x);
  }

  function getScore(r, p) {
    let r_sc = p.scorecards.find(obj => obj.round === r.id)
    return r_sc ?  r_sc.arrows.map(a => a.score) : [null]
  }

  function cSumSc( a, b ) {
    if ( a.sum > b.sum ){
      return -1;
    }
    if ( a.sum < b.sum ){
      return 1;
    }
    return 0;
  }

  export default {

    data: () => ({
      r_search: '',
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      r_table_header() {
        if (this.event) {
          let header = [
            { text: 'Name', value: 'name' },
            { text: 'Class', value: 'class' },
          ]
          header.push(...this.event.rounds.map(function(r) {
            return { text: r.ord.toString() + '. ' + r.label,
                    value: r.ord.toString() }
          }))
          header.push({ text: 'Sum', value: 'sum'})

          return header
        } else {
            return [
              { text: 'Name', value: 'name' },
              { text: 'Class', value: 'class' },
              { text: 'Round', value: 'round'},
            ]
        }
      },
      r_table() {
        if (Array.isArray(this.event.participants)) {
          let r_table = this.event.participants.map(function(p) {
            let row = {
              name: p.archer.full_name,
              class: p.age_group + p.archer.gender + p.style,
            }
            let sums = this.rounds.map(function(r) {
              row[r.ord] = sum( getScore(r, p) )
              return row[r.ord]
            })
            row['sum'] = sums.length ? sum( sums ) : 0

            this.rounds.map(function (r) {
              let r_sc = getScore(r, p)
              row['pr' + r.ord] = (r_sc.filter(obj => obj !== null).length / r_sc.length) * 100
            })
            return row
          }, this.event)
          return r_table.sort( cSumSc )
        } else {
          return []
        }
      },
    },
    methods: {
      update_r_table() {
        this.$store.dispatch('events/updateEvent', this.event.id)
      }
    }
  }
</script>
