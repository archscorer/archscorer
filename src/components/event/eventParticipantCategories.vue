<template>
  <v-sheet v-if="pModel">
    <v-row dense>
      <v-col>
        <h4>Archer category options</h4>
        <p>We offer three quickselects how archer categories are organised for the
          competition. You can fine tune categories manually on the left to suit
          your specific competition requirements.</p>
        <p><v-btn small
          :text="arrayEquals(event.age_style_used, age_style_choices.FAAE)"
          @click="event.age_style_used=age_style_choices.FAAE">FAAE</v-btn> - see table <a href="https://www.faae.ee/2019/05/voistlusklassid/">here</a></p>
        <p><v-btn small
          :text="arrayEquals(event.age_style_used, age_style_choices.IFAA)"
          @click="event.age_style_used=age_style_choices.IFAA">IFAA</v-btn> - for IFAA competitions (Book of Rules, 2019)</p>
        <p><v-btn small
          :text="arrayEquals(event.age_style_used, age_style_choices.WA)"
          @click="event.age_style_used=age_style_choices.WA">WA</v-btn> - for World Archery competitions (Book of Rules 4, 2020)</p>
      </v-col>
      <v-col>
      <v-treeview
        v-model="event.age_style_used"
        selectable
        :items="all_choices"
      ></v-treeview>
    </v-col>
  </v-row>
  </v-sheet>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    props: {
      event: Object,
    },
    data: () => ({
      age_style_choices: {
        'IFAA': [
          'C|BB-C', 'C|BB-R', 'C|BH-C', 'C|BH-R', 'C|BL', 'C|BU', 'C|FS-C', 'C|FS-R', 'C|FU', 'C|HB', 'C|LB', 'C|TR',
          'J|BB-C', 'J|BB-R', 'J|BH-C', 'J|BH-R', 'J|BL', 'J|BU', 'J|FS-C', 'J|FS-R', 'J|FU', 'J|HB', 'J|LB', 'J|TR',
          'Y|BB-C', 'Y|BB-R', 'Y|BH-C', 'Y|BH-R', 'Y|BL', 'Y|BU', 'Y|FS-C', 'Y|FS-R', 'Y|FU', 'Y|HB', 'Y|LB', 'Y|TR',
          'A|BB-C', 'A|BB-R', 'A|BH-C', 'A|BH-R', 'A|BL', 'A|BU', 'A|FS-C', 'A|FS-R', 'A|FU', 'A|HB', 'A|LB', 'A|TR', 'A|**',
          'V|BB-C', 'V|BB-R', 'V|BH-C', 'V|BH-R', 'V|BL', 'V|BU', 'V|FS-C', 'V|FS-R', 'V|FU', 'V|HB', 'V|LB', 'V|TR',
          'S|BB-C', 'S|BB-R', 'S|BH-C', 'S|BH-R', 'S|BL', 'S|BU', 'S|FS-C', 'S|FS-R', 'S|FU', 'S|HB', 'S|LB', 'S|TR',
        ],
        'FAAE': [
          'C|BB-C', 'C|BB-R', 'C|FS-C', 'C|FS-R', 'C|FU', 'C|LB', 'C|TR',
          'J|BB-C', 'J|BB-R', 'J|BH-C', 'J|BH-R', 'J|BL', 'J|BU', 'J|FS-C', 'J|FS-R', 'J|FU', 'J|LB', 'J|TR',
          'A|BB-C', 'A|BB-R', 'A|BH-C', 'A|BH-R', 'A|BL', 'A|BU', 'A|FS-C', 'A|FS-R', 'A|FU', 'A|HB', 'A|LB', 'A|TR', 'A|**',
          'V|BB-C', 'V|BB-R', 'V|BH-C', 'V|BH-R', 'V|BL', 'V|BU', 'V|FS-C', 'V|FS-R', 'V|FU', 'V|LB', 'V|TR',
        ],
        'WA': [
          'C|L', 'C|I', 'C|R', 'C|C',
          'J|L', 'J|I', 'J|R', 'J|C',
          'A|L', 'A|I', 'A|R', 'A|C',
          'M|L', 'M|I', 'M|R', 'M|C',
        ],
      },
    }),
    computed: {
      ...mapState({
        pModel: state => state.events.participantModel,
      }),
      all_choices() {
        if (this.pModel) {
          return this.pModel.age_group.choices.map(a => {
            return {
              id: a.value,
              name: a.display_name,
              children: this.pModel.style.choices.map(s => {
                return {
                  id: a.value + '|' + s.value,
                  name: s.display_name + ' (' + s.value + ')',
                  parent: a.value,
                  value: s.value
                }
              })
            }
          })
        }
        return []
      }
    },
    methods: {
      arrayEquals(a, b) {
        return Array.isArray(a) &&
               Array.isArray(b) &&
               a.length === b.length &&
               a.every((val, index) => val === b[index]);
      }
    },
    created() {
      this.$store.dispatch('events/getParticipantOpts')
    }
  }

</script>
