select r.rental_id , r.inventory_id , r.customer_id , r.rental_date , r.return_date from rental r ;
select i.inventory_id , i.film_id from inventory i ;
select f.film_id , cast(f.rental_duration||'days' as interval) from film f ;
select fc.film_id , fc.category_id from film_category fc ;
select c.category_id, c.name from category c ;

with Genre_Category as (
select
	r.rental_id , 
	r.inventory_id , 
	r.customer_id , 
	r.rental_date as 대여시작일, 
	r.return_date as 반납일 ,
	cast(f.rental_duration||'days' as interval) as 대여일 ,
	r.rental_date + cast(f.rental_duration||'days' as interval) as 반납예정일 ,
	r.return_date - (r.rental_date + cast(f.rental_duration||'days' as interval)) as 연체일 ,
	c.name
from rental r 
inner join inventory i 
	on i.inventory_id = any(r.inventory_id)
inner join film f 
	on i.film_id = f.film_id
inner join film_category fc 
	on f.film_id = fc.film_id
inner join category c 
	on fc.category_id = c.category_id
where r.return_date is not null
  and r.return_date > (r.rental_date + cast(f.rental_duration||'days' as interval))
)
select 
	name , 
	count(name) as overdue_count , 
	JUSTIFY_INTERVAL(avg(연체일)) as avg_overdue_duration 
from Genre_Category 
group by name
order by avg_overdue_duration desc ;


select a.actor_id , a.first_name , a.last_name from actor a ;
select fa.actor_id , fa.film_id from film_actor fa ;
select fc.film_id , fc.category_id from film_category fc ;
select c.category_id , c.name from category c ;

select 
	a.actor_id ,
	a.first_name , 
	a.last_name ,
	count(fa.film_id) as "Total Films",
	count(distinct fc.category_id) as "Genre Diversity"
from actor a 
inner join film_actor fa 
	on a.actor_id = fa.actor_id 
inner join film_category fc 
	on fa.film_id = fc.film_id 
inner join category c 
	on fc.category_id = c.category_id 
group by
	a.actor_id ,
	a.first_name , 
	a.last_name
having
	count(fa.film_id) >= 20
order by 
	a.first_name ,
	a.last_name ,
	"Genre Diversity" desc, 
	"Total Films" desc ;

select c.customer_id from customer c ;
select r.customer_id , count(r.rental_id ) as "Total Rentals" from rental r group by r.customer_id ;
select p.customer_id , sum(p.amount) as "Total Spent" from payment p group by p.customer_id;

with TotalRentals as (
	select
		r.customer_id , 
		count(r.rental_id ) as Total_Rentals
	from rental r 
	group by r.customer_id
) , TotalSpent as (
	select 
		p.customer_id , 
		sum(p.amount) as Total_Spent
	from payment p 
	group by p.customer_id)
select 
	c.customer_id ,
	c.first_name ,
	c.last_name ,
	coalesce(r.Total_Rentals,0) as Total_Rentals,
	coalesce(s.Total_Spent,0) as Total_Spent ,
	case
		when coalesce(s.Total_Spent,0) >= 150 and coalesce(r.Total_Rentals,0) >= 30 then 'Elite'
		when coalesce(s.Total_Spent,0) >= 150 and coalesce(r.Total_Rentals,0) < 30 then 'High Spender'
		when coalesce(s.Total_Spent,0) < 150 and coalesce(r.Total_Rentals,0) >= 30 then 'Frequent User'
		else 'Standard'
	end as customer_tier ,
	round((s.total_spent / r.total_rentals ),2) as avg_price_per_rental
from customer c 
left join TotalRentals r
	on c.customer_id = r.customer_id
left join TotalSpent s
	on c.customer_id = s.customer_id
order by 
	Total_Spent desc ,
	total_rentals desc ;

select r.inventory_id , to_char((r.return_date - r.rental_date + cast(1||'days' as interval)),'dd') as days 
from rental r ; -- 영화 재고번호 별 대여일
select i.store_id , i.film_id , i.inventory_id from inventory i 
order by i.store_id , i.film_id , i.inventory_id ; -- 매장에서 보유중인 영화 , 영화 재고번호
select f.film_id , f.rental_rate  from film f order by f.film_id ; -- 영화별 대여비

