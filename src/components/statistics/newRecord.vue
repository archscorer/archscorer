<template>
  <v-dialog v-model="rec_dialog" max-width="650px">
    <template v-slot:activator="{ on }">
      <sup v-on="on" class="font-weight-medium">R</sup>
    </template>
    <v-card>
      <v-card-title>Exceeding current {{ record['scope'] }} record</v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col class="text-uppercase text-end">event:</v-col>
          <v-col>{{ event.name }}</v-col>
        </v-row>
        <v-row dense>
          <v-col class="text-uppercase text-end">date:</v-col>
          <v-col>{{ event.date_end }}</v-col>
        </v-row>
        <v-row v-for="(attr, i) in ['archer','format','class','score', 'scope']"
          :key="'rec_' + i"
          dense>
          <v-col class="text-uppercase text-end">{{ attr }}:</v-col>
          <v-col>{{ record[attr] }}</v-col>
        </v-row>
        <v-row>
          <v-col>
            <p class='text-caption'>
              * This view will appear only for scores, that exceed current record,
              but are not yet registered by {{ record['scope'] }} officials.
            </p>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer/>
        <v-btn text @click="rec_dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

  export default {
    props: {
      record: Object,
    },
    data: () => ({
      rec_dialog: false,
    }),
    computed: {
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
    }
  }

</script>

<style scoped>
  sup {
    cursor: pointer;
  }
</style>
