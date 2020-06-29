<template>
  <v-list>
    <v-subheader v-if="series.length === 0">No series found in the database</v-subheader>
    <v-list-item v-for="s in series"
      :key="'series' + s.id"
      :to="{ name: 'series', params: { 'id': s.id}}"
      >
      <v-list-item-content>
        <v-list-item-title>{{ s.name }} {{ s.creator == user.email ? '*' : '' }}</v-list-item-title>
        <v-list-item-subtitle>
          <template v-if="s.date_start != s.date_end">
            from {{ s.date_start }} to {{ s.date_end }}
          </template>
          <template v-else>
            on {{ s.date_start }}
          </template>
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-action>
        <v-chip small v-if="s.type !== 'open'" v-text="s.type" :color="chip_color(s.type)"></v-chip>
      </v-list-item-action>
    </v-list-item>
  </v-list>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    computed: {
      ...mapState({
        series: state => state.series.series,
        user: state => state.user.user,
      }),
    },
    methods: {
      chip_color(type) {
        return type === 'private' ? 'primary' : type === 'club' ? 'secondary' : ''
      }
    },
    created() {
      this.$store.dispatch('series/getSeries')
    }
  }
</script>