with rental_days as (
	select
		r.inventory_id , 
		to_char((r.return_date - r.rental_date + cast(1||'days' as interval)),'dd') as days
	from rental r 
) , store_rental_rate as (
	select
		i.store_id ,
		f.film_id ,
		i.inventory_id ,
		f.rental_rate 
	from inventory i 
	join film f 
		on i.film_id = f.film_id)
select 
	r.store_id , 
	sum(((cast(d.days as numeric))* r.rental_rate)) as rental_rate_days ,
	rank() over(order by sum(((cast(d.days as numeric))* r.rental_rate)) desc) as Store_Rank
from store_rental_rate r
join rental_days d
	on r.inventory_id = d.inventory_id 
group by
	r.store_id ;

with store_rate_rank as (
	select 
		i.store_id ,
		case 
			when f.rental_rate > 3 then 'Premium'
			when f.rental_rate > 1 and f.rental_rate <= 3 then 'Regular'
			when f.rental_rate <= 1 then 'Cheap'
			else 'not'
		end as rate_rank
	from rental r 
	join inventory i 
		on i.inventory_id = any(r.inventory_id) 
	join film f 
		on i.film_id = f.film_id 
)
select 
	store_id ,
	count(rate_rank) filter(where rate_rank = 'Cheap') as cheap_count ,
	count(rate_rank) filter(where rate_rank = 'Regular') as regular_count ,
	count(rate_rank) filter(where rate_rank = 'Premium') as premium_count
from store_rate_rank 
group by store_id ;

select 
	store_id ,
	count(f.rental_rate) filter(where f.rental_rate <= 1) as cheap_count ,
	count(f.rental_rate) filter(where f.rental_rate > 1 and f.rental_rate <= 3) as regular_count ,
	count(f.rental_rate) filter(where f.rental_rate > 3) as premium_count
from rental r 
join inventory i 
	on i.inventory_id = any(r.inventory_id) 
join film f 
	on i.film_id = f.film_id 
group by store_id ;

select * from customer c ;

select 
	split_part(c.email , '@', 2) as domain ,
	count(c.customer_id ) as user_count 
from customer c 
group by domain
order by user_count desc ;

select * from film f ;
select * from film_actor fa ;
select * from actor a ;

select
	f.title as title,
	string_agg(concat(a.first_name , ' ' , a.last_name),', ' order by a.first_name ) as actor_list
from film f 
join film_actor fa 
	on f.film_id = fa.film_id
join actor a 
	on fa.actor_id = a.actor_id
group by title 
having count(fa.actor_id) >=10
order by title ;

select c.customer_id from customer c ;
select r.customer_id , r.rental_id , r.inventory_id , r.rental_date from rental r ;
select i.inventory_id , i.film_id from inventory i ;
select f.film_id , f.title from film f ;

with customer_rental_rank as (
	select 
		c.customer_id , 
		c.last_name ,
		f.title ,
		r.rental_date ,
		rank() over (partition by c.customer_id order by r.rental_date desc) as customer_rental_rank
	from customer c 
	left join rental r 
		on c.customer_id = r.customer_id 
	left join inventory i 
		on i.inventory_id = any(r.inventory_id)
	left join film f
		on i.film_id = f.film_id
)
select 
	customer_id ,
	last_name ,
	title ,
	rental_date
from customer_rental_rank 
where customer_rental_rank = 1 ;

select 
	distinct on (c.customer_id)
	c.customer_id ,
	c.last_name ,
	f.title ,
	r.rental_date
from customer c 
left join rental r 
	on c.customer_id = r.customer_id 
left join inventory i 
	on i.inventory_id = any(r.inventory_id)
left join film f
	on i.film_id = f.film_id
order by 
	c.customer_id ,
	rental_date desc ;

select payment_date
from payment p 
where p.payment_date >= '2007-02-20'
and p.payment_date < '2007-02-21' ;

