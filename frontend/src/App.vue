<template>
  <div id="app">
    <router-view></router-view>
    <main-footer></main-footer>
    <!--    <login></login>-->
  </div>
</template>

<script>
// import SliderNav from "@/components/SliderNav";
import MainFooter from "@/components/MainFooter";
// import Login from "@/pages/Login";
// import router from './router/index'

export default {
  name: 'App',
  components: {MainFooter}
}
</script>

<style>
#app {
  background: black;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  border-radius: 6px;
}

@font-face {
  font-family: "ESPN";
  src: url("https://a.espncdn.com/fonts/1.0.63/ESPNIcons/ESPNIcons.woff2") format('woff2');
}
</style>
