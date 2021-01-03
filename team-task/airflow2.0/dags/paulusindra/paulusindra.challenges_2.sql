select
    order_date
    , count(order_id) as order_count
from
    public.paulusindra_orders
group by
    1
order by 
    order_date asc