<template>
  <div class="home">
    <Test></Test>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import Test from '../components/Test/Test.vue';
@Component({components:{Test}})
export default class Dashboard extends Vue{

}
</script>
