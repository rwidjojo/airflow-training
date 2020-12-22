CREATE TABLE recent_orders (
    order_id smallint NOT NULL PRIMARY KEY,
    customer_id bpchar,
    employee_id smallint,
    order_date date,
    required_date date,
    shipped_date date,
    ship_via smallint,
    freight real,
    ship_name character varying(40),
    ship_address character varying(60),
    ship_city character varying(15),
    ship_region character varying(15),
    ship_postal_code character varying(10),
    ship_country character varying(15)
);

CREATE TABLE shipping_count (
    order_date date NOT NULL,
    ship_country character varying(15),
    ship_count int,
    PRIMARY KEY (order_date, ship_country)
);


INSERT INTO public.recent_orders(order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country)
SELECT 
  order_id, customer_id, employee_id,
  TO_DATE('2020-12-' || EXTRACT(DAY from order_date), 'YYYY-MM-DD') order_date, /* change year and month to 2020-12 */
  required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, 
  ship_region, ship_postal_code, ship_country 
FROM public.orders;