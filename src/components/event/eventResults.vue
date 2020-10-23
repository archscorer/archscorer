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
    <v-card-text>
      <v-data-table
        :mobile-breakpoint="300"
        dense
        :headers="r_table.header"
        :items="r_table.data"
        :search="r_search"
        :loading="loading"
        group-by="class"
        multi-sort
        :items-per-page="4 * 28"
      >
        <template v-slot:group="props">
          <tr class="v-row-group__header">
            <td :colspan="props.headers.length">{{ props.group }}</td>
          </tr>
          <tr v-for="row in props.items" :key="row.id">
            <td v-for="col in props.headers" :key="col.text">
              <template v-if="col.value === 'name'">
                <!-- <v-btn v-if="row.records" icon @click="participant_records(row.records)" small>
                  <v-icon size="16" color="primary">mdi-star</v-icon>
                </v-btn> -->
                <v-btn icon @click="participant_sc(row.id)" small>
                  <v-icon size="16">mdi-book-open-outline</v-icon>
                </v-btn>
              </template>
              <span :class="col.value === 'sum' ? 'font-weight-medium' : ''" v-html="row[col.value]"/>
              <template v-if="'pr'+col.value in row && event.archive === false">
                <v-progress-circular
                  v-model="row['pr'+col.value]"
                  :color="row['pr'+col.value] === 100 ? 'green' : 'error'"
                  width="1"
                  size="12"
                  class='progress-text'>
                  {{ row['pr'+col.value] === 100 ? '' : row['pr'+col.value] === 0 ? '' : row['pr'+col.value] }}
                </v-progress-circular>
              </template>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card-text>
    <v-card-actions>
      <v-col>
        <p class='text-caption'>
          <template v-if="[this.event.creator, ...this.event.admins].includes(this.user.email) || this.event.archive">
            Export results to <v-btn x-small color="primary" @click="results2pdfProxy()">PDF</v-btn>
          </template>
          <template v-if="[this.event.creator, ...this.event.admins].includes(this.user.email)">
            <br />Infinite scroll loop
              <v-btn  x-small color="secondary" @click="scroll_loop=(scroll_loop ? false : true)">
                {{ scroll_loop ? 'End' : 'Start' }}
              </v-btn>
          </template>
        </p>
      </v-col>
    </v-card-actions>
    <v-dialog v-model="sc_dialog" max-width="650px">
      <v-card v-if="participant !== null">
        <v-card-title>{{ participant.archer.full_name }} {{ participant.class}} {{ participant.archer.club_details.name_short }}</v-card-title>
        <v-card-subtitle>{{ event.name }}</v-card-subtitle>
        <v-card-text>
          <eventParticipantScorecards :pId="participant.id"
                                      :eId="event.id"
                                      :rounds="event.rounds"
                                      :edit="sc_edit()"/>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn text @click="sc_dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- <v-dialog v-model="records_dialog" max-width="650px">
      <v-card>
        <v-card-title>New records</v-card-title>
        <v-card-text>
          <v-row v-for="(rec, i) in new_records" :key="'rec_' + i">
            <v-col v-for="(attr, j) in ['archer','format','class','score','scope']" :key="'rec_' + i + '_' + j">{{ rec[attr] }}</v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn text @click="records_dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog> -->
    <v-btn v-if="scroll_loop"
      @click="scroll_loop = false"
      color="error"
      fixed
      dark
      bottom
      right
      fab
    ><v-icon>mdi-stop</v-icon></v-btn>
  </v-card>
</template>

