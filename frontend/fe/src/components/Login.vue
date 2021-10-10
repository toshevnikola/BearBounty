<template>
  <v-row justify="center">
    <v-dialog
      v-model="isShown"
      persistent
      max-width="70%"
      @click:outside="save()"
      style="padding: 0"
    >
      <v-card>
        <v-card-text style="padding: 0">
          <v-container>
            <v-row>
              <v-col cols="8" id="leftSide">
                <v-col cols="10"><h1>Log In</h1></v-col>
                <v-col cols="10"
                  ><input
                    v-model="email"
                    type="text"
                    autocomplete="off"
                    placeholder="Email"
                  />
                </v-col>
                <v-col cols="10"
                  ><input
                    v-model="password"
                    type="password"
                    autocomplete="new-password"
                    placeholder="Password"
                  />
                </v-col>

                <v-col cols="10">
                  <a id="login" @click="login()">Log In</a>
                </v-col>
                <v-col cols="10">
                  <div id="or">-or-</div>
                </v-col>
                <v-col cols="10">
                  <a id="loginGoogle" @click="save()"
                    ><img
                      style="position: relative; top: 5px"
                      src="../assets/google_small.png"
                    />
                    Log in with Google</a
                  >
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
import { Component, Vue, Emit } from "vue-property-decorator";
import { api } from "../api";
import { saveAuthToken, saveRefreshToken } from "../utils";
import router from "@/router";

@Component
export default class Login extends Vue {
  public isShown: boolean = true;
  private email: string = "";
  private password: string = "";
  @Emit("isLoginShown")
  public isLoginShown(show: boolean): boolean {
    return show;
  }
  public save(): void {
    this.isLoginShown(true);
  }
  public async login(): Promise<void> {
    this.isLoginShown(true);
    let response = await api.login(this.email, this.password);
    const authToken = response.data.access_token;
    const refreshToken = response.data.refresh_token;
    if (authToken && refreshToken) {
      saveAuthToken(authToken);
      saveRefreshToken(refreshToken);
      if (router.currentRoute.path === "/") {
        router.push("/dashboard");
      }
    }
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