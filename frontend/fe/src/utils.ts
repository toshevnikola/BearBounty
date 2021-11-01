import { UserExchange } from "./interfaces";

export const saveAuthToken = (token: string) => localStorage.setItem('authToken', token);
export const saveRefreshToken = (token: string) => localStorage.setItem('refreshToken', token);
export const removeTokens = () =>{
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken')
   };
   export const clearLocalStorage = () =>{
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('selectedAccountId')
   };

export const setSelectedAccountId=(accountId:string)=>localStorage.setItem('selectedAccountId',accountId);