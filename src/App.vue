<template>
  <v-app>
    <v-toolbar
      class="px-3"
      color="primary"
      flat
      density="compact"
    >
      <v-toolbar-title class="headline text-uppercase">
        <router-link :to="'/'" custom v-slot="{ navigate }">
            <span @click="navigate" role="link"> arch[scor]er </span>
        </router-link>
      </v-toolbar-title>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="hidden-sm-and-up"/>

      <v-spacer/>

      <v-toolbar-items class="hidden-xs-only">
        <v-btn to="/events"> Events</v-btn>
        <v-btn to="/series">Series</v-btn>
        <v-menu open-on-hover offset-y>
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props">Statistics</v-btn>
          </template>
            <v-list dark nav dense class="text-uppercase" color="primary">
              <v-list-item link to="/statistics/archer/rounds" title="Archer Rounds"></v-list-item>
              <v-list-item link to="/statistics/records" title="Records"></v-list-item>
            </v-list>
        </v-menu>
        <v-btn to="/clubs">Clubs</v-btn>
      </v-toolbar-items>
      <v-spacer/>
      <loginMenu/>
    </v-toolbar>
    <v-navigation-drawer v-model="drawer">
      <v-list>
        <v-list-item to="/" prepend-icon="mdi-home" title="Home"></v-list-item>
        <v-list-item to="/events" prepend-icon="mdi-bullseye-arrow" title="Events"></v-list-item>
        <v-list-item to="/series" prepend-icon="mdi-trophy" title="Series"></v-list-item>
        <v-list-group value="Statistics">
          <template v-slot:activator="{ props }">
            <v-list-item v-bind="props" prepend-icon="mdi-matrix" title="Statistics"></v-list-item>
          </template>
          <v-list-item to="/statistics/archer/rounds" title="Archer Rounds"></v-list-item>
          <v-list-item to="/statistics/records" title="Records"></v-list-item>
        </v-list-group>
        <v-list-item to="/clubs" prepend-icon="mdi-account-group" title="Clubs"></v-list-item>
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
      this.$store.dispatch('clubs/getClubs')
    }
  };
</script>

<style>
  th {
    white-space: nowrap;
  }
  a {
    text-decoration: none;
    font-weight: 500;
  }
</style>
