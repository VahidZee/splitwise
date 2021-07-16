<template>
  <div id="pay">
    <sui-form v-on:submit.prevent="settler">
      <sui-header dividing>Pay this expense to {{ creditor }}</sui-header>
      <sui-form-field>
        <label> Choose who to pay for </label>
        <sui-dropdown
            selection
            placeholder="Who to pay for"
            :options="debtors"
            v-model="settler"
        />
      </sui-form-field>
      <sui-form-field v-if="settler">
        <sui-header>Amount of debt is {{ settler.share }}$</sui-header>
        <sui-header>ID is {{ settler.id }}$</sui-header>
        <sui-button @click="submitForm"> Settle Debt</sui-button>
      </sui-form-field>
    </sui-form>
  </div>
</template>

<script>
import {APIService} from "../APIService";

export default {
  name: "PayComponent",
  data() {
    return {
      debtors: null,
      settler: null,
      creditor: null,
      payID: null,
    }
  },
  mounted() {
    this.payID = this.$route.params.id
    console.log(this.payID)
    this.$http.get(APIService.EXPENSE + this.payID+'/', {
      emulateJSON: true,
      headers: {'Authorization': 'Token ' + APIService.KEY}
    })
        .then(response => response.json())
        .then((data) => {
          this.creditor = data.payer;
          this.debtors = []
          for (let debtor of data.shares) {
            this.debtors.push({
              text: debtor.user,
              key: debtor.user,
              value: {text: debtor.user, share: debtor.share, id: debtor.id}
            })
          }
        }).catch(error => console.log(error))
  },
  methods: {
    submitForm: function () {
      console.log(this.settler)
      this.$http.post(APIService.EXPENSE + 'pay/' + this.settler.id, {}, {
        emulateJSON: true,
        headers: {'Authorization': 'Token ' + APIService.KEY}
      }).then(response => response.status).then((data) => {
        console.log(data);
        if (data === 202) {
          alert('Debt to ' + this.creditor + ' settled for ' + this.settler.text);
        } else {
          alert('Debt to ' + this.creditor + ' could not be settled for ' + this.settler.text);
        }
      }).catch(error => console.log(error))
    }
  }
}
</script>

<style scoped>
#pay {
  position: relative;
  top: 15vh;
  left: 30vw;
  width: 40vw;
  height: fit-content;
  z-index: 1001;
  gap: 10px 10px;
  padding: 10px;
  margin: 40px;
  border: solid gray thin;
  border-radius: 4px;
  background-color: dimgray;
}
</style>
