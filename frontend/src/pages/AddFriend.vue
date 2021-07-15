<template>
  <div id="app">
    <slider-nav></slider-nav>
    <add-friend-component></add-friend-component>
  </div>
</template>

<script>
import SliderNav from "../components/SliderNav";
import AddFriendComponent from "@/components/AddFriendComponent";

export default {
  name: "AddFriend",
  components: {SliderNav, AddFriendComponent}
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
@font-face {
  font-family: "ESPN";
  src: url("https://a.espncdn.com/fonts/1.0.63/ESPNIcons/ESPNIcons.woff2") format('woff2');
}
</style>
