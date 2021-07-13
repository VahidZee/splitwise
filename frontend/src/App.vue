<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {},
}
</script>

<style>
#app {
  background: gray;
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
