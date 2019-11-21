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
        <v-list-item-group color="primary">
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
        <v-list-item-group>
          <v-list-item @click="userLogout()" href="/api-auth/logout/?next=/">
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
  <v-btn v-else text
    :href="'/api-auth/login/?next=/%23' + $route.path">
    <span class="mr-2">login</span>
  </v-btn>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({
      user_menu: false,
    }),
    computed: {
      ...mapState({
        user: state => state.user.user
      })
    },
    methods: {
      ...mapActions('user', [
        'userLogout'
      ])
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('user/checkUser')
    }
  }
</script>
