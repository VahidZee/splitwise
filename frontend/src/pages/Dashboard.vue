<template>
  <div id="app">
    <!--    <full-header :post="mainNews" :match="liveMatch"></full-header>-->
    <!--    <payments v-on:change-count="onChangeCount" v-on:get-fav="getFavNews" :posts="posts" :favs="fav_posts" with-header="Latest News" with-buttons="true"></payments>-->
    <!--    <sui-grid class="container-fluid stackable padded">-->
    <h1></h1>
    <h1></h1>
    <expenses :expens="this.expens" with-header="My Expenses"></expenses>
    <div class="post-title">Friend's debts:</div>
    <expenses v-for="exps in this.parsedExp" :key="exps.user" :expens="exps" :with-header="exps.user"></expenses>
    <!--<sui-grid-row>-->
    <!--<sui-button @click="loadMoreNews" basic inverted color="red" circular class="m-auto" icon="ellipsis horizontal"></sui-button>-->
    <!--</sui-grid-row>-->
    <!--    </sui-grid>-->
    <!--    <latest-games></latest-games>-->
  </div>
</template>

<script>
import Expenses from "@/components/Expenses";
import {APIService} from "@/APIService";

export default {
  name: "Dashboard",
  components: {Expenses},
  computed: {
    parsedExp: function () {
      return this.exp_friends
    },
    parsedFri: function () {
      return this.friends
    },
  },
  methods: {
    get_payments: function () {
      this.$http.get(APIService.Expense,
          {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
          .then(response => response.json())
          .then((data) => {
            this.expens = data
            this.expens['user']=this.curr_username
          })
          .catch(error => console.log(error))
    },
    get_friends: function () {
      console.log("here")
      this.$http.get(APIService.FRIEND,
          {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
          .then(response => response.json())
          .then((data) => {
            this.friends = data
            console.log(data)
            console.log(this.friends)
            this.get_debts(data)
          })
          .catch(error => console.log(error))

    },
    get_debts: function (arg) {
      console.log(arg)

      for (let friend of arg) {
        this.$http.get(APIService.Debt + friend.username,
            {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
            .then(response => response.json())
            .then((data) => {
              data["user"] = friend.username;
              this.exp_friends.push(data);
            })
            .catch(error => console.log(error))
      }
    },
    get_me: function () {
      console.log(APIService.KEY)
      this.$http.get(APIService.UPDATEINFO,
          {emulateJSON: true, headers: {'Authorization': 'Token ' + APIService.KEY}})
          .then(response => response.json())
          .then((data) => {
            this.curr_username = data.username
          })
          .catch(error => console.log(error))
    },
  }
  ,
  data() {
    return {
      expens: [],
      friends: [],
      exp_friends: [],
      curr_username:''
    }
  }
  ,
  mounted() {
    this.get_me()
    this.get_payments()
    this.get_friends()
  }
}
</script>

<style scoped>
#app {
  background: black;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  border-radius: 6px;
}

.post-title {
  color: red;
//width: 70%; margin: 0 auto; font-size: x-large;
}
</style>
