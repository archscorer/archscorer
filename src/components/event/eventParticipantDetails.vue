<template>
  <v-container v-if="pModel">
    <v-row dense>
      <v-col cols="4">
        <v-select
          v-model="participant.style"
          :items="pModel.style.choices"
          label="Style*"
          :rules="[v => !!v || 'Bow style is required']"
          dense
        >
          <template v-slot:item="data">
            {{ data.item.value }} -- {{ data.item.display_name }}
          </template>
          <template v-slot:selection="data">
            {{ data.item.value }}
          </template>
        </v-select>
      </v-col>
      <v-col cols="4">
        <v-select
          v-model="participant.age_group"
          :items="pModel.age_group.choices"
          label="Age Group*"
          :rules="[v => !!v || 'Age Group is required']"
          item-text="display_name"
          dense
        ></v-select>
      </v-col>
      <v-col cols="4">
        <v-switch
          v-if="catering"
          v-model="participant.food"
          :label="participant.food ? 'I will eat' : 'I will not eat'"
          color="primary"
        ></v-switch>
      </v-col>
      <v-col v-if="level_class" cols="3">
        <v-select
          v-model="participant.level_class"
          :items="classification_classes"
          label="Classification Class"
          dense
        ></v-select>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="8">
        <v-textarea
          outlined
          v-model="participant.comments"
          label="Comments to organiser(s)"
        ></v-textarea>
      </v-col>
      <v-col cols="4" v-if="participant.food">
        <template v-for="meal of catering_choices">
          <v-checkbox dense v-model="participant.food_choices"
            :label="meal"
            :value="meal"
            :key="meal"
            :rules="[v => v.length > 0 || 'choose at least one meal']"/>
        </template>
      </v-col>
    </v-row>
  </v-container>
  <v-container v-else>
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    props: {
      participant: Object,
      catering: Boolean,
      level_class: Boolean,
      catering_choices: Array,
    },
    data: () => ({
      classification_classes : [
        {text: 'A', value: 'A'},
        {text: 'B', value: 'B'},
        {text: 'C', value: 'C'},
        {text: '*', value: '*'},
      ]
    }),
    watch: {
      participant: {
        deep: true,
        handler(p) {
          if (p.food && this.catering_choices.length === 1 &&
              p.food_choices !== this.catering_choices) {
            this.$nextTick(() => {
              p.food_choices = this.catering_choices
            })
          }
          if (!p.food && p.food_choices.length) {
            p.food_choices = []
          }
        }
      }
    },
    computed: {
      ...mapState({
        pModel: state => state.events.participantModel,
      }),
    },
    created() {
      this.$store.dispatch('events/getParticipantOpts')
    }
  }
</script>
