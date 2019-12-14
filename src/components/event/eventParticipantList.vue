<template>
  <v-sheet>
    <v-toolbar dense flat>
      <eventParticipantAdd action="Register" v-if="event.is_open"/>
      <eventParticipantAdd action="Add Me" v-if="user.id !== null && p_user === null"/>
      <v-spacer />
      <template v-if="user.email === event.creator">
        <template v-if="$vuetify.breakpoint.smAndUp">
          <eventParticipantAdd action="Add Archer"/>
          <eventEdit/>
        </template>
        <template v-else>
          <v-menu
            v-model="creator_menu"
          >
            <template v-slot:activator="{ on }">
              <v-btn icon
                v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-card
              class="text-uppercase"
              tile>
              <v-list dense>
                <v-subheader>admin menu</v-subheader>
                <v-list-item-group>
                  <v-list-item>
                    <v-list-item-content>
                    </v-list-item-content>
                    <v-list-item-action>
                      <eventParticipantAdd action="Add Archer"/>
                    </v-list-item-action>
                  </v-list-item>
                </v-list-item-group>
                <v-list-item-group>
                  <v-list-item>
                    <v-list-item-content>
                    </v-list-item-content>
                    <v-list-item-action>
                      <eventEdit/>
                    </v-list-item-action>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-card>
          </v-menu>
        </template>
      </template>
    </v-toolbar>
    <v-card>
      <v-card-title>
      <small>Registered Archers</small>
      <v-spacer />
      <v-text-field
        v-model="p_search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
      <v-data-table
        dense
        :headers="p_table_header"
        :items="p_table"
        :search="p_search"
        group-by="class"
        :items-per-page="50"
      >
        <template v-slot:item.start_group="props" v-if="user.email === event.creator && event.archive === false">
          <v-edit-dialog
            :return-value="props.item.start_group"
            :key="props.item.id"
            @save="save(props.item.id, {start_group: props.item.start_group})"
            @cancel="cancel"
          > {{ props.item.start_group }}
            <template v-slot:input>
              <v-text-field
                v-model="props.item.start_group"
                :rules="start_group_rules"
                type="number"
                single-line
                autofocus
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>
        <template v-slot:item.action="{ item }" v-if="event.archive === false">
          <template v-if="(user.archer.id === item.aId && event.is_open) || user.email === event.creator">
            <v-icon small class="mr-2" @click="editP(item.id)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteP(item.id)">
              mdi-delete
            </v-icon>
          </template>
        </template>
      </v-data-table>
    </v-card>
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>Edit participant info for {{ p_meta.name }}</v-card-title>
        <eventParticipantDetails :participant="p_edit"/>
        <v-card-actions>
          <v-spacer/>
          <v-btn text @click="cancel(); dialog = false">Cancel</v-btn>
          <v-btn color="primary" text @click="save(p_meta.id, p_edit); dialog = false">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
      {{ snackText }}
      <v-btn text @click="snack = false">Close</v-btn>
    </v-snackbar>
  </v-sheet>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import eventEdit from '@/components/event/eventEdit.vue'
  import eventParticipantDetails from '@/components/event/eventParticipantDetails.vue'
  import eventParticipantAdd from '@/components/event/eventParticipantAdd.vue'

  export default {

    components: {
      eventEdit,
      eventParticipantDetails,
      eventParticipantAdd,
    },
    props: {
      p_user: Object,
    },
    data: () => ({
      p_search: '',
      p_meta: {
        id: null,
        name: null,
      },
      p_edit: {
        age_group: '',
        style: '',
        eats: '',
        comments: '',
        start_group: '',
      },
      p_table_header: [
        { text: 'Name', value: 'name' },
        { text: 'Class', value: 'class' },
        { text: 'Club', value: 'club' },
        { text: 'Eats', value: 'eats', width: "80px" },
        { text: 'Group', value: 'start_group', width: "90px" },
        { text: 'Actions', value: 'action', sortable: false, width: "1%" },
      ],
      start_group_rules: [
        v => !!v || 'required',
      ],
      dialog: false,
      creator_menu: false,
      snack: false,
      snackColor: '',
      snackText: '',
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
      event() {
        return this.$store.getters['events/eventById'](parseInt(this.$route.params.id))
      },
      p_table() {
        if (Array.isArray(this.event.participants)) {
          return this.event.participants.map(function(p) {
            return {
              id: p.id,
              aId: p.archer.id,
              name: p.archer.full_name,
              class: p.age_group + p.archer.gender + p.style,
              club: p.archer.club,
              eats: (p.eats ? "Yes" : "No"),
              start_group: p.start_group,
            }
          })
        } else {
          return []
        }
      },
    },
    methods: {
      ...mapActions('events', [
        'addParticipant',
        'delParticipant',
        'putParticipant',
      ]),
      save(pId, attr) {
        let p = this.event.participants.find(obj => obj.id === pId)
        this.putParticipant({pId: p.id, participant: attr})
        this.snack = true
        this.snackColor = 'success'
        this.snackText = 'Changes have been saved'
      },
      cancel() {
        this.snack = true
        this.snackColor = 'error'
        this.snackText = 'Canceled'
      },
      editP(pId) {
        let p = this.event.participants.find(obj => obj.id === pId)
        this.p_meta = {id: p.id, name: p.archer.full_name}
        this.p_edit = {
          age_group: p.age_group,
          style: p.style,
          eats: p.eats,
          comments: p.comments,
          start_group: p.start_group,
          event: this.event.id,
        }
        this.dialog = true
      },
      deleteP(pId) {
        let p = this.event.participants.find(obj => obj.id === pId)
        confirm(p.archer.full_name + ' will be removed from participant list') && this.delParticipant({pId: p.id, eId: p.event})
      }
    },
  }
</script>
