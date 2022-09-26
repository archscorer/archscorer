<template>
  <v-dialog v-model="rec_dialog" max-width="650px">
    <template v-slot:activator="{ on }">
      <v-btn v-if='vanilla == true' v-on="on" color='primary' @click="init_vanilla()">Add Record</v-btn>
      <sup v-else v-on="on" class="font-weight-medium">R</sup>
    </template>
    <v-card>
      <v-card-title v-if='vanilla == true'>Add new record</v-card-title>
      <v-card-title v-else>Exceeding current {{ record['scope'] }} record</v-card-title>
      <v-card-text v-if="user.perms && user.perms.some(el => el === 'record')">
        <v-row v-for="(attr, i) in ['event','date','archer']"
          :key="'rec_s' + i"
          dense>
          <v-col class="text-uppercase text-end lowered">{{ attr }}:</v-col>
          <v-col>
            <v-text-field v-model="record[attr]"
              :hint="hints[attr]"
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
              :hint="hints[attr]"
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
            :hint="hints[attr]"
            :append-icon="edit[attr] ? 'mdi-pencil-outline' : 'mdi-pencil-off-outline'"
            :readonly="!edit[attr]"
            @click:append="edit[attr] = !edit[attr]"
            dense/>
          </v-col>
        </v-row>
        <v-row v-if="!vanilla">
          <v-col>
            <p class='text-caption'>
              * This view will appear only for scores, that exceed current record,
              but are not yet registered by {{ record['scope'] }} officials.
            </p>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-text v-else>
        <v-row v-for="(attr, i) in ['event','date','archer']"
          :key="'rec_s' + i"
          dense>
          <v-col class="text-uppercase text-end lowered">{{ attr }}:</v-col>
          <v-col>
            <v-text-field v-model="record[attr]"
              readonly
              dense/>
            </v-col>
        </v-row>
        <v-row dense>
          <v-col class="text-uppercase text-end lowered">class:</v-col>
          <v-col v-for="(attr, i) in ['age_group','gender','style']"
            :key="'rec_class' + i" cols="2">
            <v-text-field v-model="record[attr]"
              readonly
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
      vanilla: Boolean, // this indicates entering new (vanilla) record, not updating existing one
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
      },
      rules: {
        'event': '',
        'date': '',
        'archer': '',
        'format': '',
        'age_group': '',
        'gender': '',
        'style': '',
        'score': '',
        'scope': ''
      },
      hints: {
        'event': 'Event name',
        'date': 'valid data format expected yyyy-mm-dd',
        'archer': 'Archer full name',
        'format': 'one of "animal", "hunter", "field", "indoor" or "flint"',
        'age_group': "Valid IFAA age group [C,J,YA,A,V,S]",
        'gender': "M / F",
        'style': "Valid IFAA bow style i.e. BB-R",
        'score': "numeric value",
        'scope': "For national records association acronym"
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
      init_vanilla() {
        for (let attr in this.edit) {
          this.edit[attr] = true
        }
      },
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
