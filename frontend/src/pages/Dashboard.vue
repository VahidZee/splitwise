<template>
  <div id="Home">
    <full-header :post="mainNews" :match="liveMatch"></full-header>
    <latest-news v-on:change-count="onChangeCount" v-on:get-fav="getFavNews" :posts="posts" :favs="fav_posts" with-header="Latest News" with-buttons="true"></latest-news>
    <sui-grid class="container-fluid stackable padded">

      <!--<sui-grid-row>-->
      <!--<sui-button @click="loadMoreNews" basic inverted color="red" circular class="m-auto" icon="ellipsis horizontal"></sui-button>-->
      <!--</sui-grid-row>-->
    </sui-grid>
    <latest-games></latest-games>
  </div>
</template>

<script>
export default {
  name: "Dashboard"
}
</script>

<style scoped>

</style>
