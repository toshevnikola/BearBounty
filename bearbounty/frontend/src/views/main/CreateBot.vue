<template>
  <v-container>
    <v-form>
      <v-row justify="space-between">
        <v-form ref="form" lazy-validation v-model="valid">
          <v-col cols="12" md="4">
            <v-text-field
              v-model="botName"
              counter
              maxlength="15"
              label="Bot name"
              :rules="nameRules"
              v-validate="{ required: true }"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-textarea
              rows="2"
              name="input-7-4"
              label="Bot description"
              v-model="botDescription"
            ></v-textarea>
          </v-col>
          <v-col>
            <v-label>Strategy</v-label>
            <v-select
              v-model="selectedStrategy"
              :items="strategies"
              item-text="name"
              item-value="id"
              label="Strategy"
              persistent-hint
              return-object
              single-line
            ></v-select>
          </v-col>

          <v-btn
            color="primary"
            class="mr-4"
            @click="submit"
            :disabled="!valid"
          >
            Create
          </v-btn>
        </v-form>
      </v-row>
    </v-form>
  </v-container>
</template>
<script lang="ts">
import { IBot, IBotCreate, IStrategy } from '@/interfaces';
import { Component, Vue } from 'vue-property-decorator';
import { readStrategies } from '@/store/main/getters';
import { dispatchGetStrategies, dispatchCreateBot } from '@/store/main/actions';
@Component
export default class CreateBot extends Vue {
  public strategies: IStrategy[] = [];
  public selectedStrategy?: IStrategy = undefined;
  public valid = false;
  nameRules = [
    (v) => !!v || 'Name is required',
    (v) =>
      (v.length >= 5 && v.length <= 15) ||
      'Name must be between 5 and 15 characters',
  ];

  public botName: string = '';
  public botDescription: string = '';
  private getStrategies() {
    return readStrategies(this.$store);
  }
  private async mounted() {
    await dispatchGetStrategies(this.$store);
    this.strategies = this.getStrategies();
    this.selectedStrategy = this.strategies[0];
  }

  private async submit() {
    if (await this.$validator.validateAll()) {
      const newBot: IBotCreate = {
        name: this.botName,
        description: this.botDescription,
        strategy_id: this.selectedStrategy!.id,
      };
      if (newBot.description === '') {
        newBot.description = newBot.name;
      }
      await dispatchCreateBot(this.$store, newBot);
      this.$router.push('/main/home');
    }
  }
}
</script>
