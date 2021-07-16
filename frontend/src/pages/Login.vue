<template>
  <div>
    <div class="header">
      <div class="title">Donger</div>
      <div>
        <button @click="toggleSignIn">Sign in</button>
        <button @click="toggleSignUp">Sign up</button>
      </div>
    </div>
    <div class="sign" v-show="signBox">
      <div v-show="signIn" style="vertical-align: center">
        <form style="float: right">
          <p>
            <label for="signInUsername">Username </label>
            <input type="text" id="signInUsername" name="username">
          </p>
          <p>
            <label for="signInPassword">Password </label>
            <input type="password" id="signInPassword" name="password">
          </p>
        </form>
        <br>
        <button style="float: right">Sign in</button>
      </div>
      <div v-show="signUp" style="vertical-align: center">
        <form style="float: right">
          <p>
            <label for="email">Email </label>
            <input type="text" id="email" name="email">
          </p>
          <p>
            <label for="username">Username </label>
            <input type="text" id="username" name="username">
          </p>
          <p>
            <label for="password">Password </label>
            <input type="password" id="password" name="password">
          </p>
          <p>
            <label for="repassword">Repeat Password </label>
            <input type="password" id="repassword" name="repassword">
          </p>
          <p>
            <label for="address">Address </label>
            <input type="text" id="address" name="address">
          </p>
        </form>
        <br>
        <button style="float: right;">Sign up</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      signIn: false,
      signUp: false,
    }
  },
  watch: {
    signIn: function (val) {
      if (val) {
        this.signUp = false
      }
    },
    signUp: function (val) {
      if (val) {
        this.signIn = false
      }
    }
  },
  methods: {
    toggleSignIn: function () {
      this.signIn = !this.signIn
    },
    toggleSignUp: function () {
      this.signUp = !this.signUp
    }
  },
  computed: {
    signBox: function () {
      return this.signIn || this.signUp
    }
  }
}
</script>

<style scoped>
.header {
  background-color: darkseagreen;
  border: none;
  border-radius: 6px;
  margin: 5px 0;
  padding: 10px 10px;
  display: flex;
  justify-content: space-between;
  vertical-align: center;
}

form {
  display: table;
  vertical-align: center;
}

p {
  display: table-row;
}

label {
  display: table-cell;
  text-align: right;
}

input {
  display: table-cell;
  margin: 3px;
  padding: 3px;
  border-radius: 4px;
  border: thin darkblue;
}

button {
  background-color: lightgray;
  color: black;
  border: none;
  border-radius: 4px;
  margin: 3px;
  padding: 10px 10px;
  font-size: 13px;
  vertical-align: center;
}

.title {
  color: darkgreen;
  font-size: 20px;
  margin: 10px 10px;
}

.sign {
  float: right;
  margin: 0 0;
  background-color: darkgray;
  border: thin darkgray;
  border-style: solid;
  border-radius: 8px;
  padding: 10px 10px;
}
</style>