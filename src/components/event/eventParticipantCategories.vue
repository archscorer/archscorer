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
          @click="event.age_style_used=age_style_choices.FAAE">FAAE</v-btn> - for Field Archery Association of Estonia. See table <a href="https://www.faae.ee/2019/05/voistlusklassid/" target="_blank">here</a></p>
        <p><v-btn small
          :text="arrayEquals(event.age_style_used, age_style_choices.IFAA)"
          @click="event.age_style_used=age_style_choices.IFAA">IFAA</v-btn> - for IFAA competitions (Book of Rules, 2019)</p>
        <p><v-btn small
          :text="arrayEquals(event.age_style_used, age_style_choices.EAA)"
          @click="event.age_style_used=age_style_choices.EAA">EAA</v-btn> - for Estonian Archery Association. See table <a href="http://www.vibuliit.ee/uus/wp-content/uploads/2021/02/vanuseklassid.pdf" target="_blank">here</a></p>
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
          'YA|BB-C', 'YA|BB-R', 'YA|BH-C', 'YA|BH-R', 'YA|BL', 'YA|BU', 'YA|FS-C', 'YA|FS-R', 'YA|FU', 'YA|HB', 'YA|LB', 'YA|TR',
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
        'EAA': [
          'T|L', 'T|I', 'T|R', 'T|C',
          'C|L', 'C|I', 'C|R', 'C|C',
          'CA|L', 'CA|I', 'CA|R', 'CA|C',
          'J|L', 'J|I', 'J|R', 'J|C',
          'A|L', 'A|I', 'A|R', 'A|C',
          'V|L', 'V|I', 'V|R', 'V|C',
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
