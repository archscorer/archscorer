<template>
  <v-container>
    <v-row>
      <v-col cols="4">
        <v-text-field autofocus
          v-model="value.full_name"
          label="Your full name*"
          :rules="[v => !!v || 'This field is required']"
        >
        </v-text-field>
      </v-col>
      <v-col cols="4">
        <v-select
          v-model="value.gender"
          :items="[{'text': 'Male', 'value': 'M'}, {'text': 'Female', 'value': 'F'}]"
          label="Gender*"
          :rules="[v => !!v || 'Choice must be made :)']"
        ></v-select>
      </v-col>
      <v-col cols="4">
        <v-select
          v-if="clubs"
          v-model="value.club"
          :disabled="value.events && value.events.length && new Date().getMonth() !== 0 ? true : false"
          :items="clubs"
          label="Choose Club*"
          :rules="[v => !!v || 'Choose ..no club.. if other options are not suitable']"
          item-text="name"
          item-value="id"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4">
        <v-text-field
          v-model="value.email"
          label="Contact email address*"
          :rules="[v => !!v || 'This field is required',
                   v => /.+@.+\..+/.test(v) || 'E-mail must be valid']"
        >
        </v-text-field>
      </v-col>
      <v-col cols="4">
        <v-text-field
          v-model="value.phone"
          label="Contact phone number"
        >
        </v-text-field>
      </v-col>
      <v-col cols="4">
        <v-text-field
          v-model="value.nat_id"
          label="Archer national ID"
          hint="FAAE ID in Estonia - first 7 digits from your national ID code."
        >
        </v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  // TODO: test january as club changing month before making it public
  export default {
    props: {
      value: Object,
      clubs: Array,
    }
  }
</script>