<script>
  import { mapState } from 'vuex'

  import eventParticipantScorecards from '@/components/event/eventParticipantScorecards.vue'
  import rankingService from '@/services/rankingService'
  import pdfService from '@/services/pdfService'


  function getScore(r, p) {
    let r_sc = p.scorecards.find(sc => sc.round === r.id)
    return r_sc ?  r_sc.arrows.map(a => a.score) : [null]
  }

  function getSpots(r, p) {
    let r_sc = p.scorecards.find(sc => sc.round === r.id)
    return r_sc ?  r_sc.arrows.map(a => a.x ? 1 : 0) : [null]
  }

  export default {
    components: {
      eventParticipantScorecards,
    },
    data: () => ({
      r_search: '',
      sc_dialog: false,
      // records_dialog: false,
      loading: false,
      participant: null,
      // new_records: [],
      scroll_loop: false,
      // scope_nat: {
      //   FAAE: 'EE',
      //   // TODO when more clubs with different associations appear add here
      //   // or add it to the database with relevant getter
      // },
    }),
    watch: {
      scroll_loop: {
        handler() {
          if (this.scroll_loop) {
            this.infinite_loop()
          }
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user,
        courses: state => state.courses.courses,
        records: state => state.statistics.records,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      r_table() {
        let r_table = {header: [{ text: 'Name', value: 'name' },
                                { text: 'Class', value: 'class' },
                                { text: 'Round', value: 'round'}],
                       data: []}
        if (this.event) {
          r_table.header = [
            { text: 'Place', value: 'place', width: '1%' },
            { text: 'Name', value: 'name' },
            { text: 'Club', value: 'club' },
            { text: 'Class', value: 'class' },
          ]
          r_table.header.push(...this.event.rounds.filter(r => r.course_details.type !== 's').map(function(r) {
            return { text: r.ord.toString() + '. ' + r.label,
                    value: r.ord.toString(),
                    class: 'round-header'}
          }))
          if (this.rounds_have_x()) {
            r_table.header.push({ text: 'x', value: 'x', width: '1%' })
          }
          r_table.header.push({ text: 'Sum', value: 'sum', width: '1%' })
          r_table.header.push(...this.event.rounds.filter(r => r.course_details.type === 's').map(function(r) {
            return { text: r.label,
                    value: r.ord.toString(),
                    class: 'round-header'}
          }))
          if (Array.isArray(this.event.participants)) {
            r_table.data = this.event.participants.map(p => {
              let row = {
                id: p.id,
                name: p.archer.full_name,
                class: rankingService.getClass(p, this.event.ignore_gender),
                club: p.archer.club_details.name_short,
                rounds: [],
              }
              let sums = this.event.rounds.map(function(r) {
                if (r.course_details.type === 's') {
                  let so_arrows = getScore(r, p)
                  let so_sum = rankingService.sum( so_arrows )
                  if (so_sum !== null) {
                    row.shootoff = so_sum
                    let last_arrow = so_arrows[so_arrows.length - 1]
                    if (last_arrow !== null) {
                      // we have last arrow
                      row[r.ord] = so_sum - last_arrow + '<sup>' + -last_arrow + '</sup>'
                    } else {
                      row[r.ord] = so_sum
                    }
                  }
                  return 0
                }
                let sc_score = rankingService.sum( getScore(r, p) )
                if (r.course_details.format !== '') {
                  if (r.course_details.type === 'r') {
                    row.rounds.push({ format: r.course_details.format, score: sc_score })
                  }
                  if (r.course_details.type === 'u') {
                    let ui = this.findIndex(obj => obj.unit === r.course)
                    if (ui === -1) {
                      this.push({unit: r.course, sc_score: sc_score})
                    } else {
                      row.rounds.push({ format: r.course_details.format, score: sc_score + this[ui].sc_score })
                      this.splice(ui, 1)
                    }
                  }
                }
                // add scorecard score to results table
                row[r.ord] = sc_score
                // return score as part of scores array to calculate sum
                return sc_score
              }, []) // anonymus array for unit to round score transform
              row.sum = sums.length ? rankingService.sum( sums ) : 0
              let spots = this.event.rounds.map(function(r) {
                if (r.course_details.type === 's') {
                  return 0
                }
                return rankingService.sum( getSpots(r, p) )
              })
              row.x = spots.length ? rankingService.sum( spots ) : 0
              this.event.rounds.map(function (r) {
                if (r.is_open) {
                  let arrows = getScore(r, p)
                  row['pr' + r.ord] = Math.round((arrows.filter(a => a !== null).length / arrows.length) * 100)
                }
              })
              // // NOTE here **no club** ID has been hardcoded
              // if (this.event.records && p.archer.club_details.id !== 1) {
              //   let records = []
              //   let row_class = p.age_group + p.archer.gender + p.style
              //   for (let r of row.rounds) {
              //     let current_record = this.records.filter(record => {
              //       let rec_class = record.age_group + record.gender + record.style
              //       // build scope here
              //       let scope = this.event.records
              //       if (scope === 'nat') {
              //         scope = this.scope_nat[p.archer.club_details.association]
              //       } else {
              //         // NOTE scope order is important here - 'nat/EU/W'
              //         // the combinations are still tricky and might not work
              //         scope = this.scope_nat[p.archer.club_details.association] + '/' + scope
              //       }
              //       if ( rec_class === row_class &&
              //           record.format === r.format &&
              //           record.scope.includes(scope)) {
              //         //  && record.scope.includes(this.event.records) - this is not entirely accurate
              //         // as it needs to be cleared -- event record score should be one of 'nat', 'EU', 'W'
              //         // this is hierary, not sure about if 'W' can be shot at 'EU' turnament, 'nat' can be
              //         // shot on either
              //         return true
              //       }
              //       return false
              //     })
              //     if (r.score && r.score > Math.max(...current_record.map(record => record.score))) {
              //       records.push({
              //         scope: this.event.records,
              //         event: this.event.name,
              //         date: this.event.date_start,
              //         format: r.format,
              //         archer: row.name,
              //         class: row_class,
              //         score: r.score
              //       })
              //     }
              //   }
              //   if (records.length) {
              //     row.records = records
              //   }
              // }
              return row
            })
            rankingService.participantRank(r_table.data)
          }
        }
        return r_table
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
        this.participant = this.event.participants.find(p => p.id === pId)
        this.participant['class'] = rankingService.getClass(this.participant, this.event.ignore_gender)
        this.sc_dialog = true
      },
      // participant_records(records) {
      //   this.new_records = records
      //   this.records_dialog = true
      // },
      sc_edit() {
        return [this.event.creator, ...this.event.admins].includes(this.user.email) && !this.event.archive
      },
      rounds_have_x() {
        for (let r of this.event.rounds) {
          for (let c of this.courses) {
            if (r.course === c.id) {
              for (let e of c.ends) {
                if (e.x) {
                  return true
                }
              }
            }
          }
        }
        return false
      },
      infinite_loop() {
        let scroll_target = document.body.scrollHeight - window.innerHeight
        this.$vuetify.goTo(0, {duration: 100}).then(() => {
          this.$store.dispatch('events/updateEvent', this.event.id).then(() => {
            this.$vuetify.goTo(scroll_target, {
              duration: scroll_target * 20,
              easing: 'linear'
            }).then(() => {
              if (this.scroll_loop) {
                setTimeout(this.infinite_loop, 3000)
              }
            })
          })
        })
      },
      results2pdfProxy() {
        pdfService.results2pdf(this.event, this.r_table, this.$route.path)
      }
    },
  }
</script>

<style scoped>
  td {
    white-space: nowrap;
  }
  .progress-text {
    font-size: 7px;
  }
</style>