select a.phone , '972574862516'
from address a 
where a.phone = cast('972574862516' as varchar(20)) ;

select a.phone
from address a 
where a.phone = '972574862516' ;

select * from payment p 
where p.payment_id = 17999
order by p.staff_id desc
limit 10;

select * from payment p 
order by p.payment_date desc
offset 700 rows fetch next 10 rows only ;

select * from payment p 
where p.payment_date > '2007-04-30 14:18:06.996'
order by p.payment_date desc
offset 0 rows fetch next 10 rows only ;

select * from payment p;

select * , row_number() over(partition by p.amount order by p.staff_id ) from payment p;

with recursive emp_level as (
	select
		emp_id ,
		name ,
		manager_id ,
		0 as level
	from employees e
	where e.manager_id is null
	union all
	select
		emp_id ,
		name ,
		manager_id ,
		l.level + 1 as level
	from employees e
	left join emp_level l
		on e.manager_id = l.emp_id
)
select
	name ,
	level as lvl
from emp_level ;

select
	store_name , 
	sum(sales) filter(where category = 'Coffee') as coffee_sales ,
	sum(sales) filter(where category = 'Dessert') as dessert_sales
from store_sales
group by store_name ;

select
	student_name ,
	math ,
	english
from exam_scores ;

select
	student_name ,
	'math' as subject ,
	math as score
from exam_scores
union
select
	student_name ,
	'english' as subject ,
	english as score
from exam_scores ;

select
	team_name ,
	cast(string_agg(member_name,', ' order by member_name) as varchar(200)) as members
from team_projects
group by team_name ;

select * from customer c ;

select s.username , s.password , s.store_id , s.active from staff s where s.username = 'Mike' 
and s."password" = '8cb2237d0679ca88db6464eac60da96345513964' and s.active is true;

select s.username, s.password, s.store_id , a.address , s.active
                               from staff s
                               inner join store s2 
                               on s.store_id = s2.store_id 
                               inner join address a
                               on s2.address_id = a.address_id 
                               where s.username = %s
                                 and s.password = %s
                                 and s.active is true;

select address from address;

select c.customer_id , c.first_name||' '||c.last_name as Name , c.email , r.rental_date , f.title , r.return_date 
from customer c 
inner join rental r 
on c.customer_id = r.customer_id
inner join inventory i 
on i.inventory_id = any(r.inventory_id)
inner join film f 
on i.film_id = f.film_id
where c.customer_id = 443;

select *
from payment p 
left join customer c 
on p.customer_id = c.customer_id
left join rental r 
on p.rental_id = r.rental_id;

select *
from customer c 
left join rental r 
on c.customer_id = r.customer_id 
left join payment p 
on c.customer_id = p.customer_id ;

select * from customer c left join rental r on c.customer_id = r.customer_id ;

SELECT count(*) as error_count
FROM payment p
JOIN rental r ON p.rental_id = r.rental_id
WHERE p.payment_date < r.return_date;

SELECT 
    c.create_date as 가입일,
    r.rental_date as 대여일,
    r.return_date as 반납일,
    p.payment_date as 결제일
FROM payment p
JOIN rental r ON p.rental_id = r.rental_id
JOIN customer c ON r.customer_id = c.customer_id
ORDER BY r.rental_date DESC
LIMIT 10;

select 
	i.inventory_id ,
	r.rental_date , 
	r.return_date ,r
from inventory i
inner join rental r 
	on i.inventory_id = r.inventory_id;

검색하는 ID %s 와 동일한 title인 id를 찾는 쿼리

with search_iv_title_1 as (
	select f.film_id
	from inventory i 
	inner join film f 
		on i.film_id = f.film_id
	where i.inventory_id = 1
), search_iv_title_2 as (
	select 
		row_number() over (partition by i.inventory_id order by r.rental_date desc) as row ,
		i.inventory_id , 
		f.title ,
		r.rental_date ,
		r.return_date 
	from inventory i 
	inner join search_iv_title_1 s 
		on i.film_id = s.film_id
	inner join film f 
		on i.film_id = f.film_id 
	left join rental r 
		on i.inventory_id = r.inventory_id 
)
select 
	inventory_id , 
	title, 
	case 
		when rental_date is not null and return_date is null then 'Checked out'
		else 'In stock' 
	end as status
