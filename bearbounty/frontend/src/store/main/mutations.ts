import { IBot, IBotCreate, IStrategy, IUserProfile } from '@/interfaces';
import { MainState, AppNotification } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
  setToken(state: MainState, payload: string) {
    state.token = payload;
  },
  setLoggedIn(state: MainState, payload: boolean) {
    state.isLoggedIn = payload;
  },
  setLogInError(state: MainState, payload: boolean) {
    state.logInError = payload;
  },
  setUserProfile(state: MainState, payload: IUserProfile) {
    state.userProfile = payload;
  },
  setDashboardMiniDrawer(state: MainState, payload: boolean) {
    state.dashboardMiniDrawer = payload;
  },
  setDashboardShowDrawer(state: MainState, payload: boolean) {
    state.dashboardShowDrawer = payload;
  },
  addNotification(state: MainState, payload: AppNotification) {
    state.notifications.push(payload);
  },
  removeNotification(state: MainState, payload: AppNotification) {
    state.notifications = state.notifications.filter(
      (notification) => notification !== payload,
    );
  },
  setBots(state: MainState, payload: IBot[]) {
    state.bots = payload;
  },
  deleteBot(state: MainState, payload: IBot) {
    state.bots = state.bots.filter(function(el) {
      return el.id !== payload.id;
    });
  },
  setStrategies(state: MainState, payload: IStrategy[]) {
    state.strategies = payload;
  },
  createBot(state: MainState, payload: IBot) {
    state.bots.push(payload);
  },
  updateBot(state: MainState, payload: IBot) {
    var foundIndex = state.bots.findIndex((x) => x.id == payload.id);
    console.log(foundIndex);
    console.log(state.bots[foundIndex]);
    console.log(payload);
    state.bots[foundIndex] = payload;
  },
};

const { commit } = getStoreAccessors<MainState | any, State>('');

export const commitSetDashboardMiniDrawer = commit(
  mutations.setDashboardMiniDrawer,
);
export const commitSetDashboardShowDrawer = commit(
  mutations.setDashboardShowDrawer,
);
export const commitSetLoggedIn = commit(mutations.setLoggedIn);
export const commitSetLogInError = commit(mutations.setLogInError);
export const commitSetToken = commit(mutations.setToken);
export const commitSetUserProfile = commit(mutations.setUserProfile);
export const commitAddNotification = commit(mutations.addNotification);
export const commitRemoveNotification = commit(mutations.removeNotification);
export const commitGetBots = commit(mutations.setBots);
export const commitDeleteBot = commit(mutations.deleteBot);
export const commitGetStrategies = commit(mutations.setStrategies);
export const commitCreateBot = commit(mutations.createBot);
export const commitUpdateBot = commit(mutations.updateBot);
