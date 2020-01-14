<template>
  <v-container v-if="pModel">
    <v-row dense>
      <v-col cols="4">
        <v-select
          v-model="participant.style"
          :items="pModel.style.choices"
          label="Style*"
          :rules="[v => !!v || 'Bow style is required']"
          item-text="display_name"
          dense
        ></v-select>
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
    </v-row>
    <v-row dense>
      <v-col cols="12">
        <v-textarea
          outlined
          v-model="participant.comments"
          label="Comments to organiser(s)"
        ></v-textarea>
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
    },
    data: () => ({
      //
    }),
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
