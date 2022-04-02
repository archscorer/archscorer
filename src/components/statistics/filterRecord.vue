<template>
  <v-menu top :close-on-content-click="false" v-model="menu">
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon v-bind="attrs" v-on="on">
        <v-icon small :color="filter ? 'primary' : ''">
          mdi-filter
        </v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-text>
        <v-text-field autofocus v-model="query" label="Enter filter query"
        @input="$emit('update:filter', query)"></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="$emit('update:filter', '');query = ''" small text color="primary">Clean</v-btn>
        <v-spacer/>
        <v-btn @click="menu = false" small text color="secondary">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>
</template>

<script>

  export default {
    props: {
      filter: String,
    },
    data: () => ({
      menu: false,
      query: '',
    }),
  }

</script>
