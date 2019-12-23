<template>
  <v-container>
    <v-row v-for="round in get_rounds()" :key="round.id">
      <h3>{{ round.ord }}. {{ round.label }}</h3>
      <v-col v-for="(half, hi) in round.halves" :key="hi">
        <table>
          <thead>
            <tr>
              <th>End</th>
              <th :colspan="round.nr_of_arrows">Arrows</th>
              <th>Sum</th>
              <th>Cum</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="end in half" :key="end.id">
              <td class="end-ord">
                {{ end.ord }}
              </td>
              <td class="end-arrow" v-for="a in round.nr_of_arrows" :key="a">
                <template v-if="end.arrows !== null">
                  <!-- for very wierd reasona 'a' is starts from 1, not 0 like within <script> -->
                  {{ end.arrows[a-1].x ? 'X' : end.arrows[a-1].score === 0 ? 'M' : end.arrows[a-1].score }}
                </template>
              </td>
              <td class="end-sums text-right">
                {{ end.sum }}
              </td>
              <td class="end-sums text-right">
                {{ end.cum }}
              </td>
            </tr>
          </tbody>
        </table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */

  import { mapState} from 'vuex'

  // TODO should create util.js file to collect most used utility functions
  // sum, for example, could be there
  function sum(arr) {
    return arr.reduce((sum, x) => sum + x);
  }

  export default {

    props: {
      participant: Object,
      rounds: Array,
    },
    data: () => ({
      //
    }),
    computed: {
      ...mapState({
        courses: state => state.courses.courses,
      }),
    },
    methods: {
      get_rounds() {
        // round object for scorecard, return list of modified round objects
        let rounds = [...this.rounds]
        return rounds.map(r => {
          let course = this.courses.find(obj => obj.id === r.course)

          let ends = []
          // in some cases course is not loaded, probably related to dev hotreload
          // but nevertheless, if couse is not loaded -- request it from backend
          if (course) {
            ends = course.ends
          } else {
            this.$store.dispatch('courses/getCourses', r.course)
          }
          // max number of arrows for round ends
          let aNr = 0
          let cum = 0
          let halves = []
          let sc_ends = []
          for (let e of ends) {
            // end arrows
            let eAr = this.get_end_arrows(r.id, e.id)
            let eSum = 0
            if (eAr !== null) {
              eSum = sum( eAr.map(a => a.score ))
            }

            // update max number
            aNr = e.nr_of_arrows > aNr ? e.nr_of_arrows : aNr
            cum += eSum
            sc_ends.push(Object.assign({}, e, {arrows: eAr, sum: eSum, cum: cum}))
            if (course.halves === true && e.ord === course.ends.length / 2) {
              halves.push([...sc_ends])
              sc_ends = []
            }
          }
          halves.push(sc_ends)
          return Object.assign({}, r, {nr_of_arrows: aNr, halves: halves})
        })
      },
      get_end_arrows(rId, eId) {
        let r_sc = this.participant.scorecards.find(obj => obj.round === rId)
        if (r_sc) {
          return r_sc.arrows.filter(obj => obj.end === eId)
        }
        return null
      }
    },
  }
</script>

<style scoped>
  .end-ord {
    padding: 2px 4px;
  }
  .end-sums {
    padding: 2px 4px;
  }
  .end-arrow {
    padding: 2px 4px;
    border: solid 1px lightgray;
    font-weight: 300;
    text-align: center;
    min-width: 24px;
  }
</style>
