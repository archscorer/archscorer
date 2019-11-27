<template>
  <v-container v-if="pModel">
    <v-row dense>
      <v-col cols="4">
        <v-select
          v-model="participant.style"
          :items="pModel.style.choices"
          label="Style"
          item-text="display_name"
          dense
        ></v-select>
      </v-col>
      <v-col cols="4">
        <v-select
          v-model="participant.age_group"
          :items="pModel.age_group.choices"
          label="Age Group"
          item-text="display_name"
          dense
        ></v-select>
      </v-col>
      <v-col cols="4">
        <v-switch
          v-model="participant.eats"
          label="Catering"
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
  /*eslint no-console: ["error", { allow: ["warn", "error", "log"] }] */
  import { mapState } from 'vuex'

  export default {
    // name: "listCompetitonRegister",
    props: {
      participant: Object,
    },
    data: () => ({
      // TODO write validators for form fields: style, age, gender, full_name, email
      // TODO quicklink to register me (skip archer fields or autofill them)
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
