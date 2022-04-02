<template>
  <v-dialog v-model="rec_dialog" max-width="650px">
    <template v-slot:activator="{ on }">
      <sup v-on="on" class="font-weight-medium">R</sup>
    </template>
    <v-card>
      <v-card-title>Exceeding current {{ record['scope'] }} record</v-card-title>
      <v-card-text>
        <v-row v-for="(attr, i) in ['event','date','archer']"
          :key="'rec_s' + i"
          dense>
          <v-col class="text-uppercase text-end lowered">{{ attr }}:</v-col>
          <v-col>
            <v-text-field v-model="record[attr]"
              :append-icon="edit[attr] ? 'mdi-pencil-outline' : 'mdi-pencil-off-outline'"
              :readonly="!edit[attr]"
              @click:append="edit[attr] = !edit[attr]"
              dense/>
            </v-col>
        </v-row>
        <v-row dense>
          <v-col class="text-uppercase text-end lowered">class:</v-col>
          <v-col v-for="(attr, i) in ['age_group','gender','style']"
            :key="'rec_class' + i" cols="2">
            <v-text-field v-model="record[attr]"
              :append-icon="edit[attr] ? 'mdi-pencil-outline' : 'mdi-pencil-off-outline'"
              :readonly="!edit[attr]"
              @click:append="edit[attr] = !edit[attr]"
              dense/>
          </v-col>
        </v-row>
        <v-row v-for="(attr, i) in ['score','scope','format']"
          :key="'rec_e' + i"
          dense>
          <v-col class="text-uppercase text-end lowered">{{ attr }}:</v-col>
          <v-col><v-text-field v-model="record[attr]"
            readonly
            dense/>
          </v-col>
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
        <v-btn v-if="user.perms && user.perms.some(el => el === 'record')"
          color="primary"
          @click="addRecord(record); rec_dialog = false">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    props: {
      record: Object,
    },
    data: () => ({
      rec_dialog: false,
      edit: {
        'event': false,
        'date': false,
        'archer': false,
        'format': false,
        'age_group': false,
        'gender': false,
        'style': false,
        'score': false,
        'scope': false
      }
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
    },
    methods: {
      ...mapActions('statistics', [
        'addRecord',
      ]),
    }
  }
</script>

<style scoped>
  sup {
    cursor: pointer;
  }
  .lowered {
    margin-top: 0.5rem;
  }
</style>
