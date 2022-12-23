<template>

  <v-menu
    v-if="user.id !== null"
    v-model="user_menu"
    transition="slide-y-transition"
  >
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props">{{ user.email }}</v-btn>
    </template>
    <v-card
      class="mx-auto text-uppercase"
      tile>
      <v-list dense>
        <v-list-item type="subheader" title="user menu"></v-list-item>
        <v-list-item
          inactive
          title="Theme Dark">
          <v-list-item-action>
            <v-switch
              small
              v-model="$vuetify.theme.dark"
              hide-details
              ></v-switch>
          </v-list-item-action>
        </v-list-item>
        <v-list-item type="divider"></v-list-item>
        <!-- this is a router link -->
        <v-list-item to="/accounts/profile" prepend-icon="mdi-account" title="Profile"></v-list-item>
        <!-- this is a normal hyperlink -->
        <v-list-item href="/accounts/logout/" prepend-icon="mdi-logout" title="Logout"></v-list-item>
      </v-list>
    </v-card>
  </v-menu>
  <!-- this is a normal hyperlink -->
  <v-btn v-else :href="'/accounts/login/?next=/%23' + $route.path">Login</v-btn>
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
            if (this.$route.name !== 'profile') {this.$router.push('/accounts/profile')}
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
