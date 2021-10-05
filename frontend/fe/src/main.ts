import Vue from 'vue'
import App from './App.vue'
import router from '../src/router'
import Vuetify from 'vuetify'


Vue.use(Vuetify);
const vuetify = new Vuetify({
  theme:{ dark: false },
});

Vue.config.productionTip = false;
new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
