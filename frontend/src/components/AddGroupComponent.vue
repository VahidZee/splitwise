<template>
  <div id="add-group-component">
    <sui-form name="groupForm" style="width: 40vw;" v-on:submit.prevent="validateForm()">
      <sui-input placeholder="Group name" icon="users" v-model="name" style="margin-bottom: 10px"/>
      <div style="display: flex">
        <sui-form-field style="width: 25vw; height: fit-content; margin-right: 10px; margin-bottom: 0px">
          <sui-dropdown
              multiple
              :options="friends"
              placeholder="Choose friends"
              selection
              v-model="chosen"
          />
        </sui-form-field>
        <sui-button style="height: inherit" content="Create Group" type="submit" @click="submitForm"/>
      </div>
    </sui-form>
  </div>
</template>

<script>
import {APIService} from "../APIService";

export default {
  name: "AddGroupComponent",
  data() {
    return {
      friends: [],
      chosen: [],
      clicked: '',
      name: '',
      groupID: '',
    };
  },
  methods: {
    validateForm() {
      if (this.name === '') {
        alert("No group name entered.");
        return false;
      }
      if (this.chosen == null) {
        alert("No friends were chosen.");
        return false;
      }
    },
    submitForm() {
      this.$http.post(APIService.GROUP + "", {'name': this.name}, {
        emulateJSON: true,
        headers: {'Authorization': 'Token ' + APIService.KEY}
      })
          .then(response => response.json())
          .then((data) => {
            this.groupID = data.id;
            for (let friend of this.chosen) {
              this.$http.post(APIService.GROUP + this.groupID + '/add_member/', {'username': friend}, {
                emulateJSON: true,
                headers: {'Authorization': 'Token ' + APIService.KEY}
              })
                  .then(response => response.status)
                  .then((data) => console.log(friend + data))
            }
          })
      alert('Group created!');
    }
  },
  mounted() {
    this.$http.get(APIService.FRIEND + '', {
      emulateJSON: true,
      headers: {'Authorization': 'Token ' + APIService.KEY}
    })
        .then(response => response.json())
        .then((data) => {
          this.friends = [];
          for (let friend of data) {
            this.friends.push({
              text: friend.email, key: friend.username, value: friend.username
            })
          }
        })
  }
};
</script>

<style scoped>
#add-group-component {
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
</style>