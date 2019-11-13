<template>
  <v-card>
    <v-card-title>
    Registered Archers [{{ event ? event.name : '' }}]
    <v-spacer></v-spacer>
    <v-text-field
      v-model="p_search"
      append-icon="mdi-magnify"
      label="Search"
      single-line
      hide-details
    ></v-text-field>
  </v-card-title>
    <v-data-table
      dense
      :headers="p_table_header"
      :items="p_table"
      :search="p_search"
      group-by="class"
      :items-per-page="50"
    ></v-data-table>
  </v-card>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState} from 'vuex'

  export default {

    data: () => ({
      p_search: '',
      p_table_header: [
        { text: 'Name', value: 'name' },
        { text: 'Class', value: 'class' },
        { text: 'Club', value: 'club' },
        { text: 'Eats', value: 'eats' }
      ],
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      p_table() {
        if (this.event) {
          return this.event.participants.map(function(p) {
            return {
              name: p.archer.full_name,
              class: p.age_group + p.archer.gender + p.style,
              club: p.archer.club,
              eats: (p.eats ? "Yes" : "No")
            }
          })
        } else {
          return []
        }
      },
    }
  }
</script>
