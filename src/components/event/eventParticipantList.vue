<template>
  <v-sheet>
    <v-alert
      v-if="hint_archive"
      type="info"
      prominent
      dismissible
    >
      The end date of this event has passed. Once all scores are entered and checked
      make sure to finish this event by making it inactive (archiving) it in the 'edit event' menu!
    </v-alert>
    <v-toolbar dense flat>
      <template v-if="event.is_open">
        <eventParticipantAdd action="Register"/>
        <eventParticipantAdd action="Add Me" v-if="user.id !== null && (!Array.isArray(p_user) || !p_user.length)"/>
      </template>
      <v-spacer />
      <template v-if="[event.creator, ...event.admins].includes(user.email)">
        <template v-if="$vuetify.breakpoint.smAndUp">
          <eventParticipantAdd action="Add Archer"/>
          <eventEdit/>
        </template>
        <template v-else>
          <v-menu
            :close-on-content-click="false"
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
                  <v-list-item inactive>
                    <v-list-item-content>
                    </v-list-item-content>
                    <v-list-item-action>
                      <eventParticipantAdd action="Add Archer"/>
                    </v-list-item-action>
                  </v-list-item>
                </v-list-item-group>
                <v-list-item-group>
                  <v-list-item inactive>
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
      <v-card-text>
        <v-data-table
          dense
          :mobile-breakpoint="300"
          :headers="p_table_header"
          :items="p_table"
          :search="p_search"
          :loading="loading"
          group-by="class"
          :items-per-page="50"
          multi-sort
        >
          <template v-slot:item.group="props"
            v-if="[event.creator, ...event.admins].includes(user.email) && !event.archive">
            <v-edit-dialog
              :return-value="props.item.group"
              :key="props.item.id"
              @save="save(props.item.id, {group: props.item.group})"
              @cancel="cancel"
              large
              persistent
            > {{ props.item.group }}
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.group"
                  counter="10"
                  single-line
                  autofocus
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </template>
          <template v-slot:item.end="props"
            v-if="[event.creator, ...event.admins].includes(user.email) && !event.archive">
            <v-edit-dialog
              :return-value="props.item.end"
              :key="props.item.id"
              @save="save(props.item.id, {group_target: props.item.end})"
              @cancel="cancel"
              large
              persistent
            > {{ props.item.end }}
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.end"
                  :rules="[v => !!v || 'Target nr for the participant.']"
                  type="number"
                  single-line
                  autofocus
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </template>
          <template v-slot:item.pos="props">
            <v-edit-dialog v-if="[event.creator, ...event.admins].includes(user.email) && !event.archive"
              :return-value="props.item.pos"
              :key="props.item.id"
              @save="save(props.item.id, {group_pos: props.item.pos})"
              @cancel="cancel"
              large
              persistent
            > {{ props.item.pos }} {{ props.item.has_account ? '*' : '' }}
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.pos"
                  :rules="[v => (!!v && v.length <= 1) || 'Position is marked with single capital letter']"
                  counter="1"
                  single-line
                  autofocus
                ></v-text-field>
              </template>
            </v-edit-dialog>
            <template v-else>
              {{ props.item.pos }}
            </template>
          </template>
          <template v-slot:item.action="props">
            <template v-if="(user.archer.id === props.item.aId && event.is_open) || [event.creator, ...event.admins].includes(user.email)">
              <v-icon small class="mr-2" @click="editP(props.item.id)">
                mdi-pencil
              </v-icon>
              <v-icon small @click="deleteP(props.item.id)">
                mdi-delete
              </v-icon>
            </template>
          </template>
        </v-data-table>
        <template  v-if="[event.creator, ...event.admins].includes(user.email) && !event.archive">
          <p class='text-caption'>Export to <v-btn x-small @click="export2excel()">excel</v-btn><br/>
          'Position *' - indicates that archer has user account and could be digital scorer.</p>
        </template>
      </v-card-text>
    </v-card>
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>Edit participant info for {{ p_meta.name }}</v-card-title>
        <eventParticipantDetails :participant="p_edit"
          :catering="event.catering"
          :level_class="event.use_level_class"
          :catering_choices="event.catering_choices.split('|')"/>
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
  import { json2excel } from 'js2excel'

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
      p_user: Array,
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
        comments: '',
        food: false,
        food_choices: []
      },
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
      loading() {
        return (this.p_table.length || Array.isArray(this.event.participants) ? false : true)
      },
      p_table_header() {
        let header = [
          { text: 'Name', value: 'name', width: '148px' },
        ]
        if (this.event.use_level_class) {
          header.push({ text: 'Classification', value: 'classification'})
        }
        header.push(...[
          { text: 'Class', value: 'class' },
          { text: 'Club', value: 'club' },
          { text: 'Group', value: 'group' },
          { text: 'End', value: 'end' },
          { text: 'Position', value: 'pos' },
        ])
        if (!this.event.archive && this.user.id) {
          if (this.event.is_open || [this.event.creator, ...this.event.admins].includes(this.user.email)) {
            header.push({ text: 'Actions', value: 'action', sortable: false, width: "1%" })
          }
          if (this.user.email === this.event.creator) {
            if (this.event.catering) {
              header.push({ text: 'Food', value: 'food' })
            }
            header.push(...[{ text: 'Contact', value: 'contact' },
                            { text: 'Comments', value: 'comments' }])
          }
        }
        return header
      },
      p_table() {
        if (Array.isArray(this.event.participants)) {
          return this.event.participants.map(function(p) {
            return {
              id: p.id,
              aId: p.archer.id,
              name: p.archer.full_name,
              classification: p.level_class,
              class: p.age_group + p.archer.gender + p.style,
              club: p.archer.club,
              group: p.group,
              end: p.group_target,
              pos: p.group_pos,
              has_account: p.archer.user,
              food: (p.food ? p.food_choices.split('|').join('; ') : 'No'),
              contact: (p.archer.contact || ''),
              comments: p.comments,
            }
          })
        } else {
          return []
        }
      },
      hint_archive() {
        if (this.event && [this.event.creator, ...this.event.admins].includes(this.user.email)) {
          if (new Date(this.event.date_end).setHours(23, 59) < new Date() && !this.event.archive) {
            return true
          }
        }
        return false
      }
    },
    methods: {
      ...mapActions('events', [
        'addParticipant',
        'delParticipant',
        'putParticipant',
      ]),
      save(pId, attr) {
        if (attr.food_choices) {
          attr.food_choices = attr.food_choices.join('|')
        }
        let p = Object.assign({}, this.event.participants.find(obj => obj.id === pId), attr)
        this.putParticipant({pId: p.id, participant: p}).then(() => {
          this.snack = true
          this.snackColor = 'success'
          this.snackText = 'Changes have been saved'
        })
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
          level_class: p.level_class,
          comments: p.comments,
          food: p.food,
          food_choices: (p.food ? p.food_choices.split('|') : [])
        }
        this.dialog = true
      },
      deleteP(pId) {
        let p = this.event.participants.find(obj => obj.id === pId)
        confirm(p.archer.full_name + ' will be removed from participant list' +
        ' (and their scorecards will be lost)') &&
        this.delParticipant({pId: p.id, eId: p.event})
      },
      export2excel() {
        let data = this.event.participants.map(function(p) {
          return {
            Class: p.age_group + p.archer.gender + p.style,
            Name: p.archer.full_name,
            Club: p.archer.club,
            Group: p.group,
            End: p.group_target,
            'Position': p.group_pos,
            'Has Account': p.archer.user,
            Food: (p.food ? p.food_choices.split('|').join('; ') : 'No'),
            Contact: (p.archer.contact || ''),
            Comments: p.comments,
          }
        })
        json2excel({data: data, name: 'participants'})
      }
    },
  }
</script>
