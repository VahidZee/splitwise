<template>
  <div class="latest-news">
    <sui-grid v-if="withHeader" class="container-fluid padded head">
      <h2 is="sui-header" inverted>{{withHeader}}</h2>
      <div>
        <sui-dropdown
            text="Filter Expenses"
            icon="filter"
            floating
            labeled
            button
            class="icon grey basic small circular"
            v-model="filter"
            :options="options"
        ></sui-dropdown>
        <sui-dropdown
            placeholder="count"
            :options="exp_count_options"
            button
            labeled
            floating
            class="icon grey basic small circular"
            v-model="exp_counts"
        />
      </div>
    </sui-grid>

    <transition-group name="cell" class="ui grid container-fluid stackable padded">
      <expense
          v-for="exp in filteredExps()"
          :key="exp.id"
          :expense="exp"
          class="cell"
      ></expense>
<!--      <expense :key="12"></expense>-->
<!--      <expense :key="13"></expense>-->

    </transition-group>

  </div>
</template>


<script>
import Expense from "@/components/Expense";
import SuiDropdown from "semantic-ui-vue/dist/commonjs/modules/Dropdown/Dropdown";
import SuiHeader from "semantic-ui-vue/dist/commonjs/elements/Header/Header";

export default {
  name: "expenses",
  components: {SuiHeader, SuiDropdown, Expense},
  props: ['expens', 'withHeader'],
  data() {
    return {
      filter: 'All',
      exp_counts: 2,
      exp_count_options: [{
        text: '2',
        value: 2,
      }, {
        text: '5',
        value: 5,
      }, {
        text: '10',
        value: 10,
      }],
      options: [
        {
          key: 'All',
          text: 'All',
          value: 'All',
        },
        {
          key: 'Debt',
          text: 'Debt',
          value: 'Debt',
          label: {color: 'green', empty: true, circular: true},
        },
        {
          key: 'Payment',
          text: 'Payment',
          value: 'Payment',
          label: {color: 'orange', empty: true, circular: true},
        },
      ]
    }
  },
  watch: {
    exp_counts: function(val) {
      this.$emit('change-count', val)
    },
  },
  methods: {
    filterByType(exp) {
      return this.filter === 'All' || exp.type === this.filter.toLowerCase();
    },
    filteredExps: function () {
      // if (this.filter === 'All')
      //   return this.expens.slice(0, this.exp_count_options);
      // if (this.filter === 'All')
      let exps = this.expens.filter(this.filterByType);
        return exps.slice(0,this.exp_counts);
    }
  }
}
</script>

<style scoped>
.latest-news {
  padding-top: 1rem;
}

.head {
  justify-content: space-between;
  flex-wrap: wrap;
}
</style>
