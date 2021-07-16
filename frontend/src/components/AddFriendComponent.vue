<template>
  <div>
    <div id="add-friend-component">
      <sui-form name="groupForm" style="width: 40vw;" v-on:submit.prevent="validateForm()">
        <sui-input placeholder="Email Address" icon="users" v-model="emailAdd" style="margin-bottom: 10px"/>
        <div style="display: flex">
          <sui-input placeholder="Mobile Number" icon="users" v-model="mobNum" style="margin-bottom: 10px"/>

          <sui-button style="height: 37px; margin-left: 50px" content="Invite Contact" type="submit"/>
        </div>
      </sui-form>
    </div>
    <h1></h1>
    <h1></h1>
    <h1></h1>
    <sui-table single-line collapsing id="inner">
      <sui-table-header>
        <sui-table-row>
          <sui-table-header-cell>Full Name</sui-table-header-cell>
          <sui-table-header-cell>Username</sui-table-header-cell>
        </sui-table-row>
      </sui-table-header>
      <FriendNameRow v-for="friend in parsedFriend" :key="friend.id" :user="friend"></FriendNameRow>
    </sui-table>
    <h1></h1>
    <div id="add-friend-componentt">
      <sui-form name="groupForm" style="width: 40vw;" v-on:submit.prevent="validateForm2()">
        <div style="display: flex">
          <sui-dropdown
              :options="parsedUser"
              placeholder="Choose username"
              selection
              v-model="chosen.username"
          />
          <sui-button style="height: 37px; margin-left: 50px" content="Add as a friend" type="submit"
                      v-on:click.prevent="send_info()"/>
        </div>
      </sui-form>
    </div>
    <h1></h1>
    <br/>
  </div>
</template>

<script>
import {APIService} from "@/APIService";
import FriendNameRow from "@/components/FriendNameRow";

export default {
  name: "AddFriendComponent",
  components: {FriendNameRow},
  computed: {
    parsedFriend: function () {
      return this.friends
    },
    parsedFriendOpt: function () {
      return this.friends_options
    },
    parsedUser: function () {
      return this.usernames
    }
  },
  data() {
    return {
      friends: [],
      friends_options:[],
      clicked: '',
      chosen: {
        username: ""
      },
      del_chosen: {
        username: ""
      },
      emailAdd: '',
      mobNum: '',
      usernames: [],
      curr_username: '',
    };
  },
  methods: {
    validateForm() {
      if (this.emailAdd === '') {
        if (this.mobNum === '') {
          alert("No group name entered.");
          return false;
        }
      }
    },
    validateForm2() {
      if (this.chosen.username === '') {
        alert("No  username selected.");
        return false;
      }
    },
    validateForm3() {
      if (this.del_chosen.username === '') {
        alert("No  username selected.");
        return false;
      }
    },
    get_info: function () {
      console.log(APIService.KEY)
      this.$http.get(APIService.UPDATEINFO,
          {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
          .then(response => response.json())
          .then((data) => {
            this.curr_username = data.username
          })
          .catch(error => console.log(error))
    },
    get_friends: function () {
      this.$http.get(APIService.FRIEND,
          {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
          .then(response => response.json())
          .then((data) => {
            this.friends = data
          })
          .catch(error => console.log(error))
    },
    send_info: function () {
      this.$http.post(APIService.FRIEND, this.chosen,
          {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
          .catch(error => console.log(error))
      this.get_friends()
      this.get_all()
    },
    send_del: function () {
      this.$http.delete(APIService.FRIEND + this.del_chosen.username,  {
        emulateJSON: true,
        headers: {'Authorization': 'Token ' + APIService.KEY}
      })
          .catch(error => console.log(error))
      this.get_friends()
      this.get_all()
    },
    get_all: function () {
      this.$http.get(APIService.AUTH + '', {
        emulateJSON: true,
        headers: {'Authorization': 'Token ' + APIService.KEY}
      })
          .then(response => response.json())
          .then((data) => {
            this.usernames = [];
            for (let user of data) {
              if (user.username !== this.curr_username) {
                let bool = false;
                for (let friend of this.friends) {
                  if (user.username === friend.username) {
                    bool = true;
                  }
                }
                if (!bool) {
                  this.usernames.push({
                    text: user.username, key: user.username, value: user.username
                  })
                }
              }
            }
          })
    }
  },
  mounted() {
    this.get_info()
    this.get_friends()
    this.get_all()
  }
};
</script>

<style scoped>
#add-friend-component {
  position: relative;
  top: 100px;
  left: 25vw;
  width: 50vw;
  height: fit-content;
  padding: 10px;
  z-index: 900;
  gap: 10px 10px;
  border: solid gray thin;
  border-radius: 5px;
  background-color: dimgray;
}

#add-friend-componentt {
  position: relative;
  top: 100px;
  left: 25vw;
  width: 50vw;
  height: fit-content;
  padding: 10px;
  z-index: 900;
  gap: 10px 10px;
  border: solid gray thin;
  border-radius: 5px;
  background-color: dimgray;
}

#del-friend-componentt {
  position: relative;
  top: 100px;
  left: 25vw;
  width: 50vw;
  height: fit-content;
  padding: 10px;
  z-index: 900;
  gap: 10px 10px;
  border: solid gray thin;
  border-radius: 5px;
  background-color: dimgray;
}

#inner {
  width: 50%;
  margin: 0 auto;
}
</style>
