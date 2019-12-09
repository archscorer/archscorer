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
          <v-list-item @click="passUserLogout()">
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
  <AppLoginDialog v-else :csrf="getCSRFCookie"/>
</template>

<script>
  import axios from 'axios'
  import Cookies from 'js-cookie'

  import AppLoginDialog from '@/components/accounts/AppLoginDialog.vue'

  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({
      user_menu: false,
    }),
    components: {
      AppLoginDialog,
    },
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
      getCSRFCookie() {
        return Cookies.get('csrftoken')
      }
    },
    methods: {
      ...mapActions('user', [
        'userLogout'
      ]),
      passUserLogout() {
        axios({
          method: 'post',
          url: '/accounts/logout/',
          next: '/',
          headers: {
            'X-CSRFToken': this.getCSRFCookie,
          }
        }).then(() => {
          this.userLogout()
          if (this.$route.path !== '/') this.$router.push('/')
        })
      },
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('user/checkUser')
    }
  }
</script>
