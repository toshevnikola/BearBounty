/* eslint-disable @typescript-eslint/no-this-alias */
<template>
  <div>
    <v-navigation-drawer id="drawer" :mini-variant="miniDrawer" fixed>
      <div id="topNav">
        <div
          v-for="option in menuOptions"
          :key="option.name"
          class="iconWrapper"
          v-bind:class="{ activeIconWrapper: option.isActive }"
        >
          <v-tooltip bottom open-delay="300" color="#f0943d">
            <template v-slot:activator="{ on, attrs }">
              <v-icon
                v-bind:class="{ activeIcon: option.isActive }"
                large
                v-bind="attrs"
                v-on="on"
                @click="navigate(option)"
              >
                {{ option.icon }}
              </v-icon>
            </template>
            <span style="color: #113c4a; font-weight: bold">{{
              option.name
            }}</span>
          </v-tooltip>
        </div>
      </div>
      <div>
        <br />
        <br />
        <br />
        <div>_______</div>
        <br />
        <br />
        <br />
      </div>
      <div id="botNav">
        <div class="iconWrapper">
          <v-tooltip bottom open-delay="300" color="#f0943d">
            <template v-slot:activator="{ on, attrs }">
              <v-icon large v-bind="attrs" v-on="on"> mdi-account </v-icon>
            </template>
            <span style="color: #113c4a; font-weight: bold">Profile</span>
          </v-tooltip>
        </div>
        <div class="iconWrapper">
          <v-tooltip bottom open-delay="300" color="#f0943d">
            <template v-slot:activator="{ on, attrs }">
              <v-icon large v-bind="attrs" v-on="on"> mdi-cog </v-icon>
            </template>
            <span style="color: #113c4a; font-weight: bold">Settings</span>
          </v-tooltip>
        </div>
        <div class="iconWrapper">
          <v-tooltip bottom open-delay="300" color="#f0943d">
            <template v-slot:activator="{ on, attrs }">
              <v-icon large v-bind="attrs" v-on="on" @click="logout">
                mdi-exit-to-app
              </v-icon>
            </template>
            <span style="color: #113c4a; font-weight: bold">Logout</span>
          </v-tooltip>
        </div>
      </div>
    </v-navigation-drawer>
  </div>
</template>

<script lang="ts">
import router from "@/router";
import { Component, Vue } from "vue-property-decorator";
import { clearLocalStorage } from "../utils";

@Component
export default class Menu extends Vue {
  public showDrawer: boolean = true;
  public miniDrawer: boolean = true;
  public menuOptions: Array<any> = [
    {
      name: "Dashboard",
      isActive: false,
      icon: "mdi-monitor-dashboard",
      linkTo: "/dashboard",
    },
    {
      name: "Exchanges",
      isActive: false,
      icon: "mdi-swap-horizontal",
      linkTo: "/exchanges",
    },
    {
      name: "Charts",
      isActive: false,
      icon: "mdi-chart-bar",
      linkTo: "/charts",
    },
    {
      name: "Statistics",
      isActive: false,
      icon: "mdi-chart-areaspline-variant",
      linkTo: "/statistics",
    },
  ];
  mounted(): void {
    this.setActiveIcon(this.$router.currentRoute.path);
    // eslint-disable-next-line @typescript-eslint/no-this-alias
    var that = this;
    window.onpopstate = function () {
      console.log("setting to " + that.$router.currentRoute.path);
      that.setActiveIcon(that.$router.currentRoute.path);
    };
  }

  public logout(): any {
    clearLocalStorage();
    router.push("/");
  }
  public navigate(option: any): void {
    this.$router.push(option.linkTo);
    this.menuOptions.forEach((x) => {
      if (x.name === option.name) {
        x.isActive = true;
      } else {
        x.isActive = false;
      }
    });
  }
  public setActiveIcon(path: string): void {
    this.menuOptions.forEach((x) => {
      if (path == x.linkTo) {
        x.isActive = true;
      } else {
        x.isActive = false;
      }
    });
  }
}
</script>

<style scoped>
#drawer {
  background-color: #113c4a;
  color: white;
}
.iconWrapper {
  text-align: center;
  margin-top: 50%;
  cursor: pointer;
}

i,
button {
  color: #dddddd !important;
}
i:hover,
button:hover {
  color: #f0943d !important;
}
.activeIcon {
  color: #f0943d !important;
}
.activeIconWrapper {
  border-left: 4px solid #f0943d;
}
</style> 