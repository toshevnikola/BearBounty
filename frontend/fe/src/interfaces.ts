export interface Exchange{
    id:number,
    name:string,
    supported_pairs:Array<string>,
    is_available:boolean,
}
export interface UserExchange{
    id:number,
    user_id:number,
    is_valid:boolean,
    exchange:Exchange,
    currency:string,
    balance:number
    assets:Array<any>
}
export interface Bot{
    name?:string,
    description:string,
    trading_pairs?:Array<string>,
    base_coin?:string,
    base_order_amount?:number,
    safety_order_amount?:number,
    max_safety_orders?:number,
    max_active_safety_orders?:number,
    safety_order_price_deviation_pct?:number,
    safety_order_price_deviation_scale?:number,
    allocated_funds?:number,
    consider_overall_sentiment?:number,
    stop_loss_pct?:number,
    take_profit_pct?:number,
    is_running?:boolean,
    in_deal?:boolean,
    id:number,
    user_exchange_id:number,
    avatar_color?:string
}
export interface BotEdit{
    name?:string,
    description?:string,
    trading_pairs?:Array<string>,
    base_coin?:string,
    base_order_amount?:number,
    safety_order_amount?:number,
    max_safety_orders?:number,
    max_active_safety_orders?:number,
    safety_order_price_deviation_pct?:number,
    safety_order_price_deviation_scale?:number,
    allocated_funds?:number,
    consider_overall_sentiment?:number,
    stop_loss_pct?:number,
    take_profit_pct?:number,
    is_running?:boolean,
    in_deal?:boolean,
    id?:number,
    user_exchange_id?:number,
    avatar_color?:string
}
export interface BotCreate{
    name:string,
    description:string,
    trading_pairs:Array<string>,
    base_coin:string,
    base_order_amount:number,
    safety_order_amount:number,
    max_safety_orders:number,
    max_active_safety_orders:number,
    safety_order_price_deviation_pct:number,
    safety_order_price_deviation_scale:number,
    allocated_funds:number,
    consider_overall_sentiment:boolean,
    stop_loss_pct:number,
    take_profit_pct:number,
    is_running:boolean,
    in_deal:boolean,
    user_exchange_id:number,
    avatar_color:string,
}
export interface Order{
    deal_id:number,
    fee:number,
    id:number,
    type:number,
    created_at:string,
    updated_at:string
    price:number,
    amount:number,
    status:number,
    exchange_order_id:number,
}
export interface Deal {
    bot_id:number,
    pair:string,
    is_active:boolean,
    created_at:string,
    updated_at:string,
    bot:Bot
    orders:Array<Order>
}
// for coinmarketcap reponse
export interface Status {
    timestamp: Date;
    error_code: number;
    error_message?: any;
    elapsed: number;
    credit_count: number;
    notice?: any;
    total_count: number;
}

export interface Platform {
    id: number;
    name: string;
    symbol: string;
    slug: string;
    token_address: string;
}

export interface USD {
    price: number;
    volume_24h: number;
    volume_change_24h: number;
    percent_change_1h: number;
    percent_change_24h: number;
    percent_change_7d: number;
    percent_change_30d: number;
    percent_change_60d: number;
    percent_change_90d: number;
    market_cap: number;
    market_cap_dominance: number;
    fully_diluted_market_cap: number;
    last_updated: Date;
}

export interface Quote {
    USD: USD;
}

export interface Datum {
    id: number;
    name: string;
    symbol: string;
    slug: string;
    num_market_pairs: number;
    date_added: Date;
    tags: string[];
    max_supply?: number;
    circulating_supply: number;
    total_supply: number;
    platform: Platform;
    cmc_rank: number;
    last_updated: Date;
    quote: Quote;
}

export interface CoinMarketCapResponse {
    status: Status;
    data: Datum[];
}