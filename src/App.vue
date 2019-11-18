<template>
  <v-app>
    <v-app-bar app dark color="primary">
      <v-toolbar-title class="headline text-uppercase">
        <router-link
          to="/"
          tag="span"
          style="cursor: pointer">
          arch[scor]er
        </router-link>
      </v-toolbar-title>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"
        class="hidden-sm-and-up"></v-app-bar-nav-icon>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-xs-only">
        <v-btn text
          to="/events">
          Events
        </v-btn>
        <v-btn text
          to="/statistics">
          Statistics
        </v-btn>
        <v-btn text
          to="/clubs">
          Clubs
        </v-btn>
      </v-toolbar-items>
      <v-spacer></v-spacer>
      <AppLogin/>
    </v-app-bar>
    <v-navigation-drawer app v-model="drawer">
      <v-list dense>
        <v-list-item to="/">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        <v-list-item to="/events">
          <v-list-item-icon>
          </v-list-item-icon>
          <v-list-item-title>Events</v-list-item-title>
        </v-list-item>
        <v-list-item to="/statistics">
          <v-list-item-icon>
          </v-list-item-icon>
          <v-list-item-title>Statistics</v-list-item-title>
        </v-list-item>
        <v-list-item to="/clubs">
          <v-list-item-icon>
          </v-list-item-icon>
          <v-list-item-title>Clubs</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-content>

  </v-app>
</template>

<script>
  import AppLogin from '@/components/AppLogin.vue'

  export default {
    // name: 'ArchScorER',
    components: {
      AppLogin,
    },
    data: () => ({
      drawer: null,
    }),
  };
</script>
