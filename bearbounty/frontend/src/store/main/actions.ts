import { api } from '@/api';
import { IAccount, IBot, IBotCreate, IBotUpdate } from '@/interfaces';
import router from '@/router';
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import {
  commitAddNotification,
  commitRemoveNotification,
  commitSetLoggedIn,
  commitSetLogInError,
  commitSetToken,
  commitSetUserProfile,
  commitGetBots,
  commitDeleteBot,
  commitGetStrategies,
  commitCreateBot,
  commitUpdateBot,
  commitGetAccounts,
  commitSetCurrentAccount,
} from './mutations';
import { AppNotification, MainState } from './state';

type MainContext = ActionContext<MainState, State>;

export const actions = {
  async actionLogIn(
    context: MainContext,
    payload: { username: string; password: string },
  ) {
    try {
      const response = await api.logInGetToken(
        payload.username,
        payload.password,
      );
      const token = response.data.access_token;
      if (token) {
        saveLocalToken(token);
        commitSetToken(context, token);
        commitSetLoggedIn(context, true);
        commitSetLogInError(context, false);
        await dispatchGetUserProfile(context);
        await dispatchRouteLoggedIn(context);
        commitAddNotification(context, {
          content: 'Logged in',
          color: 'success',
        });
      } else {
        await dispatchLogOut(context);
      }
    } catch (err) {
      commitSetLogInError(context, true);
      await dispatchLogOut(context);
    }
  },
  async actionGetUserProfile(context: MainContext) {
    try {
      const response = await api.getMe(context.state.token);
      if (response.data) {
        commitSetUserProfile(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateUserProfile(context: MainContext, payload) {
    try {
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateMe(context.state.token, payload),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(undefined), 500),
          ),
        ])
      )[0];
      commitSetUserProfile(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Profile successfully updated',
        color: 'success',
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCheckLoggedIn(context: MainContext) {
    if (!context.state.isLoggedIn) {
      let token = context.state.token;
      if (!token) {
        const localToken = getLocalToken();
        if (localToken) {
          commitSetToken(context, localToken);
          token = localToken;
        }
      }
      if (token) {
        try {
          const response = await api.getMe(token);
          commitSetLoggedIn(context, true);
          commitSetUserProfile(context, response.data);
        } catch (error) {
          await dispatchRemoveLogIn(context);
        }
      } else {
        await dispatchRemoveLogIn(context);
      }
    }
  },
  async actionRemoveLogIn(context: MainContext) {
    removeLocalToken();
    commitSetToken(context, '');
    commitSetLoggedIn(context, false);
  },
  async actionLogOut(context: MainContext) {
    await dispatchRemoveLogIn(context);
    await dispatchRouteLogOut(context);
  },
  async actionUserLogOut(context: MainContext) {
    await dispatchLogOut(context);
    commitAddNotification(context, { content: 'Logged out', color: 'success' });
  },
  actionRouteLogOut(context: MainContext) {
    if (router.currentRoute.path !== '/login') {
      router.push('/login');
    }
  },
  async actionCheckApiError(context: MainContext, payload: AxiosError) {
    if (payload.response!.status === 401) {
      await dispatchLogOut(context);
    }
  },
  actionRouteLoggedIn(context: MainContext) {
    if (
      router.currentRoute.path === '/login' ||
      router.currentRoute.path === '/'
    ) {
      router.push('/main');
    }
  },
  async removeNotification(
    context: MainContext,
    payload: { notification: AppNotification; timeout: number },
  ) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commitRemoveNotification(context, payload.notification);
        resolve(true);
      }, payload.timeout);
    });
  },
  async passwordRecovery(context: MainContext, payload: { username: string }) {
    const loadingNotification = {
      content: 'Sending password recovery email',
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.passwordRecovery(payload.username),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(undefined), 500),
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Password recovery email sent',
        color: 'success',
      });
      await dispatchLogOut(context);
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Incorrect username',
      });
    }
  },
  async resetPassword(
    context: MainContext,
    payload: { password: string; token: string },
  ) {
    const loadingNotification = {
      content: 'Resetting password',
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.resetPassword(payload.password, payload.token),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(undefined), 500),
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Password successfully reset',
        color: 'success',
      });
      await dispatchLogOut(context);
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Error resetting password',
      });
    }
  },

  async actionGetBots(context: MainContext) {
    try {
      const response = await api.getBots(context.state.token);
      if (response.data) {
        commitGetBots(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },

  async actionDeleteBot(context: MainContext, payload: { id: number }) {
    try {
      const response = await api.deleteBot(payload.id, context.state.token);
      if (response.data) {
        commitDeleteBot(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },

  async actionGetStrategies(context: MainContext) {
    try {
      const response = await api.getStrategies(context.state.token);
      if (response.data) {
        commitGetStrategies(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateBot(context: MainContext, payload: IBotCreate) {
    try {
      const response = await api.createBot(context.state.token, payload);
      if (response.data) {
        commitCreateBot(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateBot(context: MainContext, payload: IBotUpdate) {
    try {
      const response = await api.updateBot(context.state.token, payload);
      if (response.data) {
        commitUpdateBot(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetAccounts(context: MainContext) {
    try {
      const response = await api.getAccounts(context.state.token);
      if (response.data) {
        commitGetAccounts(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionSetCurrentAccount(context: MainContext, payload: IAccount) {
    console.log('in action:', payload);
    commitSetCurrentAccount(context, payload);
  },
};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetUserProfile = dispatch(actions.actionGetUserProfile);
export const dispatchLogIn = dispatch(actions.actionLogIn);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchUpdateUserProfile = dispatch(
  actions.actionUpdateUserProfile,
);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchPasswordRecovery = dispatch(actions.passwordRecovery);
export const dispatchResetPassword = dispatch(actions.resetPassword);
export const dispatchGetAccounts = dispatch(actions.actionGetAccounts);
export const dispatchGetStrategies = dispatch(actions.actionGetStrategies);
export const dispatchGetBots = dispatch(actions.actionGetBots);
export const dispatchCreateBot = dispatch(actions.actionCreateBot);
export const dispatchDeleteBot = dispatch(actions.actionDeleteBot);
export const dispatchUpdateBot = dispatch(actions.actionUpdateBot);
export const dispatchSetCurrentAccount = dispatch(
  actions.actionSetCurrentAccount,
);
