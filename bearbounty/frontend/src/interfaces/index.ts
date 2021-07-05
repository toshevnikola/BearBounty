export interface IUserProfile {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: number;
}

export interface IUserProfileUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface IUserProfileCreate {
  email: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface IBot {
  id: number;
  name: string;
  description: string;
  strategy_id: number;
  created_at: string;
  updated_at: string;
  profit_24h: number;
  profit_all_time: number;
  is_running: boolean;
  account_id: number;
}
export interface IBotCreate {
  name: string;
  description: string;
  strategy_id: number;
  account_id: number;
}
export interface IBotUpdate {
  id: number;
  name: string;
  description: string;
  strategy_id: number;
  is_running: boolean;
  account_id: number;
}
export interface IStrategy {
  id: number;
  name: string;
  description: string;
}
export interface IAccount {
  id: number;
  name: string;
}
