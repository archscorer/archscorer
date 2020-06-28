<template>
  <v-sheet>
    <v-card>
      <v-card-title>
        <small>Archers Summary</small>
        <v-spacer />
        <v-text-field
          v-model="s_search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :mobile-breakpoint="300"
        dense
        :headers="s_table_header"
        :items="s_table"
        :search="s_search"
        :loading="loading"
        group-by="class"
        multi-sort
        :items-per-page="50"
      >
      </v-data-table>
    </v-card>
    <v-card v-if="s.club_ranking">
      <v-card-title>
        <small>Clubs Summary</small>
        <v-spacer />
      </v-card-title>
      <v-data-table
        :mobile-breakpoint="300"
        dense
        :headers="c_table_header"
        :items="c_table"
        :loading="loading"
        multi-sort
        :items-per-page="15"
      >
      </v-data-table>
    </v-card>
  </v-sheet>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import rankingService from '@/services/rankingService'
  import { mapState } from 'vuex'

  export default {
    // name: 'Series',
    components: {
    },
    data: () => ({
      s_search: '',
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
      s() {
        return this.$store.getters['series/seriesById'](parseInt(this.$route.params.id))
      },
      loading() {
        if (this.s_table.length) {
          return false
        }
        if (this.s) {
          for (let stage of this.s.stages) {
            if (Array.isArray(stage.participants)) {
              return false
            }
          }
        }
        return true
      },
      s_table_header() {
        if (this.s) {
          let header = [
            { text: 'Class', value: 'class' },
            { text: 'Place', value: 'place', width: '1%' },
            { text: 'Name', value: 'name', width: '140px' },
            { text: 'Club', value: 'club' },
            { text: 'Points', value: 'points'},
            { text: 'Sum', value: 'sum' },
          ]
          header.push(...this.s.stages.map(function(stage) {
            return { text: stage.name,
                    value: 'stage' + stage.id.toString(),
                    class: 'stage-header' }
          }).reverse())
          return header
        }
        return []
      },
      c_table_header() {
        if (this.s_table && this.s.club_ranking) {
          let header = [
            { text: 'Place', value: 'place', width: '1%' },
            { text: 'Club', value: 'club'},
            { text: 'Points', value: 'points'}
          ]
          header.push(...this.s.stages.map(function(stage) {
            return { text: stage.name,
                    value: 'stage' + stage.id.toString(),
                    class: 'stage-header' }
          }).reverse())
          return header
        }
        return []
      },
      s_table() {
        if (this.s) {
          let s_table = []
          for (let stage of this.s.stages) {
            if (!Array.isArray(stage.participants)) {
              continue
            }
            let p_table = stage.participants.map(p => {
              // handle shootoff
              let so = stage.rounds.find(obj => obj.course_name.search('shootoff') !== -1)
              // NOTE: however it works, if there are multiple shootoff rounds (there should not), then find
              // returns first shootoff round and rest of them are treated as normal.
              // get shootoff round id (if it exists) to test against in scorecard filtering
              so = so ? so.id : null
              return {
                name: p.archer.full_name,
                class: p.age_group + p.archer.gender + p.style,
                id: p.archer.id + p.age_group + p.style,
                club: p.archer.club,
                sum: rankingService.sum([].concat(...p.scorecards.filter(obj => obj.round !== so).map(sc => [...sc.arrows.map(a => a.score)]))),
                x: rankingService.sum([].concat(...p.scorecards.filter(obj => obj.round !== so).map(sc => [...sc.arrows.map(a => a.x)]))),
                shootoff: so ? rankingService.sum(...p.scorecards.filter(obj => obj.round === so).map(sc => [...sc.arrows.map(a => a.score)])) : null,
              }
            })

            rankingService.participantRank(p_table)
            // Map solution to count classes in participant array
            let class_counts = p_table.reduce((acc, e) => acc.set(e.class, (acc.get(e.class) || 0) + 1), new Map())
            // populate series table
            let points = {class: null, points: null}
            for (let p of p_table.filter(obj => obj.sum > 0)) {
              if (p.class !== points.class) {
                points.class = p.class
                points.points = Math.min(this.s.points_max, class_counts.get(p.class))
              }
              p.points = points.points >= p.place && p.sum > 0 ? points.points - p.place + 1 : 0
              let index = s_table.findIndex(obj => obj.id === p.id)
              if (index === -1) {
                s_table.push({
                  id: p.id,
                  class: p.class,
                  name: p.name,
                  club: p.club,
                  sum: [p.sum],
                  points: [p.points]
                })
                // [p.sum, p.points]
                s_table[s_table.length - 1]['stage' + stage.id.toString()] = (p.points > 0 ? p.points : '-') + ' (' + p.sum + ')'
              } else {
                s_table[index].sum.push(p.sum)
                s_table[index].points.push(p.points)
                s_table[index]['stage' + stage.id.toString()] = (p.points > 0 ? p.points : '-') + ' (' + p.sum + ')'
              }
            }
          }
          for (let p of s_table) {
            // This sorts and scores participant points based on best stages and series
            // participant_max and participant_min limits
            p.sum.sort(function (a, b) { return p.points[p.sum.indexOf(b)] - p.points[p.sum.indexOf(a)] })
            p.points.sort(function (a, b) { return b - a })
            if (p.points.length >= this.s.participant_min) {
              // this is initialised here as later is trickier to figure out the number of stages
              // participated
              p.place = null
            }
            if (p.points.length >= this.s.participant_max) {
              p.points = rankingService.sum(p.points.slice(0, this.s.participant_max))
              p.sum = rankingService.sum(p.sum.slice(0, this.s.participant_max))
            } else {
              p.points = rankingService.sum(p.points)
              p.sum = rankingService.sum(p.sum)
            }
          }

          return s_table.sort(function(a, b) {
            if (a.class < b.class) {
              return -1
            }
            if (a.class > b.class) {
              return 1
            }
            if (a.points < b.points) {
              return 1
            }
            if (a.points > b.points) {
              return -1
            }
            if (a.sum < b.sum) {
              return 1
            }
            if (a.sum > b.sum) {
              return -1
            }
            return 0
          }).map(p => {
            // assigning series place for participant if points and enough stages
            // p.place === null <-- see code above
            if (p.class !== this.class) {
              this.class = p.class
              this.ord = 1
              this.place = 1
              this.points = p.points
              this.sum = p.sum
            }
            if (p.place === null && p.points > 0) {
              if (p.points < this.points || p.sum < this.sum) {
                this.place = this.ord
              }
              p.place = this.place
              this.ord += 1
              this.sum = p.sum
              this.points = p.points
            }
            if (p.points === 0) {
              p.points = '-'
            }
            return p
          }, {class: null, place: 1, ord: 1, sum: null, points: null}).sort(function (a, b) {
            if (a.class < b.class) {
              return -1
            }
            if (a.class > b.class) {
              return 1
            }
            // not all have place, so in this case use large positive number
            if ((a.place || 9999) > (b.place || 9999)) {
              return 1
            }
            if ((a.place || 9999) < (b.place || 9999)) {
              return -1
            }
            return 0
          })
        }
        return []
      },
      c_table() {
        if (this.s_table.length && this.s.club_ranking) {
          let c_table = []
          for (let stage of this.s.stages) {
            let stageID = 'stage' + stage.id.toString()
            // this.s.club_ranking_max shows how many participants per class per club score points
            let club_max = {class: null, counter: {}}
            for (let p of this.s_table) {
              if (p[stageID]) {
                if (p.class != club_max.class) {
                  club_max.class = p.class
                  club_max.counter = {}
                }
                if (!(p.club in club_max.counter)) {
                  club_max.counter[p.club] = 0
                }
                if (club_max.counter[p.club] < this.s.club_ranking_max) {
                  let points = parseInt(p[stageID].split(' ')[0]) || 0
                  let ci = c_table.findIndex(obj => obj.club === p.club)
                  if (ci === -1) {
                    c_table.push({club: p.club, place: null, points: points})
                    c_table[c_table.length - 1][stageID] = points
                  } else {
                    if (stageID in c_table[ci]) {
                      c_table[ci][stageID] += points
                    } else {
                      c_table[ci][stageID] = points
                    }
                    c_table[ci].points += points
                  }
                }
                club_max.counter[p.club] += 1
              }
            }
          }
          return c_table.sort(function (a, b) {
            if (a.points > b.points) {
              return -1
            }
            if (a.points < b.points) {
              return 1
            }
            return 0
          }).map(club => {
            if (club.points < this.points) {
              this.place = this.ord
            }
            club.place = this.place
            this.points = club.points
            this.ord += 1
            return club
          }, {place: 1, ord: 1, points: null})
        }
        return []
      }
    },
    methods: {
      //
    },
  }
</script>
