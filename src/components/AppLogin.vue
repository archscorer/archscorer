<template>
  <v-menu
    v-if="user.id !== null"
    v-model="logout_menu"
    :close-on-content-click="false"
    transition="slide-y-transition"
    offset-y
  >
    <template v-slot:activator="{ on }">
      <v-btn text
        rounded
        v-on="on">
        <span class="mr-2">{{ user.email }}</span>
      </v-btn>
    </template>
    <v-card>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="logout_menu = false;userLogout()">Logout</v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-menu>
  <v-menu
    v-else
    v-model="login_menu"
    :close-on-content-click="false"
    transition="slide-y-transition"
    offset-y
  >
    <template v-slot:activator="{ on }">
      <v-btn text
        rounded
        v-on="on">
        <span class="mr-2">login</span>
      </v-btn>
    </template>
    <v-form v-model="valid">
      <v-card class="pa-5" min-width="250px">
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="username"
              :rules="emailRules"
              label="email address"
              append-icon="mdi-at"
              required></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="password"
                :append-icon="passw_show ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="passwRules"
                :type="passw_show ? 'text' : 'password'"
                name="input-10-1"
                label="Password"
                @click:append="passw_show = !passw_show"
              ></v-text-field>
            </v-col>
          </v-row>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="login_menu = false;userLogin({username, password})">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-menu>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({
      login_menu: false,
      logout_menu: false,
      passw_show: false,
      valid: false,

      username: '',
      password: '',

      emailRules: [v => !!v || 'email address is required'],
      passwRules: [v => !!v || 'password is required'],
    }),
    computed: {
      ...mapState({
        user: state => state.user.user
      })
    },
    methods: {
      ...mapActions('user', [
        'userLogin',
        'userLogout'
      ])
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('user/checkUser')
    }
  }
</script>
