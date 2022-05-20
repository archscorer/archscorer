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
                <eventParticipantScorecards :pId="row.id"
                                            :eId="event.id"
                                            :rounds="event.rounds"
                                            :edit="sc_edit()"/>
              </template>
              <span :class="col.value === 'sum' ? 'font-weight-medium' : ''" v-html="row[col.value]"/>
              <template v-if="'rec'+col.value in row">
                <newRecord :record="row['rec'+col.value]"/>
              </template>
              <template v-if="'pr'+col.value in row && event.archive === false">
                <v-icon v-if="row['pr'+col.value] === 'checked'" color="green" size="12">mdi-check</v-icon>
                <v-progress-circular
                  v-else
                  v-model="row['pr'+col.value]"
                  :color="row['pr'+col.value] === 100 ? 'orange' : 'error'"
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
            Export results to <v-btn x-small color="primary" @click="results2pdfProxy()" class="mr-3">PDF</v-btn>
            <v-btn x-small color="primary"
              v-for="(r, ri) in r_table.meta.rounds"
              @click="roundResults2pdfProxy(r)"
              :key="'rb_' + ri">R{{ ri+1 }}</v-btn>
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
  import { mapState, mapActions } from 'vuex'

  import eventParticipantScorecards from '@/components/event/eventParticipantScorecards.vue'
  import newRecord from '@/components/statistics/newRecord.vue'
  import rankingService from '@/services/rankingService'
  import pdfService from '@/services/pdfService'


  function getScore(r, p) {
    let r_sc = p.scorecards.find(sc => sc.round === r.id)
    return r_sc ?  [r_sc.score] : []
  }

  function getProgress(r, p) {
    let r_sc = p.scorecards.find(sc => sc.round === r.id)
    return r_sc ?  r_sc.pr : null
  }

  function getSpots(r, p) {
    let r_sc = p.scorecards.find(sc => sc.round === r.id)
    return r_sc ?  r_sc.spots : null
  }

  function getChecked(r, p) {
    let r_sc = p.scorecards.find(sc => sc.round === r.id)
    return r_sc ?  r_sc.checked : null
  }


  export default {
    components: {
      eventParticipantScorecards,
      newRecord,
    },
    data: () => ({
      r_search: '',
      loading: false,
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
        arrows: state => state.events.arrows,
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
            rounds: rounds,
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
            { text: this.event.show_association ? 'Association' : 'Club', value: 'club' },
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
              if (this.event.records && p.archer_rep.split('|')[1] !== '') {
                p_style_records = this.records.filter(rec => {
                  if (rec.age_group === p.age_group &&
                      rec.gender === p.gender &&
                      rec.style === p.style &&
                      rec.scope === p.archer_rep.split('|')[1]) {
                    return true
                  }
                  return false
                })
              }
              let row = {
                id: p.id,
                classification: p.level_class,
                name: p.full_name,
                class: rankingService.getClass(p, this.event.ignore_gender),
                club: p.archer_rep.split('|')[this.event.show_association ? 1 : 0],
              }
              let sums = rounds.map(function(r) {
                let r_ord = null, score = null, open = false, checked = false, progress = null
                let format = null
                if (Array.isArray(r)) {
                  // we have units that are combined into a round
                  r_ord = r.map(obj => obj.ord).join('_')
                  score = r.map(u => getScore(u, p)).flat()
                  progress = rankingService.sum( r.map(u => getProgress(u, p)).flat() ) / 2
                  checked = r.every(u => getChecked(u, p) === true)
                  open = r.some(u => u.is_open === true)
                  format = r[0].course_details.format
                } else {
                  // we have round object
                  r_ord = r.ord
                  score = getScore(r, p)
                  progress = getProgress(r, p)
                  checked = getChecked(r, p)
                  open = r.is_open
                  format = r.course_details.format
                }
                row[r_ord] = rankingService.sum( score )
                if (open === true && score) {
                  if (checked) {
                    row['pr' + r_ord] = 'checked'
                  } else {
                    row['pr' + r_ord] = Math.round(progress ? progress * 100 : 0)// Math.round((arrows.filter(a => a !== null).length / arrows.length) * 100)
                  }
                }
                if (p_style_records !== null) {
                  let seen_scope = null // NOTE this might still fail in some conditions
                  p_style_records.filter(v => v.format === format).map(function(rec) {
                    if (rec.score < row[r_ord] && seen_scope !== rec.scope) {
                      row['rec' + r_ord] = {
                        event: this.event.name,
                        date: this.event.date_end,
                        format: format,
                        archer: p.full_name,
                        age_group: p.age_group,
                        gender: p.gender,
                        style: p.style,
                        score: row[r_ord],
                        scope: p.archer_rep.split('|')[1],
                        current: rec
                      }
                    }
                    seen_scope = rec.scope
                  }, this)
                }
                return row[r_ord]
              }, this)
              row.sum = sums.length ? rankingService.sum( sums ) : 0

              let spots = this.event.rounds.map(function(r) {
                if (r.course_details.type === 's') {
                  return 0
                }
                return getSpots(r, p)
              })
              row.x = spots.length ? rankingService.sum( spots ) : 0
              // NOTE progress is used by rankingService to determine if place column should be shown
              row.progress = sums.some(v => v !== null)

              if (so) {
                let so_sum = rankingService.sum( getScore(so, p) )
                if (so_sum !== null) {
                  row.shootoff = so_sum
                  row.progress = true
                  let last_arrow = p.scorecards.find(sc => sc.round === so.id).last_arrow
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
      ...mapActions('events', [
        'getArrows',
      ]),
      update_r_table() {
        this.loading = true
        this.$store.dispatch('events/updateEvent', this.event.id).then(() => {
          this.loading = false
        })
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
      roundResults_table(r) {
        let round_table = {
          header: [{ text: 'Place', value: 'place', pdf_width: 'auto' }],
          data: [],
          meta: {
            url: this.$route.path,
            ends: 0,
          }
        }
        if (this.event.use_level_class) {
          round_table.header.push({ text: 'Classif.', value: 'classification', pdf_width: 'auto' })
        }
        round_table.header.push(
          { text: 'Name', value: 'name', pdf_width: 98 },
          { text: 'Club', value: 'club', pdf_width: 28 },
          { text: 'Class', value: 'class' },
          { text: 'Total', value: 'sum', pdf_width: 22},
        )
        // exract ends from round.course object
        // we can have different representations here:
        // single unit or round will be an event.round object
        // 2 units of the same type will be an array of two event.round objects
        // rounds can have halves or not. these we need to split up here?
        let spots = false
        if (Array.isArray(r)) {
          // we have units that are combined into a round
          round_table.meta.round_label = '(' + r.map(obj => obj.ord).join('+') + ') ' + rankingService.longestPrefix(r.map(obj => obj.label))
          for (let h of r) {
            let c = this.courses.find(obj => obj.id === h.course)
            for (let e of c.ends) {
              round_table.header.push({ text: e.ord, value: h.ord + '_' + e.ord, pdf_width: '*'})
              round_table.meta.ends += 1
              if (e.x) {
                spots = true
              }
            }
            round_table.header.push({ text: 'Sum', value: h.ord + '_sum', pdf_width: 20})
          }
        } else {
          // we have round object, it can have halves or if not a single unit or smth special
          round_table.meta.round_label = r.ord + '. ' + r.label
          let c = this.courses.find(obj => obj.id === r.course)
          for (let e of c.ends) {
            round_table.header.push({ text: e.ord, value: r.ord + '_' + e.ord, pdf_width: '*'})
            round_table.meta.ends += 1
            if (c.halves && e.ord === c.ends.length / 2) {
              round_table.header.push({ text: 'Sum', value: r.ord + '_1_sum', pdf_width: 20})
            }
            if (e.x) {
              spots = true
            }
          }
          round_table.header.push({ text: 'Sum', value: r.ord + '_2_sum', pdf_width: 20})
        }
        if (spots) {
          round_table.header.push({ text: 'x', value: 'spots', pdf_width: 14})
        }
        if (Array.isArray(this.event.participants)) {
          round_table.data = this.event.participants.map(p => {
            let row = {
              classification: p.level_class,
              name: p.full_name,
              club: p.archer_rep.split('|')[0],
              class: rankingService.getClass(p, this.event.ignore_gender),
              progress: false,
              sum: 0,
            }
            let spots = 0
            if (Array.isArray(r)) {
              // we have units that are combined into a round
              for (let h of r) {
                let c = this.courses.find(obj => obj.id === h.course)
                let sc = p.scorecards.find(obj => obj.round === h.id)
                let sum = 0
                if (sc) {
                  row.progress = true
                  let sc_arrows = this.arrows.filter(a => a.sc === sc.id)
                  for (let e of c.ends) {
                    spots += rankingService.sum(sc_arrows.filter(a => a.e === e.id).map(a => a.x ? 1 : 0))
                    row[h.ord + '_' + e.ord] = rankingService.sum(sc_arrows.filter(a => a.e === e.id).map(a => a.p))
                    sum += row[h.ord + '_' + e.ord]
                    row.sum += row[h.ord + '_' + e.ord]
                  }
                  row[h.ord + '_sum'] = sum
                }
              }
            } else {
              // we have round object, it can have halves or if not a single unit or smth special
              let c = this.courses.find(obj => obj.id === r.course)
              let sc = p.scorecards.find(obj => obj.round === r.id)
              let sum = 0
              if (sc) {
                row.progress = true
                let sc_arrows = this.arrows.filter(a => a.sc === sc.id)
                for (let e of c.ends) {
                  spots += rankingService.sum(sc_arrows.filter(a => a.e === e.id).map(a => a.x ? 1 : 0))
                  row[r.ord + '_' + e.ord] = rankingService.sum(sc_arrows.filter(a => a.e === e.id).map(a => a.p))
                  sum += row[r.ord + '_' + e.ord]
                  row.sum += row[r.ord + '_' + e.ord]
                  if (c.halves && e.ord === c.ends.length / 2) {
                    row[r.ord + '_1_sum'] = sum
                    sum = 0
                  }
                }
                row[r.ord + '_2_sum'] = sum
              }
            }
            row.spots = spots
            return row
          }, this)
          rankingService.participantRank(round_table.data)
        }
        pdfService.roundResults2pdf(this.event, round_table)
      },
      results2pdfProxy() {
        pdfService.results2pdf(this.event, this.r_table)
      },
      roundResults2pdfProxy(r) {
        let afilter = r.id
        if (Array.isArray(r)) {
          afilter = r.map(h => h.id)
        }
        this.getArrows({'rId': afilter}).then(() => {
          this.roundResults_table(r)
        })
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