from search_iv_title_2 
where row = 1;

-- 결과가 0건이어야 정상입니다.
SELECT 
    r1.inventory_id,
    r1.rental_date AS current_rental,
    r2.return_date AS prev_return,
    r1.rental_id AS current_id,
    r2.rental_id AS prev_id
FROM rental r1
JOIN rental r2 ON r1.inventory_id = r2.inventory_id
WHERE r1.rental_date > r2.rental_date -- r1이 r2보다 나중에 빌렸는데
  AND r1.rental_date < r2.return_date; -- r2가 반납되기 전에 r1이 시작됨 (중복!)
  
  SELECT 
    r.inventory_id,
    r.rental_id, 
    r.rental_date, 
    r.return_date,
    c.first_name || ' ' || c.last_name AS customer_name
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
where r.return_date is null
ORDER BY r.rental_date ASC;

-- 결과가 0건이어야 정상입니다.
SELECT count(*) AS error_count
FROM payment p
JOIN rental r ON p.rental_id = r.rental_id
WHERE p.payment_date < r.return_date; 
-- 결제일이 반납일보다 빠르면 에러

-- 결과가 0건이어야 정상입니다.
SELECT count(*) AS error_count
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
WHERE r.rental_date < c.create_date;

select 
	f.film_id ,
	f.release_year ,
	f.title ,
	l."name" ,
	f.rental_duration ,
	f.rental_rate ,
	f.replacement_cost ,
	f.rating ,
	f.description
from film f 
inner join "language" l 
	on f.language_id = l.language_id
where f.title ILike %s or f.description ILike %s
order by
	f.film_id ,
	f.release_year ,
	f.title ,
	f.description
	
select * from inventory_data

select distinct count(*) from not_return_customer nrc ;

select 
	c.customer_id , 
	c.first_name || ' ' || c.last_name as name, 
	c.email, 
	a.address, 
	c.create_date ,
	c.store_id ,
	case when n.customer_id is not null then 'Overdue' else 'Normal' end as Status
from customer c
inner join address a 
	on c.address_id = a.address_id
left join not_return_customer n 
	on n.customer_id = c.customer_id;

select customer_id
from customer
where first_name ilike '%sss%' 
or last_name ilike '%sss%';

select
	inventory_id ,
	title ,
	case when store_id = 1 then '🇨🇦 Lethbridge' else '🇦🇺 Woodridge' end as store ,
    case when return_date is not null then 'In stock' else 'Checked out' end as status ,
    rental_date ,
    rental_rate
from inventory_data
where status is not null
and inventory_id = 31;

select distinct inventory_id
from inventory_data
where title ilike '%fire%';


select 
    rental_id ,
    name ,
    title ,
    rental_date ,
    due_day ,
    over_due ,
    case 
	    when over_due is not null then 'Overdue'||' ('||date_trunc('day',over_due)||')' 
	    when today < due_day then 'Unreturned'
    	else 'Returned' 
	end as status
from rental_data
order by return_date desc, rental_date desc

-- due today
select count(*)
from rental_data
where return_date is null
and due_day::date = today
and store_id = 1;

-- overdue
select *
from rental_data
where return_date is null
and due_day > today
and store_id = 1;

-- total
select count(*)
from rental_data
where return_date is null
and store_id = 1;

select 
    rental_id ,
    name ,
    title ,
    to_char(rental_date,'YYYY-MM-DD hh:mm:ss') as rental_date ,
    to_char(due_day,'YYYY-MM-DD hh:mm:ss') as due_day ,
    case
        when due_day < today 
        then 'Overdue'||' ('||replace(date_trunc('day',over_due)::text,'00:00:00','1 days')||')'
        else 'Unreturned'
    end as status
from rental_data
where return_date is null
and store_id = 1
order by return_date desc, rental_date desc;

