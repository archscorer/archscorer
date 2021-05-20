<template>
  <v-autocomplete
    v-model="archer"
    @input="$emit('input', archer)"
    :search-input.sync="query"
    :items="qresponse_items"
    label="Find archer ..."
    hint="Search is executed from 2 characters"
    placeholder="Start typing .."
    prepend-icon="mdi-database-search"
    return-object
    hide-no-data
    no-filter
    clearable
  >
  </v-autocomplete>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    props: {
      value: Object,
    },
    data: () => ({
      archer: {},
      query: '',
    }),
    watch: {
      query: function(val) {
        if (val && val.length >= 2) {
          this.searchArcher(val)
        } else {
          this.clearSearch([{ header: 'be more specific (at least 2 letters)' }])
        }
      },
    },
    computed: {
      ...mapState({
        qresponse: state => state.user.qresponse,
        clubs: state => state.clubs.clubs,
      }),
      qresponse_items() {
        return this.qresponse.map(a => {
          if (a.id) {
            // add text field only if we have valid archer object
            let text = a.full_name + ' (' + this.clubs.find(obj => obj.id === a.club).name_short + ')' +
                      (a.user ? ' - w account' : '') +
                      (a.events.length ? ' ' + a.events.length + ' events': '')
            return Object.assign({}, a, { text })
          } else {
            return a
          }
        })
      }
    },
    methods: {
      ...mapActions('user', [
        'searchArcher',
        'clearSearch',
      ]),
    },
    created() {
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>
