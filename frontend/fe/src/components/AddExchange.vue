<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      max-width="70%"
      persistent
      @click:outside="close()"
    >
      <v-card>
        <v-card-text style="padding: 0">
          <v-container>
            <v-row>
              <v-col cols="8" id="leftSide">
                <v-col cols="10"><h1>Add Exchange</h1></v-col>
                <v-col cols="10"><span>Connect to New Exchange</span></v-col>
                <v-col cols="10">
                  <v-select
                    v-model="selectedAccount"
                    @input="changeAccount"
                    id="selection"
                    return-object
                    style="display: block; width: 70%"
                    :items="accounts"
                    item-text="exchange.name"
                    filled
                    label="Exchange"
                    persistent-hint
                  >
                  </v-select>
                </v-col>
                <v-col cols="10">
                  <h3>Api key</h3>
                </v-col>
                <v-col cols="10">
                  <input
                    v-model="email"
                    type="text"
                    autocomplete="off"
                    placeholder="Enter Api Key"
                  />
                </v-col>
                <v-col cols="10">
                  <h3>Secret key</h3>
                </v-col>
                <v-col cols="10">
                  <input
                    v-model="password"
                    type="password"
                    autocomplete="new-password"
                    placeholder="Enter Secret Key"
                  />
                </v-col>

                <v-col cols="10">
                  <a id="login" @click="close()">Add</a>
                </v-col>
              </v-col>
              <v-col cols="4" id="rightSide">
                <img style="max-width: 100%" src="../assets/bb_big.svg" />
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script lang="ts">
import { Component, Emit, Vue } from "vue-property-decorator";

@Component
export default class AddExchange extends Vue {
  public dialog: boolean = true;
  @Emit("isAddExchangeShown")
  public isExchangeShown(show: boolean): boolean {
    console.log("Emitting event");
    return show;
  }
  public close(): void {
    this.isExchangeShown(true);
  }
}
</script>


<style scoped>
h1 {
  color: #1c5d73;
}
input {
  font-size: 20px;
  font-family: Helvetica, Arial, sans-serif;
  color: #929292;
  font-weight: 700;
  background-color: #c4c4c4;
  width: 395px;
  height: 47px;
  padding-left: 20px;
}
input:focus {
  border: none;
}
#rightSide {
  background-color: #113c4a;
  vertical-align: middle;
  position: relative;
  padding: 0;
}
#rightSide > img {
  position: absolute; /* 2 */
  top: 0;
  bottom: 0;
  margin: auto;
}
#leftSide {
  background-color: #dddddd;
  padding-left: 5%;
  padding-top: 5%;
}
#login {
  width: 395px;
  font-size: 20px;
  display: block;
  background-color: #f0943d;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  float: left;
  text-align: center;
  padding: 25px 0;
  margin-top: 1%;
}
#loginGoogle {
  width: 395px;
  font-size: 20px;
  display: block;
  background-color: #2e6361;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  float: left;
  text-align: center;
  padding: 25px 0;
  margin-top: 1%;
  margin-bottom: 50px;
}
#or {
  width: 395px;
  text-align: center;
  font-size: 30px;
  color: #1c5d73;
  margin-top: 15%;
}
</style>