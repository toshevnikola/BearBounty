import axios from 'axios';
import { apiUrl, apiVersion } from '@/env';
import {UserExchange, Bot} from './interfaces';
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
        return axios.post(`${apiUrl}/${apiVersion}/login/get-tokens`, payload);
    },
    async getUserExchanges(token:string):Promise<any> {
        return axios.get<UserExchange[]>(`${apiUrl}/${apiVersion}/user_exchanges`, authHeaders(token))
    },
    async getBots(token:string):Promise<any>{
        return axios.get<Bot[]>(`${apiUrl}/${apiVersion}/bots`, authHeaders(token));
    },
    async getBotsByUserExchange(token:string, userExchangeId:number):Promise<any>{
        return axios.get<Bot[]>(`${apiUrl}/${apiVersion}/bots/${userExchangeId}`, authHeaders(token));
    }

}