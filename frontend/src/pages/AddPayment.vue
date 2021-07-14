<template>
  <div id="app">
    <slider-nav></slider-nav>
    <adding-payment></adding-payment>
  </div>
</template>

<script>
import SliderNav from "../components/SliderNav";
import AddingPayment from "../components/AddingPayment";

export default {
  name: "AddPayment",
  components: {SliderNav, AddingPayment},
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