<template>
  <v-container v-if="clubs">
    <v-card width="100%" v-for="ass in association" :key="ass.name_short"
      class="ma-5">
      <v-card-title>{{ ass.name }} ({{ ass.name_short }})</v-card-title>
      <v-card-text>
        <v-list dense>
          <v-list-item v-for="club in association_clubs(ass.name_short)"
            :key="ass.name_short + '_' + club.id" class="ma-5"
            :to="{ name: 'club', params: { 'id': club.id}}">
            <v-list-item-content>
              <v-list-item-title>{{ club.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ get_club_members_string(club) }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <small><p>Club managers, please contact 'info @ archscorer . faae . ee'  to request
        admin access to your club.</p></small>
      </v-card-text>
    </v-card>
  </v-container>
  <v-overlay v-else>
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-overlay>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    computed: {
      ...mapState({
        user: state => state.user.user,
        clubs: state => state.clubs.clubs,
      }),
      association() {
        let association = []
        for (let club of this.clubs) {
          for (let ass of club.association) {
            const index = association.findIndex(obj => obj.name_short === ass.name_short);
            if (index === -1) {
              association.push(ass)
            }
          }
        }
        return association.sort()
      },
    },
    methods: {
      get_club_members_string(club) {
        let nr = Array.isArray(club.members) ? club.members.length : club.members
        return 'There ' + (nr > 1 ? 'are' : 'is') + ' ' + nr + ' ' +
               (club.id === 1 ? 'user' : 'member') + (nr > 1 ? 's' : '')
      },
      association_clubs(ass_short) {
        return this.clubs.filter(obj => obj.association.some(obj => obj.name_short === ass_short))
      },
    },
    created() {
      this.$store.dispatch('clubs/getClubs')
    }
  }
</script>