select replace(date_trunc('day',over_due),'00:00:00','0')
from rental_data;

select distinct count(r.rental_date)
from rental r ;

select * from payment p

-- 대여 반납 결제 
begin;
update rental 
set return_date = now() 
where rental_id = 14697;
update payment
set 
	payment_date = now() , 
	amount = (
		select	
			case 
				when r.return_date::date - r.rental_date::date > f.rental_duration
				then least(((r.return_date::date - r.rental_date::date) - f.rental_duration) * 1.0 
				, f.replacement_cost)
			else 0
			end + f.rental_rate
		from payment p
		left join rental r
			on p.rental_id = r.rental_id
		inner join customer c
		on r.customer_id = c.customer_id
		inner join inventory i
			on i.inventory_id = any(r.inventory_id) 
		inner join film f
			on i.film_id = f.film_id
		where p.rental_id = 14697)
where payment.rental_id = 14697;
commit;

select
	case 
		when now()::date - r.rental_date::date > f.rental_duration
		then least(((now()::date - r.rental_date::date) - f.rental_duration) * 1.0 , f.replacement_cost)
	else 0
	end + f.rental_rate -- 연체료($) + 기본 대여료 = 21.98
from payment p
left join rental r
	on p.rental_id = r.rental_id
inner join customer c
on r.customer_id = c.customer_id
inner join inventory i
	on i.inventory_id = any(r.inventory_id) 
inner join film f
	on i.film_id = f.film_id
where p.rental_id = 14697

select r.rental_id ,r.days_overdue , r.base_rental_rate , r.est_late_fee , r.total_amount from rental_full_status r 
where r.return_date is null and r.days_overdue is not null;
select * from rental_full_status r;

select count(*) from rental; -- 13756

select count(*) from payment; -- 13756

select * , row_number() over (partition by p.rental_id order by p.rental_id) from payment p --13853

select p.rental_id ,r.rental_id  
from payment p
left join rental r 
on p.rental_id = r.rental_id
where r.rental_id is null -- 0

select
	r.rental_id , 
	r.customer_id , 
	r.inventory_id , 
	r.rental_date , 
	(r.rental_date::date + r.rental_limit_days)::date as due_date ,
	case when r.return_date is not null then 'Returned'
		when r.return_date is null then 
		case when r.rental_limit_days >= r.days_rented then 'Rented'
			when r.est_late_fee = f.replacement_cost then 'Lost'
		else 'Overdue' end
	end as status ,
	r.return_date ,
	r.est_late_fee , 
	f.replacement_cost
from rental_full_status r
inner join inventory i
on i.inventory_id = any(r.inventory_id) 
inner join film f 
on i.film_id = f.film_id 
where r.item_store_id = 1
and r.return_date is null

select *
from rental r
inner join customer c 
on r.customer_id = c.customer_id 
inner join inventory i 
on i.inventory_id = any(r.inventory_id) 
inner join film f
on i.film_id = f.film_id 
where r.return_date is null
and i.store_id = 1
order by r.rental_date desc

select *
from rental_data
where return_date is null
and store_id = 1

select 
	r.rental_id ,
	c.first_name ||' '||c.last_name as name ,
	f.title ,
	r.rental_date ,
	(r.rental_date::date + f.rental_duration) as due_day ,
	r.return_date ,
	f.rental_duration ,
	case 
		when r.return_date is null 
			and CURRENT_DATE > (r.rental_date::date + f.rental_duration)
			then (CURRENT_DATE - (r.rental_date::date + f.rental_duration))
	end as over_due ,
	i.store_id
from rental r
inner join customer c 
	on r.customer_id = c.customer_id 
inner join inventory i 
	on i.inventory_id = any(r.inventory_id)
inner join film f 
	on i.film_id = f.film_id
	
select 
    rental_id ,
    name ,
    title ,
    to_char(rental_date,'YYYY-MM-DD HH24:MI:SS') as rental_date ,
    due_day ,
    case when over_due is null then 'Unreturned'
    	else 'Overdue'||' ('||over_due * interval '1 day'||')'
    end as status
