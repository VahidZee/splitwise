<template id="app">
  <div>
    <br/>
    <br/>
    <br/>
  <sui-table single-line collapsing id="inner">
    <sui-table-header>
      <sui-table-row>
        <sui-table-header-cell>Field</sui-table-header-cell>
        <sui-table-header-cell>Information</sui-table-header-cell>
      </sui-table-row>
    </sui-table-header>
    <sui-table-row>
      <sui-table-cell>Username:</sui-table-cell>
      <sui-table-cell>{{ user.username }}</sui-table-cell>
    </sui-table-row>
    <sui-table-row >
      <sui-table-cell>Name:</sui-table-cell>
      <sui-table-cell>{{ user.first_name + ' ' + user.last_name }}</sui-table-cell>
    </sui-table-row>
    <sui-table-row >
      <sui-table-cell>Email:</sui-table-cell>
      <sui-table-cell>{{ user.email }}</sui-table-cell>
    </sui-table-row>
    <sui-table-row >
      <sui-table-cell>Address:</sui-table-cell>
      <sui-table-cell>{{ user.address }}</sui-table-cell>
    </sui-table-row>
    <sui-table-row>
      <sui-table-cell>Phone:</sui-table-cell>
      <sui-table-cell>{{ user.phone }}</sui-table-cell>
    </sui-table-row>
  </sui-table>
    <br/>
    <br/>
    <br/>
    <br/>
    <br/>
    <div id="add-friend-component" v-if="this.input!=={}">
      <sui-form name="groupForm" style="width: 40vw;" >
        <sui-input placeholder="Username" icon="users" v-model="parsedInput.username" style="margin-bottom: 10px"/>
        <sui-input placeholder="First Name" icon="users" v-model="input.first_name" style="margin-bottom: 10px"/>
        <sui-input placeholder="Last Name" icon="users" v-model="input.last_name" style="margin-bottom: 10px"/>
        <sui-input placeholder="Email" icon="users" v-model="input.email" style="margin-bottom: 10px"/>
        <sui-input placeholder="Address" icon="users" v-model="input.address" style="margin-bottom: 10px"/>
        <div style="display: flex">
          <sui-input placeholder="Mobile Number" icon="users" v-model="input.phone" style="margin-bottom: 10px"/>

          <sui-button style="height: 37px; margin-left: 50px" content="Update Info" type="submit" v-on:click.prevent="send_info()"/>
        </div>
      </sui-form>
    </div>
  </div>
</template>

<script>
import {APIService} from "@/APIService";

export default {
  name: "UserInfo",
  props: [],
  data() {
    return {
      // user: {
      //   username: "admin",
      //   email: "sfch199999@gmail.com",
      //   first_name: "Soroush",
      //   last_name: "Farghadani",
      //   address: "kjdsnfajsdfojaijdsfoi",
      //   phone: null
      // },
      user: {},
      // userName:this.user.username,
      // fname: this.user.first_name,
      // lname: this.user.last_name,
      // email: this.user.email,
      // address: this.user.address,
      // mobNum: this.user.phone,
      input: {},
    }
  },
  computed:{
    parsedInput: function() {
      return this.input
    }
  },
  mounted() {
    this.get_info();
  },  methods: {
    send_info: function () {
      this.$http.put(APIService.UPDATEINFO, this.input,
          {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
          .catch(error => console.log(error))
    },
    get_info: function () {
      console.log(APIService.KEY)
      this.$http.get(APIService.UPDATEINFO,
          {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
          .then(response => response.json())
          .then((data) => {this.user=data
          this.input=JSON.parse(JSON.stringify(data))})
          .catch(error => console.log(error))
    },
  }
}
</script>

<style scoped>
#app {
  color: inherit;
  /*background: inherit;*/
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*height: 100vw;*/
  /*display: grid;*/
  /*justify-content: center;*/
}
#inner {
  width: 50%;
  margin: 0 auto;
}

@font-face {
  font-family: "ESPN";
  src: url("https://a.espncdn.com/fonts/1.0.63/ESPNIcons/ESPNIcons.woff2") format('woff2');
}
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
</style>
