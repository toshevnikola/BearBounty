import axios from 'axios';
import { apiUrl, apiVersion } from '@/env';
import {UserExchange, Bot, BotEdit, Deal, Exchange, BotCreate,CoinMarketCapResponse} from './interfaces';
function authHeaders(token: string) {
    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  }
export const api = {
    async login(email:string, password:string):Promise<any>{
        const payload = {"email":email, "password":password}
        return axios.post(`${apiUrl}/${apiVersion}/login/get-tokens/`, payload);
    },
    async getUserExchanges(token:string):Promise<any> {
        return axios.get<UserExchange[]>(`${apiUrl}/${apiVersion}/user_exchanges/`, authHeaders(token))
    },
    async getBots(token:string):Promise<any>{
        return axios.get<Bot[]>(`${apiUrl}/${apiVersion}/bots/`, authHeaders(token));
    },
    async getBotsByUserExchange(token:string, userExchangeId:number):Promise<any>{
        return axios.get<Bot[]>(`${apiUrl}/${apiVersion}/bots/${userExchangeId}`, authHeaders(token));
    },
    async updateBot(token:string, payload:BotEdit):Promise<any>{
      return axios.patch(`${apiUrl}/${apiVersion}/bots/${payload.id}/`,payload ,authHeaders(token))
    },
    async deleteBot(token:string, botId:number):Promise<any>{
      return axios.delete(`${apiUrl}/${apiVersion}/bots/${botId}`, authHeaders(token));
    },
    async createBot(token:string, payload:BotCreate):Promise<any>{
      return axios.post(`${apiUrl}/${apiVersion}/bots/`,payload, authHeaders(token));
    },
    async getDealsByExchange(token:string,exchangeId:number):Promise<any>{
      return axios.get<Deal[]>(`${apiUrl}/${apiVersion}/deals/user_exchange/${exchangeId}/`, authHeaders(token));
    },
    async getExchanges():Promise<any>{
      return axios.get<Exchange[]>(`${apiUrl}/${apiVersion}/exchanges/`);
    },
    async addUserExchange(token:string, exchangeId:number, apiKey:string, secretKey:string):Promise<any>{
      const payload = {'exchange_id':exchangeId, 'api_key':apiKey, 'api_secret':secretKey};
      console.log(payload);
      return axios.post(`${apiUrl}/${apiVersion}/user_exchanges/`, payload, authHeaders(token))
    },
    async refreshAssets(token:string, userExchangeId:number){
      return axios.get<UserExchange>(`${apiUrl}/${apiVersion}/user_exchanges/${userExchangeId}/?refresh=true`, authHeaders(token));
    },
    async getCurrencies(token:string, exchangeId:string):Promise<any>{
      return axios.get<CoinMarketCapResponse>(`${apiUrl}/${apiVersion}/cryptocurrencies/?exchange_id=${exchangeId}`, authHeaders(token));
    },
    async googleLogin(token:string):Promise<any>{
      const payload={"token":token}
      return axios.post(`${apiUrl}/${apiVersion}/login/google-login/`, payload);
    }
    

}