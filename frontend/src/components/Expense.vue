<template>
    <!--<sui-grid-column :width="post.type === 'small' ? 4 : 8" class="news-card" :class="{big: post.type === 'big'}">-->
    <sui-grid-column :width=8 class="news-card">
    <!--<sui-grid-column width='4' class="news-card">-->
        <div class="post">
            <div class="post-cat">
                <sui-label
                        circular
                        :color="color"
                        empty
                ></sui-label>
                {{expense.creator.toUpperCase()}}
                <sui-icon name="calendar" class="inverted"></sui-icon>{{expense.add_date}}
            </div>
          <p>

          </p>
          <router-link :to='"/expense/" + expense.id'><span>Group: </span><span class="post-title">{{expense.cgroup}}</span></router-link>
          <router-link :to='"/expense/" + expense.id'><span>Members: </span>
              <span v-for="member in expense.members"
                                                            :key="member"
                                                            class="post-title">{{member}}</span></router-link>
            <router-link :to='"/expense/" + expense.id'><span>Amount: </span>
              <span class="post-title">{{expense.val}}$</span></router-link>
          <p>

          </p>
            <!--<router-link :to='"/news/" + post.id'><h3 class="post-title" ><sui-icon name="play" v-if="post.media === 'video'"></sui-icon>{{post.title}}</h3></router-link>-->
            <router-link :to='"/expense/" + expense.id'><sui-button circular size="mini" color="blue" basic>Pay</sui-button></router-link>
        </div>
    </sui-grid-column>
</template>

<script>
    export default {
        name: "Expense",
        props: ["expense"],
        // data(){
        //   return {
        //     expense: {
        //       id: 123,
        //       creator: "Soroush",
        //       cgroup: "Group1",
        //       val: 123,
        //       add_date: "12/02/1999",
        //       type: 'debt',
        //       members: ['Ahmad', 'Asghar', ' Akbar']
        //     }
        //   }
        // },
        computed: {
            color: function () {
                return this.expense.type ===  'debt' ? 'green' : 'orange';
            }
        }
    }
</script>

<style scoped>
    .news-card {
        position: relative;
        overflow: hidden;
        display: flex !important;
        flex-direction: column;
        align-items: stretch;
    }
    .news-card.big .post {
        position: absolute;
        bottom: 1rem;
    }
    .post {
        background: linear-gradient(to left, #000, rgba(255, 255, 255, .1));
        padding: 0.75rem;
        width: 100%;
        border-radius: 0 0 15px 15px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: baseline;
    }
    .news-card.big .post {
        background: linear-gradient(rgba(0, 0, 0, 0), #000);
    }
    .post-cat {
        color: rgba(255, 255, 255, 0.5);
    }
    .post-title {
        color: white;
        margin: 0.5rem 0 1.5rem 0;
        font-size: medium;
    }
</style>

# Coded by Soroush Farghadani - Documents are available in the GIT!
