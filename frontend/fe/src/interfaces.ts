export interface Exchange{
    id:number,
    name:string,
    pairs:Array<string>,
    is_available:boolean
}
export interface UserExchange{
    id:number,
    user_id:number,
    is_valid:boolean,
    exchange:Exchange,
    currency:string,
    balance:number
}
export interface Bot{
    name?:string,
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
    user_exchange_id:number
}