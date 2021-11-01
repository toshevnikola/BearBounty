import Vue from 'vue'
import App from './App.vue'
import router from '../src/router'
import 'vuetify/dist/vuetify.min.css';
import Vuetify from 'vuetify';
import './plugins/vuetify';
import './plugins/vee-validate';
import GAuth from 'vue-google-oauth2'


const vuetify=new Vuetify({theme: {
    themes: {
      light: {
        primary: "#113C4A",
        secondary: "#f0943d",
        accent: "#3F7B70",
        error: "#FF5252",
        info: "#2196F3",
        success: "#4CAF50",
        warning: "#FFC107",
        lightblue: "#14c6FF",
        yellow: "#FFCF00",
        pink: "#FF1976",
        orange: "#FF8657",
        magenta: "#C33AFC",
        darkblue: "#1E2D56",
        gray: "#909090",
        neutralgray: "#9BA6C1",
        green: "#489258",
        red: "#ff3d3d",
        darkblueshade: "#308DC2",
        lightgray: "#BDBDBD",
        lightpink: "#FFCFE3",
        white: "#FFFFFF",
        marketchipstext:"#C5C5C5",
        marketchipsbg:"#1C5D73",
        dddddd:"#DDDDDD",
      }
    }
  }});

const gauthOption = {
  clientId: '148971071468-tq52cumdc82n6slf9tj0j3vu2fpgqj0s.apps.googleusercontent.com',
  scope: 'email',
  prompt: 'consent'
}
Vue.use(GAuth, gauthOption)
Vue.config.productionTip = false;
new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
