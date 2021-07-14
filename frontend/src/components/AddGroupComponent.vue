<template>
  <div id="add-group-component">
    <sui-form name="groupForm" style="width: 40vw;" v-on:submit.prevent="validateForm()">
      <sui-input placeholder="Group name" icon="users" v-model="groupName" style="margin-bottom: 10px"/>
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
        <sui-button style="height: inherit" content="Create Group" type="submit"/>
      </div>
    </sui-form>
  </div>
</template>

<script>
export default {
  name: "AddGroupComponent",
  data() {
    return {
      friends: [
        {key: 'arvin', text: 'Arvin', value: 'arvin'},
        {key: 'vahid', text: 'Vahid', value: 'vahid'},
        {key: 'surush', text: 'Soroush', value: 'surush'},],
      chosen: null,
      clicked: '',
      groupName: '',
    };
  },
  methods: {
    validateForm() {
      if (this.groupName === '') {
        alert("No group name entered.");
        return false;
      }
      if (this.chosen == null) {
        alert("No friends were chosen.");
        return false;
      }
    }
  },
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