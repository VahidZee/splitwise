<template>
  <div id="slider-nav" v-scroll="scrolling">
    <div class="dimmer" v-if="isOpen" @click.prevent="isOpen = ! isOpen"></div>
    <div class="wrapper">
      <sui-container>
        <sui-header class="logo large" inverted>DONGER</sui-header>
        <sui-button @click="isOpen = !isOpen" icon="bars" floated="left" color="red" basic inverted
                    circular></sui-button>
        <sui-button @click="goBack" icon="arrow left" floated="left" color="red" basic inverted
                    circular></sui-button>
        <sui-button @click.native="toggle" icon="user" floated="right" basic inverted circular><span
            v-if="isLoggedIn()">sign out</span></sui-button>
        <!--        <sui-button icon="search" floated="right" basic inverted circular @click="toggleSearch">-->
        <!--          <sui-input v-if="isSearch" v-model="search" class="transparent inverted search-input"-->
        <!--                     @click.stop=""></sui-input>-->
        <!--        </sui-button>-->
      </sui-container>
    </div>
    <div class="ui wide sidebar inverted vertical menu" :class="{visible: isOpen}" style="border: none">
      <div is="sui-segment" class="nav-menu">
        <sui-accordion exclusive inverted transparent>
          <router-link v-for="item in links" :key="item.id" :to="item.link">
            <sui-list-item>{{ item.name }}</sui-list-item>
          </router-link>
        </sui-accordion>
      </div>
    </div>

    <div>
      <sui-modal v-model="open">
        <sui-modal-header>
          <sui-button-group size="large" :widths="2">
            <sui-button @click.native="changeFormType('login')" content="Login"
                        :active="form_type === 'login'"/>
            <sui-button-or/>
            <sui-button @click.native="changeFormType('signup')" content="Signup"
                        :active="form_type === 'signup'"/>
          </sui-button-group>
        </sui-modal-header>
        <login v-if="form_type === 'login'" nav="this"></login>
        <signup v-if="form_type === 'signup'"></signup>
      </sui-modal>
    </div>
  </div>
</template>

<script>
import Login from "@/components/Login";
import Signup from "@/components/Signup";
import {APIService} from "@/APIService";

export default {
  name: "SliderNav",
  components: {Signup, Login},
  data() {
    return {
      open: false,
      form_type: 'login',
      alpha: 0,
      isOpen: false,
      isSearch: false,
      search: '',
      links: [
        {id: 3, name: 'Dashboard', link: '/dash'},
        {id: 4, name: 'Add Group', link: '/add_group'},
        {id: 5, name: 'Add Expense', link: '/add_payment'},
        {id: 6, name: 'Add Friend', link: '/add_friend'},
        {id: 7, name: 'User Info', link: '/user_info'},
      ]
    }
  },
  methods: {
    goBack() {
      window.history.length > 1
          ? this.$router.go(-1)
          : this.$router.push('/')
    },
    scrolling: function () {
      this.alpha = window.scrollY / 500;
      if (this.alpha > 1) this.alpha = 1;
    },
    toggleSearch: function () {
      this.isSearch = !this.isSearch;
      this.search.el.focus();
    },
    toggle() {
      if (!this.isLoggedIn())
        this.open = !this.open;
      else {
        this.signOut();
      }
    },
    changeFormType(value) {
      this.form_type = value;
    },
    signOut() {
      this.$http.post(APIService.AUTH + 'logout/', '', {
        emulateJSON: true,
        headers: {'Authorization': 'Token ' + APIService.KEY}
      })
          .then(response => response.status)
          .then((data) => {
            // APIService.KEY = data.token;
            console.log(data)
          })
          // .then(this.logged())
          .catch(error => console.log(error))
      APIService.loggedIn = false;
      APIService.KEY = 'unknown';
    },
    isLoggedIn: function () {
      // this.logged();
      return APIService.loggedIn;
    },
    logged() {
      this.$http.post(APIService.USER + 'logged/', {key: APIService.KEY}, {emulateJSON: true})
          .then(response => response.json())
          .then((data) => APIService.loggedIn = data)
          .catch(error => console.log(error))
    }
  },
  computed: {
    opacity: function () {
      return "background: rgba(127,127,127," + 1 + ");"
    },
    showP: function () {
      return this.open && !this.isLoggedIn()
    }
  },
  mounted() {
    // this.logged()
  },
}
</script>

<style scoped>
#slider-nav {
  position: fixed;
  padding: .75rem 0;
  z-index: 1000;
  /*background-color: #42b983;*/
}

#slider-nav .wrapper {
  width: 100vw;
}

.search-input {
  margin: -0.5rem 0;
}

.logo {
  display: inline-block;
  text-align: center;
  margin: 0 auto !important;
  line-height: 40px;
  height: 40px;
}

.black {
  background: rgba(0, 0, 0, 0.75);
}

.wrapper {
  text-align: center;
}

.ui.wide.sidebar {
  width: 250px;
  background: linear-gradient(to right, rgb(0, 0, 0), rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0));
}

.nav-menu {
  background: none !important;
  border: none;
}

.dimmer {
  background: rgba(0, 0, 0, 0.1);
  z-index: auto;
  width: 100vw;
  height: 100%;
  position: fixed;
  margin-top: -.75rem;
}
</style>
