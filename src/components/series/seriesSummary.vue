<template>
  <v-card>
    <v-card-title>
      <small>Summary Table</small>
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
      group-by="class"
      multi-sort
      :items-per-page="50"
    >
    </v-data-table>
  </v-card>
</template>

<script>
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
      s_table_header() {
        if (this.s) {
          let header = [
            { text: 'Class', value: 'class' },
            { text: 'Place', value: 'place', width: '1%' },
            { text: 'Name', value: 'name' },
            { text: 'Club', value: 'club' },
            { text: 'Points', value: 'points'},
            { text: 'Sum', value: 'sum' },
          ]
          header.push(...this.s.stages.map(function(stage) {
            return { text: stage.name,
                    value: 'stage' + stage.id.toString() }
          }).reverse())
          return header
        }
        return []
      },
      s_table() {
        if (this.s) {
          let s_table = []
          for (let stage of this.s.stages) {
            // here before map should be filter to exclude participants who should not be in
            // cup ranking (i.e for club cup, they dont have club that belongs to faae)
            let p_table = stage.participants.map(p => {
              // handle shootoff
              let so = stage.rounds.find(obj => obj.course_name.search('shootoff') !== -1)
              // get shootoff round id (if it exists) to test against in scorecard filtering
              so = so ? so.id : null
              return {
                name: p.archer.full_name,
                class: p.age_group + p.archer.gender + p.style,
                id: p.archer.id + p.age_group + p.style,
                club: p.archer.club,
                sum: rankingService.sum(...p.scorecards.filter(obj => obj.round !== so).map(sc => [...sc.arrows.map(a => a.score)])),
                x: rankingService.sum(...p.scorecards.filter(obj => obj.round !== so).map(sc => [...sc.arrows.map(a => a.x)])),
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
              p.points = points.points >= p.place && p.sum > 0 ? points.points - p.place + 1 : null
              if (p.points) {
                let index = s_table.findIndex(obj => obj.id === p.id)
                if (index === -1) {
                  s_table.push({
                    id: p.id,
                    class: p.class,
                    name: p.name,
                    club: p.club,
                    sum: p.sum,
                    points: p.points
                  })
                  // [p.sum, p.points]
                  s_table[s_table.length - 1]['stage' + stage.id.toString()] = p.points.toString() + ' (' + p.sum.toString() + ')'
                } else {
                  s_table[index].sum += p.sum
                  s_table[index].points += p.points
                  s_table[index]['stage' + stage.id.toString()] = p.points.toString() + ' (' + p.sum.toString() + ')'
                }
              }
            }
          }
          return s_table.sort(function(a, b) {
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
          })
        }
        return []
      }
    },
    methods: {
      //
    },
  }
</script>

<style>
</style>
