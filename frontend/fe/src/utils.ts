export const saveAuthToken = (token: string) => localStorage.setItem('authToken', token);
export const saveRefreshToken = (token: string) => localStorage.setItem('refreshToken', token);
export const removeTokens = () =>{
                                  localStorage.removeItem('authToken');
                                  localStorage.removeItem('refreshToken')
                                 };