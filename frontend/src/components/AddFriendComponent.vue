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
    <div id="add-friend-componentt">
      <sui-form name="groupForm" style="width: 40vw;" v-on:submit.prevent="validateForm2()">
        <div style="display: flex">
          <sui-dropdown
              multiple
              :options="usernames"
              placeholder="Choose username"
              selection
              v-model="chosen"
          />
          <sui-button style="height: 37px; margin-left: 50px" content="Add as a friend" type="submit"/>
        </div>
      </sui-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddFriendComponent",
  data() {
    return {
      clicked: '',
      chosen: null,
      emailAdd: '',
      mobNum: '',
      usernames: [
        {key: 'arvin', text: 'Arvin', value: 'arvin'},
        {key: 'vahid', text: 'Vahid', value: 'vahid'},
        {key: 'surush', text: 'Soroush', value: 'surush'},],
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
      if (this.emailAdd === '') {
        if (this.mobNum === '') {
          alert("No group name entered.");
          return false;
        }
      }
    }
  },
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
</style>
