<template>
  <div id="app">
    <pay-component></pay-component>
  </div>
</template>

<script>
import PayComponent from "../components/PayComponent";

export default {
  name: "Pay",
  components: {PayComponent}
}
</script>

<style scoped>
#app {
  color: inherit;
  background: inherit;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*margin-bottom: 20px;*/
  /*height: 100vw;*/
  /*display: grid;*/
  /*justify-content: center;*/
}

@font-face {
  font-family: "ESPN";
  src: url("https://a.espncdn.com/fonts/1.0.63/ESPNIcons/ESPNIcons.woff2") format('woff2');
}
</style>