<template>

  <v-menu
    v-if="user.id !== null"
    v-model="user_menu"
    transition="slide-y-transition"
  >
    <template v-slot:activator="{ on }">
      <v-btn text
        v-on="on">
        <span>{{ user.email }}</span>
      </v-btn>
    </template>
    <v-card
      class="mx-auto text-uppercase"
      dark
      tile>
      <v-list dense>
        <v-subheader>user menu</v-subheader>
        <v-list-item-group>
          <!-- this is a router link -->
          <v-list-item to="/accounts/profile">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
        <v-list-item-group>
          <!-- this is a normal hyperlink -->
          <v-list-item href="/accounts/logout/">
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>
  </v-menu>
  <!-- this is a normal hyperlink -->
  <v-btn v-else text :href="'/accounts/login/?next=/%23' + $route.path">Login</v-btn>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    data: () => ({
      user_menu: false,
    }),
    watch: {
      user: {
        handler() {
          if (this.user.id !== null && this.user.archer.full_name === '') {
            if (this.$route.name !== 'profile') this.$router.push('/accounts/profile')
          }
        }
      }
    },
    computed: {
      ...mapState({
        user: state => state.user.user
      }),
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('user/checkUser')
    }
  }
</script>
