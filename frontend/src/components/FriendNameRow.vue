<template>
  <sui-table-row>
    <sui-table-cell>{{ user.first_name+' '+user.last_name }}</sui-table-cell>
    <sui-table-cell>{{ user.username }}</sui-table-cell>
  </sui-table-row>
</template>

<script>
export default {
  name: "FriendNameRow",
  props:['user']
}
</script>

<style scoped>

</style>
