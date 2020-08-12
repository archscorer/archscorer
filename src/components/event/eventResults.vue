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
              <span :class="col.value === 'sum' ? 'font-weight-medium' : ''" v-html="row[col.value]"/>
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
    </v-card-text>
    <v-card-actions>
      <template v-if="[this.event.creator, ...this.event.admins].includes(this.user.email) || this.event.archive">
        <p class='text-caption'>Export <v-btn @click="export2pdf()" x-small>to PDF</v-btn></p>
      </template>
    </v-card-actions>
    <v-dialog v-model="sc_dialog" max-width="650px">
      <v-card v-if="participant !== null">
        <v-card-title>{{ participant.archer.full_name }} {{ participant.class}} {{ participant.archer.club }}</v-card-title>
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
  </v-card>
</template>

<script>
  import pdfMake from 'pdfmake/build/pdfmake'
  import pdfFonts from 'pdfmake/build/vfs_fonts'

  pdfMake.vfs = pdfFonts.pdfMake.vfs

  import { mapState } from 'vuex'

  import eventParticipantScorecards from '@/components/event/eventParticipantScorecards.vue'
  import rankingService from '@/services/rankingService'

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
        courses: state => state.courses.courses,
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
          header.push(...this.event.rounds.filter(obj => obj.course_type !== 's').map(function(r) {
            return { text: r.ord.toString() + '. ' + r.label,
                    value: r.ord.toString(),
                    class: 'round-header'}
          }))
          if (this.rounds_have_x()) {
            header.push({ text: 'x', value: 'x', width: '1%' })
          }
          header.push({ text: 'Sum', value: 'sum', width: '1%' })
          header.push(...this.event.rounds.filter(obj => obj.course_type === 's').map(function(r) {
            return { text: r.label,
                    value: r.ord.toString(),
                    class: 'round-header'}
          }))
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
              class: rankingService.getClass(p, this.ignore_gender),
              club: p.archer.club
            }
            let sums = this.rounds.map(function(r) {
              if (r.course_type === 's') {
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
              row[r.ord] = rankingService.sum( getScore(r, p) )
              return row[r.ord]
            })
            row['sum'] = sums.length ? rankingService.sum( sums ) : 0
            let x = this.rounds.map(function(r) {
              if (r.course_type === 's') {
                return 0
              }
              return rankingService.sum( getX(r, p) )
            })
            row['x'] = x.length ? rankingService.sum( x ) : 0
            this.rounds.map(function (r) {
              if (r.is_open) {
                let r_sc = getScore(r, p)
                row['pr' + r.ord] = (r_sc.filter(obj => obj !== null).length / r_sc.length) * 100
              }
            })
            return row
          }, this.event)
          rankingService.participantRank(r_table)
          return r_table
        } else {
          return []
        }
      }
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
      export2pdf() {
        let docDefinition = {
          pageOrientation: this.event.rounds.length > 2 ? 'landscape' : 'portrait',
          footer: {
            columns: [
              { text: window.location.origin + this.$route.path, style: 'footer' },
              { text: new Date().toLocaleString(), alignment: 'right', style: 'footer' }
            ]
          },
          content: [{text: this.event.name, style: 'header'},
            [...new Set(this.r_table.map(r => r.class))].map(cls => {
            return {
              layout: 'lightHorizontalLines',
              table: {
                headerRows: 2,
                widths: [30, 125, 25, ...Array(this.r_table_header.length - 4).fill('*')],
                body: [
                  [{text: cls, colSpan: this.r_table_header.length - 1, style: 'styleheader' },
                   ...Array(this.r_table_header.length - 2).fill('')],

                  this.r_table_header.filter(h => h.value !== 'class').map(h => {
                    return {text: h.text, style: 'tableheader'}
                  }),

                  ...this.r_table.filter(r => r.class === cls).map(r => {
                    return this.r_table_header.filter(h => h.value !== 'class').map(h => {
                      if (typeof(r[h.value]) === 'undefined') {
                        return ''
                      }
                      if (typeof(r[h.value]) === 'string' && r[h.value].match(/<sup>(\d)<\/sup>/)) {
                        let m = r[h.value].match(/(\d+)<sup>(\d)<\/sup>/)
                        return {columns: [
                          {text: m[1], width: 'auto'},
                          {text: m[2], fontSize: 8}
                        ]}
                      }
                      return h.value === 'sum' ? {text: r[h.value], bold: true} : r[h.value]
                    })
                  })
                ]
              }
            }
          })],
          styles: {
            header: {
              fontSize: 24,
              bold: true,
              alignment: 'center',
              margin: [0, 15, 0, 5]
            },
            styleheader: {
              fontSize: 18,
              bold: true,
              margin: [0, 15, 0, 5]
            },
            tableheader: {
              fontSize: 12,
              bold: true,
              margin: [0, 0, 0, 0]
            },
            footer: {
              fontSize: 10,
              margin: [5, 0, 5, 0]
            }
          },
        }
        pdfMake.createPdf(docDefinition).open()
      }
    }
  }
</script>

<style scoped>
  td {
    white-space: nowrap;
  }
</style>
