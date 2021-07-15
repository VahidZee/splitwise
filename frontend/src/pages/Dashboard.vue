<template>
  <div id="app">
    <!--    <full-header :post="mainNews" :match="liveMatch"></full-header>-->
    <!--    <payments v-on:change-count="onChangeCount" v-on:get-fav="getFavNews" :posts="posts" :favs="fav_posts" with-header="Latest News" with-buttons="true"></payments>-->
    <!--    <sui-grid class="container-fluid stackable padded">-->
    <slider-nav></slider-nav>
    <h1></h1>
    <h1></h1>
    <expenses :expens="this.expens" with-header="Dashboard"></expenses>
    <!--<sui-grid-row>-->
    <!--<sui-button @click="loadMoreNews" basic inverted color="red" circular class="m-auto" icon="ellipsis horizontal"></sui-button>-->
    <!--</sui-grid-row>-->
    <!--    </sui-grid>-->
    <!--    <latest-games></latest-games>-->
  </div>
</template>

<script>
import Expenses from "@/components/Expenses";
import SliderNav from "@/components/SliderNav";

export default {
  name: "Dashboard",
  components: {Expenses,SliderNav},
  data() {
    return {
      expens: [
        {
          id: 123,
          creator: "Soroush",
          cgroup: "Group1",
          val: 123,
          add_date: "12/02/1999",
          type: 'debt',
          members: ['Ahmad', 'Asghar', ' Akbar']
        },
        {
          id: 74,
          creator: "Soroush",
          cgroup: "Group1",
          val: 123,
          add_date: "12/02/1999",
          type: 'payment',
          members: ['Ahmad', 'Asghar', ' Akbar']
        },
        {
          id: 12,
          creator: "Soroush",
          cgroup: "Group1",
          val: 123,
          add_date: "12/02/1999",
          type: 'payment',
          members: ['Ahmad', 'Asghar', ' Akbar']
        },
        {
          id: 14,
          creator: "Soroush",
          cgroup: "Group1",
          val: 123,
          add_date: "12/02/1999",
          type: 'payment',
          members: ['Ahmad', 'Asghar', ' Akbar']
        }
      ]
    }
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

</style>
