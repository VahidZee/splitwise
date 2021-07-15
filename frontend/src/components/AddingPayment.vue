<template>
  <div id="adding-payment">
    <sui-form>
      <sui-form-field>
        <sui-header dividing>The group of the payment</sui-header>
        <sui-segment style="width: fit-content">
          <sui-checkbox toggle label="Choose a group" v-model="choosingGroup"/>
        </sui-segment>
        <sui-form-field v-if="choosingGroup">
          <sui-dropdown
              placeholder="Choose a group"
              search
              selection
              :options="groups"
              v-model="selectedGroup"
          />
        </sui-form-field>
        <sui-form-field v-else>
          <sui-dropdown
              placeholder="Choose friends"
              search
              selection
              multiple
              :options="friends"
              v-model="selectedGroup"
          />
        </sui-form-field>
      </sui-form-field>
      <sui-form-fields v-if="selectedGroup!=null" fields="two">
        <sui-form-field width="seven">
          <sui-header dividing style="width: fit-content;">Choose who paid</sui-header>
          <sui-segment style="width: fit-content">
            <sui-checkbox toggle label="Paid myself" v-model="myself"/>
          </sui-segment>
          <sui-form-field style="margin-bottom: 10px">
            <sui-dropdown
                :options="selectedGroup"
                placeholder="Choose who paid"
                selection
                :disabled="myself"
                v-model="payer"
            />
          </sui-form-field>
          <sui-form-field>
            <sui-header dividing>Specify the amount</sui-header>
            <sui-input placeholder="Amount" v-model="paidAmount" type="number"/>
          </sui-form-field>
          <sui-form-field>
            <sui-header dividing>Specify the location</sui-header>
            <sui-input placeholder="Location" icon="location arrow" type="text" v-model="location"/>
          </sui-form-field>
          <sui-form-field>
            <sui-header dividing>Short description</sui-header>
            <sui-input placeholder="Description" icon="clipboard outline" type="text" v-model="description"/>
          </sui-form-field>
          <sui-form-field>
            <sui-header dividing>Image</sui-header>
            <sui-input placeholder="Image" icon="image outline" type="file" v-model="description"/>
          </sui-form-field>
          <sui-button animated style="margin-top: 20px">
            <sui-button-content visible>Submit form</sui-button-content>
            <sui-button-content hidden>
              <sui-icon name="right arrow"/>
            </sui-button-content>
          </sui-button>
        </sui-form-field>
        <sui-form-field width="nine">
          <sui-header dividing>Share</sui-header>
          <sui-form-fields inline>
            <label>Share method:</label>
            <sui-form-field>
              <sui-checkbox radio v-model="share" label="Split equally" value="1"/>
            </sui-form-field>
            <sui-form-field>
              <sui-checkbox radio v-model="share" label="Amount" value="2"/>
            </sui-form-field>
            <sui-form-field>
              <sui-checkbox radio v-model="share" label="Percent" value="3"/>
            </sui-form-field>
          </sui-form-fields>
          <sui-form-field
              v-for="member in selectedGroup"
              v-bind:key="member"
              v-bind:title="member.text">
            <label>{{ member.text }}</label>
            <sui-input
                type="number"
                placeholder="Enter amount"
                v-model="member.share"
                :icon="shareIcon"
                :disabled="disableInput"
            />
          </sui-form-field>
          <sui-form-field>
            <label>{{ myDet.value }}</label>
            <sui-input
                type="number"
                placeholder="Enter amount"
                v-model="myDet.share"
                :disabled="disableInput"
                :icon="shareIcon"
            />
          </sui-form-field>
        </sui-form-field>
      </sui-form-fields>
    </sui-form>
  </div>
</template>

<script>
import {APIService} from "../APIService";

export default {
  name: "AddingPayment",
  data() {
    return {
      choosingGroup: true,
      myself: true,
      myDet: {key: 'me', value: 'Me', text: 'Me', share: null},
      share: "1",
      disableInput: true,
      shareIcon: "dollar",
      paidAmount: null,
      groups: null,
      friends: null,
      selectedGroup: null,
      location: null,
      description: null,
      paymentImage: null,
      payer: null,
    }
  },
  methods: {
    changeShareAuto: function (oval, nval) {
      if (this.selectedGroup) {
        var len = this.selectedGroup.length + 1
        var eachShare = this.paidAmount / len
        if (nval === "1" || (oval === "1" && nval === "2")) {
          for (let member of this.selectedGroup) {
            member.share = eachShare
          }
        } else if (oval === "1") {
          for (let member of this.selectedGroup) {
            member.share = 100 / len
          }
        } else if (nval === "2") {
          for (let member of this.selectedGroup) {
            member.share = member.share * this.paidAmount / 100
          }
        } else {
          for (let member of this.selectedGroup) {
            member.share = 100 * member.share / this.paidAmount
          }
        }
      }
    }
  },
  watch: {
    myself: function (val) {
      if (val) {
        this.payer = null
      }
    },
    share: function (nval, oval) {
      this.changeShareAuto(oval, nval)
      this.disableInput = nval === "1";
      if (nval === "3") {
        this.shareIcon = "percent"
      } else {
        this.shareIcon = "dollar"
      }
    },
    paidAmount: function (nval, oval) {
      let len = this.selectedGroup.length + 1
      if (this.share === "1") {
        for (let member of this.selectedGroup) {
          member.share = nval / len;
        }
      } else if (oval && oval > 3) {
        for (let member of this.selectedGroup) {
          member.share = member.share * nval / oval;
        }
      } else {
        for (let member of this.selectedGroup) {
          member.share = nval / len;
        }
      }
    },
    selectedGroup: {
      handler() {
        let sum = 0
        for (let member of this.selectedGroup) {
          member.share = Math.round(member.share)
          sum += member.share
        }
        let tot = ((this.share === "3") ? 100 : this.paidAmount)
        this.myDet.share = tot - sum
      },
      deep: true
    },
    choosingGroup: function () {
      this.selectedGroup = null
    }
  },
  mounted() {
    this.$http.get(APIService.FRIEND + '', {
      emulateJSON: true,
      headers: {'Authorization': 'Token ' + APIService.KEY}
    })
        .then(response => response.json())
        .then((data) => {
          this.friends = [];
          for (let friend of data) {
            this.friends.push({
              text: friend.username, key: friend.username, value: {text: friend.username, share: null}
            })
          }
        })
    this.$http.get(APIService.GROUP + '', {
      emulateJSON: true,
      headers: {'Authorization': 'Token ' + APIService.KEY}
    })
        .then(response => response.json())
        .then((data) => {
          this.groups = [];
          for (let group of data) {
            var membs = []
            for (let member of group.members) {
              membs.push({text: member.username, key: member.username, value: member.username, share: null})
            }
            this.groups.push({text: group.name, key: group.id, value: membs})
          }
        })
  }
}
</script>

<style scoped>
#adding-payment {
  position: relative;
  top: 15vh;
  left: 25vw;
  width: 50vw;
  height: fit-content;
  z-index: 1001;
  gap: 10px 10px;
  padding: 10px;
  margin: 40px;
  border: solid gray thin;
  border-radius: 5px;
  background-color: dimgray;
}
</style>