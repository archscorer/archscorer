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
      :loading="loading"
      group-by="class"
      multi-sort
      :items-per-page="50"
    >
      <template v-slot:group="props">
        <tr class="v-row-group__header">
          <td :colspan="props.headers.length">{{ props.group }}</td>
        </tr>
        <tr v-for="row in props.items" :key="row.id">
          <td v-for="col in props.headers" :key="col.text">
            <template v-if="col.value === 'name'">
              <v-btn icon @click="participant_sc(row.id)" small>
                <v-icon size="16">mdi-book-open-outline</v-icon>
              </v-btn>
            </template>
            {{ row[col.value] }}
            <template v-if="'pr'+col.value in row && event.archive === false">
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
    <v-dialog v-model="sc_dialog" max-width="650px">
      <v-card v-if="participant !== null">
        <v-card-title>{{ participant.archer.full_name }} {{ participant.class}} {{ participant.archer.club }}</v-card-title>
        <v-card-subtitle>{{ event.name }}</v-card-subtitle>
        <v-card-text>
          <eventParticipantScorecards :participant="participant" :rounds="event.rounds" :edit="sc_edit()"/>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn text @click="sc_dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
  import eventParticipantScorecards from '@/components/event/eventParticipantScorecards.vue'
  import rankingService from '@/services/rankingService'
  import { mapState } from 'vuex'



  function getScore(r, p) {
    let r_sc = p.scorecards.find(obj => obj.round === r.id)
    return r_sc ?  r_sc.arrows.map(a => a.score) : [null]
  }

  function getX(r, p) {
    let r_sc = p.scorecards.find(obj => obj.round === r.id)
    return r_sc ?  r_sc.arrows.map(a => a.x ? 1 : 0) : [null]
  }

  export default {

    components: {
      eventParticipantScorecards,
    },
    data: () => ({
      r_search: '',
      sc_dialog: false,
      loading: false,
      participant: null,
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
            { text: 'Place', value: 'place', width: '1%' },
            { text: 'Name', value: 'name' },
            { text: 'Club', value: 'club' },
            { text: 'Class', value: 'class' },
          ]
          header.push(...this.event.rounds.map(function(r) {
            return { text: r.ord.toString() + '. ' + r.label,
                    value: r.ord.toString(),
                    class: 'round-header'}
          }))
          header.push({ text: 'x', value: 'x', width: '1%' })
          header.push({ text: 'Sum', value: 'sum', width: '1%' })

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
              id: p.id,
              name: p.archer.full_name,
              class: p.age_group + p.archer.gender + p.style,
              club: p.archer.club
            }
            let sums = this.rounds.map(function(r) {
              row[r.ord] = rankingService.sum( getScore(r, p) )
              if (r.course_name.search('shootoff') !== -1) {
                if (row[r.ord] > 0) {
                  row.shootoff = row[r.ord]
                }
                return 0
              }
              return row[r.ord]
            })
            row['sum'] = sums.length ? rankingService.sum( sums ) : 0
            let x = this.rounds.map(function(r) {
              if (r.course_name.search('shootoff') !== -1) {
                return 0
              }
              return rankingService.sum( getX(r, p) )
            })
            row['x'] = x.length ? rankingService.sum( x ) : 0
            this.rounds.map(function (r) {
              let r_sc = getScore(r, p)
              row['pr' + r.ord] = (r_sc.filter(obj => obj !== null).length / r_sc.length) * 100
            })
            return row
          }, this.event)
          rankingService.participantRank(r_table)
          return r_table
        } else {
          return []
        }
      },
    },
    methods: {
      update_r_table() {
        this.loading = true
        this.$store.dispatch('events/updateEvent', this.event.id).then(() => {
          this.loading = false
        })
      },
      participant_sc(pId) {
        this.participant = this.event.participants.find(obj => obj.id === pId)
        this.participant['class'] = this.participant.age_group + this.participant.archer.gender + this.participant.style
        this.sc_dialog = true
      },
      sc_edit() {
        return [this.event.creator, ...this.event.admins].includes(this.user.email) && !this.event.archive
      }
    }
  }
</script>

<style scoped>
  td {
    white-space: nowrap;
  }
</style>
