create or replace view public.customer_data as 
(select DISTINCT ON (c.customer_id)
	c.first_name ||' '||c.last_name as name ,
	c.customer_id ,
	c.email ,
	a.phone as phone ,
    a.address,
	coalesce(to_char(r.rental_date,'YYYY-MM-DD'),'Not Rental Data') as last_rental_date ,
	case 
		when r.rental_id is null then 'Not Rental Data'
		when r.return_date is null 
			and CURRENT_DATE > (r.rental_date::date + f.rental_duration)
			then 'Overdue'
		when r.return_date is null 
			and CURRENT_DATE <= (r.rental_date::date + f.rental_duration)
			then 'Rental'
		else 'Normal'
	end as status ,
	c.store_id as customer_store,
	c.activebool ,
	i.store_id as last_rental_store
from customer c
inner join address a on c.address_id = a.address_id
left join rental r on r.customer_id = c.customer_id 
left join inventory i on i.inventory_id = r.inventory_id[1] 
left join film f on i.film_id = f.film_id
order by c.customer_id , last_rental_date desc);

CREATE OR REPLACE VIEW public.inventory_data as (
select 
	i.inventory_id ,
	f.title ,
	i.store_id ,
	r.rental_date::date ,
	r.return_date::date ,
	case 
		when rank() over (partition by i.inventory_id , i.store_id order by r.rental_date desc) = 1 then 1
	else null
	end as status ,
	f.rental_rate 
from inventory i
inner join film f
	on i.film_id = f.film_id
inner join rental r
	on i.inventory_id = any(r.inventory_id));

CREATE OR REPLACE VIEW public.rental_data as (
select 
	r.rental_id ,
	c.first_name ||' '||c.last_name as name ,
	string_agg(f.title,', ' order by f.title) as full_title ,
	min(f.title) as title ,
	case when count(f.title) = 1 then '' else '+'||(count(f.title) - 1)||' more' end count_title ,
	to_char(r.rental_date,'YYYY-MM-DD HH24:MI:SS') as rental_date ,
	(r.rental_date::date + max(f.rental_duration)) as due_day ,
	r.return_date::date ,
	max(f.rental_duration) as rental_duration ,
	case 
		when r.return_date is null 
			and CURRENT_DATE > (r.rental_date::date + max(f.rental_duration))
			then sum((CURRENT_DATE - (r.rental_date::date + f.rental_duration)))
	end as over_due ,
	i.store_id
from rental r
inner join customer c 
	on r.customer_id = c.customer_id 
inner join inventory i 
	on i.inventory_id = any(r.inventory_id) 
inner join film f 
	on i.film_id = f.film_id
where c.activebool is True
group by
	r.rental_id ,
	name ,
	r.rental_date ,
	r.return_date ,
	i.store_id);