from rental_data
where store_id = 1
and rental_id = 1
order by name

select count(*)
from rental_data
where return_date is null
and due_day = CURRENT_DATE
and store_id = 1

select distinct rating from film

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
	r.return_date 
	
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
group by
	r.rental_id ,
	name ,
	r.rental_date ,
	r.return_date ,
	i.store_id
	
select 
    rental_id ,
    name ,
    title ,
    rental_date ,
    due_day ,
    case when over_due is null then 'Unreturned'
        else 'Overdue'||' ('||over_due * interval '1 day'||')'
    end as status ,
    count_title ,
    full_title
from rental_data
where return_date is null
and store_id = 1
order by name

select rfs.payment_id , rfs.customer_id , rfs.rental_date , rfs.inventory_id , rfs.total_amount , rfs.days_overdue
from rental_full_status rfs ;

select 
	p.payment_id ,
	r.name ,
	r.rental_date ,
	r.title ,
	p.amount as subtotal ,
	p.amount * 0.1 as tax ,
	p.amount * 1.1 as total,
	case when return_date is null and over_due is null then 'Unreturned'
        when return_date is null and over_due is not null then 'Overdue'||' ('||over_due * interval '1 day'||')'
        else 'Returned'
    end as status ,
	r.count_title ,
	r.full_title
from payment p 
inner join rental_data r on p.rental_id = r.rental_id 
where p.payment_id = 11742
and r.store_id = 1
order by payment_date desc, name;

select *
from payment p
inner join rental_data r on p.rental_id = r.rental_id 
where r.store_id = 1
and r.due_day < r.return_date 

select 
    p.payment_id ,
    r.name ,
    r.rental_date ,
    r.title ,
    p.amount as subtotal ,
    p.amount * 0.1 as tax ,
    p.amount * 1.1 as total,
    case when return_date is null and over_due is null then 'Unreturned'
        when return_date is null and over_due is not null then 'Overdue'||' ('||over_due * interval '1 day'||')'
        else 'Returned'
    end as status ,
    r.count_title ,
    r.full_title
from payment p 
inner join rental_data r on p.rental_id = r.rental_id 
where r.store_id = 1
--limit 10 offset 220

select 
	payment_id ,
	rental_date ,
	name ,
	poster_path ,
	title ,
	rental_rate ,
	amount ,
	tax ,
	total
from view_receipt
where payment_id = 15017
order by 
	amount asc , 
	title asc;

select *
from rental_data
where store_id = 1
and name ilike 'Nancy Thomas'

select 
    rental_id ,
    name ,
    title ,
    rental_date ,
    due_day ,
    case 
        when return_date is null and over_due is null then 'Unreturned'
        when return_date is null and over_due is not null then 'Overdue'||' ('||over_due * interval '1 day'||')'
        else 'Returned'
    end as status ,
    count_title ,
    full_title
from rental_data
where store_id = 2
and name ilike 'Nancy Thomas'
order by name , rental_date desc , over_due desc

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
where c.customer_id = 12
group by
	r.rental_id ,
	name ,
	r.rental_date ,
	r.return_date ,
	i.store_id;

select *
from rental_data
where name = 'Charles Kowalski'

select DISTINCT ON (c.customer_id)
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
where c.customer_id = '53' 
order by c.customer_id , last_rental_date desc

select 
    rental_id ,
    name ,
    title ,
    poster_path ,
    rental_date ,
    due_date ,
    return_data ,
    return_date
from rental_history
where rental_id = 8716
order by title desc

