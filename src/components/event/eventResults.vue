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
                <v-btn icon @click="participant_sc(row.id)" small>
                  <v-icon size="16">mdi-book-open-outline</v-icon>
                </v-btn>
              </template>
              <span :class="col.value === 'sum' ? 'font-weight-medium' : ''" v-html="row[col.value]"/>
              <template v-if="'rec'+col.value in row">
                <newRecord :record="row['rec'+col.value]"/>
              </template>
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
  import newRecord from '@/components/statistics/newRecord.vue'
  import rankingService from '@/services/rankingService'
  import pdfService from '@/services/pdfService'


  function getScore(r, p) {
    let r_sc = p.scorecards.find(sc => sc.round === r.id)
    return r_sc ?  r_sc.arrows.map(a => a.score) : []
  }

  function getSpots(r, p) {
    let r_sc = p.scorecards.find(sc => sc.round === r.id)
    return r_sc ?  r_sc.arrows.map(a => a.x ? 1 : 0) : []
  }

  export default {
    components: {
      eventParticipantScorecards,
      newRecord,
    },
    data: () => ({
      r_search: '',
      sc_dialog: false,
      loading: false,
      participant: null,
      scroll_loop: false,
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
        let r_table = {header: [
            { text: 'Place', value: 'place', width: '1%' },
            { text: 'Name', value: 'name' },
            { text: 'Club', value: 'club' },
            { text: 'Class', value: 'class' },
            { text: 'Round', value: 1 },
            { text: 'Sum', value: 'sum' }
          ],
          data: []
        }
        if (this.event) {
          // reorganise event rounds
          let rounds = [], so = null
          for (let r of this.event.rounds) {
            if (r.course_details.type == 's') {
              so = r
            }
            if (r.course_details.type == 'r') {
              rounds.push(r)
            }
            if (r.course_details.type == 'u') {
              let ui = rounds.findIndex(obj => obj.course == r.course)
              if (ui === -1) {
                rounds.push(r)
              } else {
                rounds.splice(ui, 1, [rounds[ui], r])
              }
            }
          }
          // NOTE: this can be used to add other information to the pdfService
          // that needs to be calculated
          r_table.meta = {
            rounds: rounds.length,
            so: so ? true : false,
            url: this.$route.path,
          }
          r_table.header = [
            { text: 'Place', value: 'place', width: '1%' }
          ]
          if (this.event.use_level_class) {
            r_table.header.push({ text: 'Classif.', value: 'classification', width: '1%' })
          }
          r_table.header.push(
            { text: 'Name', value: 'name' },
            { text: 'Club', value: 'club' },
            { text: 'Class', value: 'class' })
          r_table.header.push(...rounds.map(function(r) {
            if (Array.isArray(r)) {
              // we have units that are combined into a round
              let label = rankingService.longestPrefix(r.map(obj => obj.label))
              return { text: '(' + r.map(obj => obj.ord).join('+') + ') ' + label,
                      value: r.map(obj => obj.ord).join('_'),
                      class: 'round-header'}
            } else {
              // we have round object
              return { text: r.ord.toString() + '. ' + r.label,
                      value: r.ord.toString(),
                      class: 'round-header'}
            }
          }))
          if (this.rounds_have_x()) {
            r_table.header.push({ text: 'x', value: 'x', width: '1%' })
            // NOTE: this should be changed if we're going to include X, X+10, 10, 10+9 exeptions
            r_table.meta.spots = 1
          }
          r_table.header.push({ text: 'Sum', value: 'sum', width: '1%' })
          if (so) {
            r_table.header.push({
              text: so.label,
              value: so.ord.toString(),
              class: 'round-header'})
          }
          if (Array.isArray(this.event.participants)) {
            r_table.data = this.event.participants.map(p => {
              let p_style_records = null
              if (this.event.records && p.archer.club_details.association != '') {
                p_style_records = this.records.filter(rec => {
                  if (rec.age_group === p.age_group &&
                      rec.gender === p.archer.gender &&
                      rec.style === p.style &&
                      rec.scope === p.archer.club_details.association) {
                    return true
                  }
                  return false
                })
              }
              let row = {
                id: p.id,
                classification: p.level_class,
                name: p.archer.full_name,
                class: rankingService.getClass(p, this.event.ignore_gender),
                club: p.archer.club_details.name_short,
              }
              let sums = rounds.map(function(r) {
                let r_ord = null, arrows = null, open = false
                let format = null
                if (Array.isArray(r)) {
                  // we have units that are combined into a round
                  r_ord = r.map(obj => obj.ord).join('_')
                  arrows = r.map(v => getScore(v, p)).flat()
                  open = r.some(v => v.is_open === true)
                  format = r[0].course_details.format
                } else {
                  // we have round object
                  r_ord = r.ord
                  arrows = getScore(r, p)
                  open = r.is_open
                  format = r.course_details.format
                }
                row[r_ord] = rankingService.sum( arrows )
                if (open === true && arrows.length) {
                  row['pr' + r_ord] = Math.round((arrows.filter(a => a !== null).length / arrows.length) * 100)
                }
                if (p_style_records !== null) {
                  let seen_scope = null // NOTE this might still fail in some conditions
                  p_style_records.filter(v => v.format === format).map(function(rec) {
                    if (rec.score < row[r_ord] && seen_scope !== rec.scope) {
                      row['rec' + r_ord] = {
                        format: format,
                        archer: row.name,
                        class: row.class,
                        score: row[r_ord],
                        scope: p.archer.club_details.association,
                        current: rec
                      }
                    }
                    seen_scope = rec.scope
                  })
                }
                return row[r_ord]
              })
              row.sum = sums.length ? rankingService.sum( sums ) : 0

              let spots = this.event.rounds.map(function(r) {
                if (r.course_details.type === 's') {
                  return 0
                }
                return rankingService.sum( getSpots(r, p) )
              })
              row.x = spots.length ? rankingService.sum( spots ) : 0
              row.progress = sums.some(v => v !== null)

              if (so) {
                let so_arrows = getScore(so, p)
                let so_sum = rankingService.sum( so_arrows )
                if (so_sum !== null) {
                  row.shootoff = so_sum
                  let last_arrow = so_arrows[so_arrows.length - 1]
                  if (last_arrow !== null) {
                    // we have last arrow
                    row[so.ord] = so_sum - last_arrow + '<sup>' + -last_arrow + '</sup>'
                  } else {
                    row[so.ord] = so_sum
                  }
                }
              }
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
        pdfService.results2pdf(this.event, this.r_table)
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
