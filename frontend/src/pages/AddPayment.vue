<template>
  <div id="app">
    <adding-payment></adding-payment>
  </div>
</template>

<script>
import AddingPayment from "../components/AddingPayment";

export default {
  name: "AddPayment",
  components: {AddingPayment},
}
</script>

<style scoped>
#app {
  color: inherit;
  background: inherit;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-bottom: 20px;
  /*height: 100vw;*/
  /*display: grid;*/
  /*justify-content: center;*/
}

@font-face {
  font-family: "ESPN";
  src: url("https://a.espncdn.com/fonts/1.0.63/ESPNIcons/ESPNIcons.woff2") format('woff2');
}
</style>