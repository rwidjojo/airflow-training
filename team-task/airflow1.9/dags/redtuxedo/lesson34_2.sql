SELECT order_date, count(order_id) as countid from rwidjojo_orders
GROUP BY order_date
ORDER BY order_date ASC;