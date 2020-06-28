<template>
  <v-container v-if="club">
    <v-card>
      <v-card-title v-text="club.name + ' ('+ club.name_short +')'"></v-card-title>
      <v-card-text>
        <p v-html="club.contact"></p>
        <p v-html="club.description"></p>
        <template v-if="user_is_member_or_admin">
          <v-row>
            <v-col cols="8">
              <template v-if="club.admins.includes(user.email)">
                <clubEdit />
                <v-btn color="primary" class="mx-2" @click="addA()">Add member</v-btn>
              </template>
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model="m_search"
                append-icon="mdi-magnify"
                label="Search member"
                single-line
                hide-details
              ></v-text-field>
            </v-col>
          </v-row>
          <v-data-table
            dense
            :headers="m_table_header"
            :items="m_table"
            :search="m_search"
            :items-per-page="50"
            multi-sort>
            <template v-slot:item.ops="props">
              <template v-if="club.admins.includes(user.email)">
                <v-icon small class="mr-2" @click="editA(props.item.id)">
                  mdi-pencil
                </v-icon>
                <v-icon small @click="deleteA(props.item.id)"
                  v-if="!props.item.events">
                  mdi-delete
                </v-icon>
              </template>
            </template>
          </v-data-table>
        </template>
        <p v-else>
          Club member list is visible only to club members and club administrators.
          Also you need to be logged in!
        </p>
      </v-card-text>
    </v-card>
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>Edit Archer profile</v-card-title>
        <v-card-text>
          <v-form v-model="valid">
            <archerDetails v-model="a_edit" :clubs="[{name: '*_kick out_*', id: 1}, club]"/>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn text @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" text @click="putMember(a_edit); dialog = false">{{ action }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
  <v-overlay v-else>
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-overlay>
</template>

<script>
  import clubEdit from '@/components/club/clubEdit.vue'
  import archerDetails from '@/components/archer/archerDetails.vue'
  import { mapState, mapActions } from 'vuex'

  export default {
    // name: 'Club',
    components: {
      clubEdit,
      archerDetails
    },
    data: () => ({
      m_search: '',
      valid: false,
      action: '',
      dialog: false,
      a_edit: {},
    }),
    computed: {
      ...mapState({
        user: state => state.user.user,
      }),
      club() {
        return this.$store.getters['clubs/clubById'](parseInt(this.$route.params.id))
      },
      m_table_header() {
        let header = [
          { text: 'Name', value: 'full_name'},
          { text: 'Activity', value: 'events', width: '90px'}
        ]
        if (this.club.admins.includes(this.user.email)) {
          header.push(...[{ text: 'Gender', value: 'gender' },
                          { text: 'E-mail', value: 'email' },
                          { text: 'Phone', value: 'phone' },
                          { text: 'National ID', value: 'nat_id' },
                          { text: 'Edit', value: 'ops', sortable: false, width: "80px" }])
        }
        return header
      },
      m_table() {
        if (Array.isArray(this.club.members)) {
          return this.club.members.map(function(m) {
            let member = {full_name: m.full_name,
                          events: m.events.length ? m.events.length : null}
            if (this.club.admins.includes(this.user.email)) {
              return Object.assign(member, {id: m.id,
                                            gender: m.gender,
                                            email: m.email,
                                            phone: m.phone,
                                            nat_id: m.nat_id})
            }
            return member
          }, this)
        } else {
          return []
        }
      },
      user_is_member_or_admin() {
        if (!this.user.id || this.user.email === "") {
          return false
        } else if (this.club.admins.includes(this.user.email)) {
          return true
        } else if (Array.isArray(this.club.members)) {
          return this.club.members.map(m => m.email).includes(this.user.email) ||
                 this.club.members.map(m => m.email).includes(this.user.archer.email)
        }
        return false
      }
    },
    methods: {
      ...mapActions('clubs', [
        'putMember',
        'delMember'
      ]),
      editA(aId) {
        this.a_edit = this.club.members.find(obj => obj.id === aId)
        this.action = 'Save changes'
        this.dialog = true
      },
      deleteA(aId) {
        let a = this.club.members.find(obj => obj.id === aId)
        confirm(a.full_name + ' will be permanently deleted. This action' +
        ' can not be undone!') &&
        this.delMember({aId: a.id, cId: a.club})
      },
      addA() {
        this.a_edit = {
          id: null,
          full_name: '',
          gender: '',
          club: this.club.id,
          email: '',
          phone: '',
          nat_id: '',
        }
        this.action = 'Add archer'
        this.dialog = true
      }
    },
    created() {
      //do something after creating vue instance
      this.$store.dispatch('clubs/updateClub', parseInt(this.$route.params.id)).catch(() => {
        this.$router.push('/clubs')
      })
    },
  }
</script>
