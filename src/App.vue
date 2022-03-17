<template>
  <v-app>
    <v-app-bar app dark color="primary">
      <v-toolbar-title class="headline text-uppercase">
        <router-link
          :to="'/'"
          style="cursor: pointer"
          custom v-slot="{ navigate }">
            <span @click="navigate" @keypress.enter="navigate" role="link">
              arch[scor]er
            </span>
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
          to="/series">
          Series
        </v-btn>
        <v-menu
             open-on-hover offset-y
             close-on-content-click
             min-width="auto"
             rounded="0"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn text v-bind="attrs" v-on="on">Statistics</v-btn>
          </template>
            <v-list dark nav dense class="text-uppercase" color="primary">
              <v-list-item
                      link to="/statistics/archer/rounds">
                  Archer Rounds
              </v-list-item>
              <v-list-item
                      link to="/statistics/records">
                  Records
              </v-list-item>
            </v-list>
        </v-menu>
        <v-btn text
          to="/clubs">
          Clubs
        </v-btn>
      </v-toolbar-items>
      <v-spacer></v-spacer>
      <loginMenu/>
    </v-app-bar>
    <v-navigation-drawer app disable-resize-watcher v-model="drawer">
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
        <v-list-item to="/series">
          <v-list-item-icon>
          </v-list-item-icon>
          <v-list-item-title>Series</v-list-item-title>
        </v-list-item>
        <v-list-group
        :value="false"
        no-action
        prepend-icon="mdi-matrix"
        >
        <template v-slot:activator>
          <v-list-item-title>Statistics</v-list-item-title>
        </template>
        <v-list-item to="/statistics/archer/rounds">
          <v-list-item-title>Archer Rounds</v-list-item-title>
        </v-list-item>
          <v-list-item to="/statistics/records">
          <v-list-item-title>Records</v-list-item-title>
        </v-list-item>
        </v-list-group>
        <v-list-item to="/clubs">
          <v-list-item-icon>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Clubs</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <!-- <v-container fluid> -->
        <router-view></router-view>
      <!-- </v-container> -->
    </v-main>

  </v-app>
</template>

<script>
  import loginMenu from '@/components/accounts/loginMenu.vue'

  export default {
    // name: 'ArchScorER',
    components: {
      loginMenu,
    },
    data: () => ({
      drawer: false,
    }),
    created() {
      this.$store.dispatch('courses/getCourses')
      this.$store.dispatch('statistics/getRecords')
    }
  };
</script>

<style>
  th {
    white-space: nowrap;
  }
  a {
    text-decoration: none;
    font-weight: bold;
  }
</style>
