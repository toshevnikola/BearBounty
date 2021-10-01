pairs_to_check_query = """select dcabot.trading_pairs,
       dcabot.id   as bot_id,
       e.name      as exchange_name,
       e.id        as exchange_id,
       u.id        as user_id,
       ue.id       as user_exchange_id,
       dcabot.base_order_amount as base_order_amount
from dcabot
         left join userexchange ue on dcabot.user_exchange_id = ue.id
         left join exchange e on e.id = ue.exchange_id
         left join "user" u on u.id = ue.user_id
         left join deal d on dcabot.id = d.bot_id
where dcabot.is_running = True
  and dcabot.in_deal = False
"""