with all_d as (
select
	r.rental_id ,
	c.first_name || ' ' || c.last_name as name ,
	f.title ,
	f.poster_path ,
	to_char(r.rental_date,'YYYY-MM-DD HH24:MI:SS') as rental_date ,
	r.rental_date::date + f.rental_duration as due_date ,
	case 
		when r.return_date is null 
			and current_date > (r.rental_date::date + f.rental_duration) 
			then 'Overdue' || ' (' || (current_date - r.rental_date::date) * interval '1Day' || ')'
		when r.return_date is null 
			and current_date <= (r.rental_date::date + f.rental_duration) then 'Unreturned'
		else to_char(r.return_date,'YYYY-MM-DD')
	end as return_data , 
	r.return_date::date as return_date ,
	c.activebool
from rental r
inner join customer c on r.customer_id = c.customer_id 
inner join inventory i on i.inventory_id = any(r.inventory_id)
inner join film f on i.film_id = f.film_id
) , union_all as (
select rental_id , name , title , poster_path , rental_date , due_date , return_data , return_date from all_d
union all
select distinct rental_id , name , Null , Null , rental_date , due_date , return_data , return_date from all_d)
select * from union_all

select * from payment

begin;
update rental 
set return_date = now() 
where rental_id = %s;
update payment
set 
    payment_date = now() , 
    amount = (
		select	
		    sum(case 
		        when (coalesce(r.return_date::date, current_date) - r.rental_date::date) > f.rental_duration
		        	then least(((coalesce(r.return_date::date, current_date) - r.rental_date::date) - f.rental_duration) * 1.0 
		        	, f.replacement_cost)
		    else 0
		    end + f.rental_rate)
		from payment p
		left join rental r on p.rental_id = r.rental_id
		inner join inventory i on i.inventory_id = any(r.inventory_id)
		inner join film f on i.film_id = f.film_id
		where p.rental_id = %s)
where payment.rental_id = %s;
commit;

select 
	r.rental_id , 
	sum(f.rental_rate) , -- 대여료 합산
	sum(f.replacement_cost) , -- 분실료 합산
	r.rental_date::date , -- 대여일
	r.rental_date::date + max(f.rental_duration) , -- 반납예정일
	case when ((current_date - (r.rental_date::date + max(f.rental_duration))) * 1.0) < 0 then 0
	else (current_date - (r.rental_date::date + max(f.rental_duration))) * 1.0 end , -- 연체일 * 연체료
	least(case when ((current_date - (r.rental_date::date + max(f.rental_duration))) * 1.0) < 0 then 0
	else (current_date - (r.rental_date::date + max(f.rental_duration))) * 1.0 end,sum(f.replacement_cost)) -- 연체일 * 연체료 , 분실료 중 작은 값
from rental r
inner join inventory i on i.inventory_id = any(r.inventory_id)
inner join film f on i.film_id = f.film_id 
where r.rental_id = 15594
group by r.rental_id
order by 5 desc

select 
	sum(f.rental_rate), null
from rental r
inner join inventory i on i.inventory_id = any(r.inventory_id)
inner join film f on i.film_id = f.film_id 
where r.rental_id = 15594;

select 
    c.customer_id ,
    c.first_name ,
    c.last_name ,
    c.email ,
    a.phone ,
    a.address ,
    a.postal_code ,
    c3.country ,
    c2.city ,
    c.activebool
from customer c
inner join address a on c.address_id = a.address_id 
inner join city c2 on a.city_id = c2.city_id 
inner join country c3 on c2.country_id = c3.country_id
--where c.customer_id = %s
--and c.first_name || ' ' || c.last_name = %s

select count(*) from city c inner join country c2 on c.country_id = c2.country_id where c.city = 'Abha' and c2.country = 'Saudi Arabia';

select fulltext from film where fulltext @@ to_tsquery('english', 'doom')

select i.inventory_id 
from inventory i
inner join film f on i.film_id = f.film_id
where f.fulltext @@ to_tsquery('english', 'Iron&Lung')

select i.inventory_id 
from inventory i
inner join film f on i.film_id = f.film_id
where f.title ilike 'Iron Lung'

select *
from city c
inner join country c2 
on c.country_id = c2.country_id 

begin;
with new_address_id as (
    insert into address (address, city_id, postal_code, phone) 
    values ('123rv23v', 5, 42345, 2512534)
    RETURNING address_id
)
insert into customer (store_id, first_name, last_name, email, address_id)
values (1, 'asd', 'asd', '23423@fasd.com', (select address_id from new_address_id))
RETURNING customer_id;
commit;



