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
        <v-row dense
          v-if="[event.creator, ...event.admins].includes(user.email)">
          <v-col>
            <v-select
              v-model="group_by"
              dense
              :items="[{ text: '--disabled--', value: null },
                      { text: 'Class', value: 'class'},
                      { text: 'End', value: 'end'}]"
              label="organise archers by">
            </v-select>
            <p>Export end assignments to <v-btn x-small color="primary" @click="endAssignments2pdfProxy()">PDF</v-btn><br/>
            Export all participant data to <v-btn x-small color="green" dark @click="export2excel()">EXCEL</v-btn></p>
          </v-col>
        </v-row>
        <v-data-table
          dense
          :mobile-breakpoint="300"
          :headers="p_table.header"
          :items="p_table.data"
          :search="p_search"
          :loading="loading"
          :group-by="group_by"
          :items-per-page="4 * 28"
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
                  @focus="$event.target.select()"
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
                  @focus="$event.target.select()"
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
                  @focus="$event.target.select()"
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
      </v-card-text>
      <v-card-actions>
        <template  v-if="[event.creator, ...event.admins].includes(user.email) && !event.archive">
          <p class='text-caption'>'Position *' - indicates that archer has user account and could be digital scorer.</p>
        </template>
      </v-card-actions>
    </v-card>
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>Edit participant info for {{ p_meta.name }}</v-card-title>
        <eventParticipantDetails :participant="p_edit"
          :catering="event.catering"
          :level_class="event.use_level_class"
          :catering_choices="event.catering_choices.split('|')"
          :age_style_choices="event.age_style_used.split(',')"/>
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
  import { json2excel } from 'js2excel'

  import { mapState, mapActions } from 'vuex'

  import eventEdit from '@/components/event/eventEdit.vue'
  import eventParticipantDetails from '@/components/event/eventParticipantDetails.vue'
  import eventParticipantAdd from '@/components/event/eventParticipantAdd.vue'
  import rankingService from '@/services/rankingService'
  import pdfService from '@/services/pdfService'

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
      group_by: 'class',
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
      p_table() {
        let p_table = {header: [{ text: 'Name',
                                  value: 'name',
                                  width: '175px' }],
                       data: []}
        // populate table header
        if (this.event.use_level_class) {
          p_table.header.push({ text: 'Classif.', value: 'classification'})
        }
        p_table.header.push(...[
          { text: 'Class', value: 'class' },
          { text: 'Club', value: 'club' },
          { text: 'Group', value: 'group' },
          { text: 'End', value: 'end' },
          { text: 'Position', value: 'pos' },
        ])
        if (!this.event.archive && this.user.id) {
          if (this.event.is_open || [this.event.creator, ...this.event.admins].includes(this.user.email)) {
            p_table.header.push({ text: 'Actions', value: 'action', sortable: false, width: "1%" })
          }
          if ([this.event.creator, ...this.event.admins].includes(this.user.email)) {
            p_table.header.push({ text: 'Score', value: 'sum'})
          }
          if (this.user.email === this.event.creator) {
            if (this.event.catering) {
              p_table.header.push({ text: 'Food', value: 'food' })
            }
            p_table.header.push(...[{ text: 'Contact', value: 'contact' },
                            { text: 'Comments', value: 'comments' }])
          }
        }
        // populate table data part
        if (Array.isArray(this.event.participants)) {
          let so = this.event.rounds.find(r => r.course_details.type === 's')
          so = so ? so.id : null
          p_table.data =  this.event.participants.map(p => {
            return {
              id: p.id,
              aId: p.archer.id,
              name: p.archer.full_name,
              classification: p.level_class,
              class: rankingService.getClass(p, this.event.ignore_gender),
              club: p.archer.club_details.name_short,
              group: p.group,
              end: p.group_target,
              pos: p.group_pos,
              has_account: p.archer.user,
              sum: ([this.event.creator, ...this.event.admins].includes(this.user.email) && !this.event.archive ? rankingService.participantScore(p, so) : null),
              food: (p.food ? p.food_choices.split('|').join('; ') : 'No'),
              contact: (p.archer.contact || ''),
              comments: p.comments,
            }
          })
        }
        return p_table
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
        let so = this.event.rounds.find(obj => obj.course_details.type === 's')
        so = so ? so.id : null
        let data = this.event.participants.map(p => {
          return {
            Class: rankingService.getClass(p, this.event.ignore_gender),
            Name: p.archer.full_name,
            Cassification: p.level_class,
            Club: p.archer.club_details.name_short,
            Group: p.group,
            End: p.group_target,
            'Position': p.group_pos,
            'Has Account': p.archer.user,
            Score: rankingService.participantScore(p, so),
            Food: (p.food ? p.food_choices.split('|').join('; ') : 'No'),
            Contact: (p.archer.contact || ''),
            Comments: p.comments,
          }
        })
        json2excel({data: data, name: 'participants'})
      },
      endAssignments2pdfProxy() {
        pdfService.endAssignments2pdf(this.event, this.p_table, this.$route.path)
      }
    },
  }
</script>

<style scoped>
  .v-select {
    max-width: 120px;
  }
</style>
