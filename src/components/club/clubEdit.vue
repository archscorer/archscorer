<template>
  <v-dialog v-model="dialog" fullscreen hide-overlay>
    <template v-slot:activator="{ on }">
      <v-btn color="warning" class="mx-2" v-on="on" @click="c_edit()">Edit club</v-btn>
    </template>
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Edit {{ club.name }}</v-toolbar-title>
        <v-spacer />
        <v-toolbar-items>
          <v-btn dark text @click="putClub(club); dialog = false">Save</v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-card class="ma-5">
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <v-textarea
                outlined
                v-model="club.contact"
                label="Contact information"
                auto-grow
              ></v-textarea>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-textarea
                outlined
                v-model="club.description"
                label="Club description"
                auto-grow
              ></v-textarea>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-card>
  </v-dialog>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    data: () => ({
      dialog: false,
      club: {}
    }),
    computed: {
      p_club() {
        return this.$store.getters['clubs/clubById'](parseInt(this.$route.params.id))
      },
    },
    methods: {
      ...mapActions('clubs', [
        'putClub',
      ]),
      c_edit() {
        this.club = Object.assign({}, this.p_club)
      }
    }
  }
</script>