CREATE OR REPLACE VIEW public.rental_full_status as (
select
	r.customer_id as customer_id , -- "고객 ID"
	p.payment_id as payment_id , -- "결제 ID"
	r.rental_id as rental_id , -- "대여 ID"
	array_to_string(r.inventory_id,', ') as inventory_id , -- "재고 ID"
	i.store_id as item_store_id ,-- "대여 매장 ID"
	c.store_id as customer_store_id , -- "고객 소속 매장 ID"
	sum(f.rental_rate) as total_base_rental_rate , -- "기본 대여료($)""
	to_char(r.rental_date,'YYYY-MM-DD HH24:MI:SS') as rental_date , -- "대여 시작일"
	to_char(p.payment_date,'YYYY-MM-DD HH24:MI:SS') as payment_date , -- "결제일"
	r.return_date::date as return_date , -- "반납일"
	max(f.rental_duration) * INTERVAL '1 day' as rental_limit_days , -- "대여가능기간"
	greatest(0,
		case 
			when r.return_date is not null 
				then (r.return_date::date - r.rental_date::date)
			else (CURRENT_DATE - r.rental_date::date) 
		end
	) * INTERVAL '1 day' as days_rented , -- "고객대여기간"
	case 
		when r.return_date is not null 
		and (r.return_date::date - r.rental_date::date) - max(f.rental_duration) > 0
			then sum((r.return_date::date - r.rental_date::date) - f.rental_duration)
		when r.return_date is null 
		and r.rental_date::date + max(f.rental_duration) < CURRENT_DATE
			then sum(CURRENT_DATE - (r.rental_date::date + f.rental_duration))
	end as days_overdue , -- "연체 기간"
	case 
		when r.return_date is not null 
		and (r.return_date::date - r.rental_date::date) > max(f.rental_duration)
			then sum(least(((r.return_date::date - r.rental_date::date) - f.rental_duration) * 1.0 , f.replacement_cost))
		when r.return_date is null 
		and (r.rental_date::date + max(f.rental_duration)) < CURRENT_DATE 
			then sum(least(CURRENT_DATE - (r.rental_date::date + f.rental_duration) , f.replacement_cost))
	end as est_late_fee , -- "연체료"
	case 
		when r.return_date is not null 
		and (r.return_date::date - r.rental_date::date) - max(f.rental_duration) > 0
			then to_char(r.return_date,'YYYY-MM-DD HH24:MI:SS')
	end as overdue_paid_date , -- "연체료 결제일"
	p.amount as total_amount -- "총 결제액 (기본 대여료)"
from payment p
left join rental r
	on p.rental_id = r.rental_id
inner join customer c
on r.customer_id = c.customer_id
inner join inventory i
	on i.inventory_id = any(r.inventory_id) 
inner join film f
	on i.film_id = f.film_id
group by
	r.customer_id ,
	p.payment_id , 
	r.rental_id ,
	r.inventory_id ,
	i.store_id ,
	c.store_id ,
	r.rental_date ,
	p.payment_date ,
	r.return_date);

create or replace view public.view_receipt as (
with receipt as (
select 
	p.payment_id ,
	to_char(r.rental_date,'YYYY-MM-DD HH24:MI:SS') as rental_date ,
	c.first_name ||' '||c.last_name as name ,
	f.poster_path ,
	f.title ,
	f.rental_rate ,
	p.amount ,
    r.rental_id
from payment p
inner join rental r
	on p.rental_id = r.rental_id
inner join customer c
	on p.customer_id = c.customer_id
inner join inventory i 
	on i.inventory_id = any(r.inventory_id) 
inner join film f 
	on i.film_id = f.film_id
group by
	p.payment_id ,
	f.film_id ,
	r.rental_id ,
	c.customer_id
) , union_teist as (
select payment_id , rental_date , name , null , null , sum(rental_rate) as total_rental_rate , amount , amount * 0.1 as tax , amount * 1.1 as total , rental_id
from receipt
group by payment_id, rental_date , name , amount , rental_id
), union_overdue_return as (
select r2.payment_id , r2.rental_date , r2.name , null , 
case when r3.return_date is not null then 'Total Payment (Inc. Overdue)'
else 'Total Payment (Unreturned)' end , r2.total_rental_rate , r2.amount , tax , total
from union_teist r2
inner join rental_data r3 on r2.rental_id  = r3.rental_id
where r3.due_day < coalesce(r3.return_date, current_date)
union all
select r2.payment_id , r2.rental_date , r2.name , null , 'Total Payment' , r2.total_rental_rate , r2.amount , tax , total
from union_teist r2
inner join rental_data r3 on r2.rental_id  = r3.rental_id
where r3.due_day >= coalesce(r3.return_date, current_date)
) , union_receipt as (
select r.payment_id , r.rental_date , r.name , r.poster_path , r.title , r.rental_rate , null as amount , r.rental_rate * 0.1 as tax , r.rental_rate * 1.1 as total
from receipt r
union all
select * from union_overdue_return)
select * from union_receipt);