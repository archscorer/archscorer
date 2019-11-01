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
          to="/competitions">
          Competitons
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
      <v-btn text rounded>
        <span class="mr-2">login</span>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer app v-model="drawer">
      <v-list dense>
        <v-list-item to="/">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        <v-list-item to="/competitions">
          <v-list-item-icon>
          </v-list-item-icon>
          <v-list-item-title>Competitions</v-list-item-title>
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
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>

  </v-app>
</template>

<script>

export default {
  name: 'Arch[scor]er',

  data: () => ({
    drawer: null,
  }),
};
</script>
