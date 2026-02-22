class Search:

    #############################################
    # menu search customer
    #############################################

    customer_name_query\
        = """
        select customer_id
        from customer
        where first_name ilike %s 
        or last_name ilike %s
        """

    customer_id_query\
        = """
        select
            case when c.store_id = 1 then '🇨🇦 Lethbridge' else '🇦🇺 Woodridge' end as store ,
            c.first_name || ' ' || c.last_name as name,
            c.customer_id ,
            c.email ,
            a.phone as phone ,
            a.address,
            c.create_date ,
            case when n.customer_id is not null then 'Overdue' else 'Normal' end as status ,
            c.store_id
        from customer c
        inner join address a
            on c.address_id = a.address_id
        left join not_return_customer n
            on n.customer_id = c.customer_id
        where c.activebool is true
        and c.customer_id = ANY(%s)
        """ # ANY(%s) : 상자에 담겨있는 ID들을 전부 비교

    # <-- View Table Create -->
    # CREATE OR REPLACE VIEW public.not_return_customer as
    # select distinct r.customer_id
    # from rental r
    # inner join inventory i
    # 	on r.inventory_id = i.inventory_id
    # inner join film f
    # 	on i.film_id = f.film_id
    # where r.return_date is null
    # 	and r.rental_date::date + f.rental_duration < CURRENT_DATE;

    #############################################
    # menu search inventory
    #############################################

    film_title_query\
        = """
        select distinct inventory_id
        from inventory_data
        where title ilike %s 
        """

    inventory_id_query\
        = """
        select
            inventory_id ,
            title ,
            case when store_id = 1 then '🇨🇦 Lethbridge' else '🇦🇺 Woodridge' end as store ,
            case when return_date is not null then 'In stock' else 'Checked out' end as status ,
            rental_date ,
            '$'||rental_rate ,
            store_id
        from inventory_data
        where status is not null
        and inventory_id = ANY(%s)
        """ # ANY(%s) : 상자에 담겨있는 ID들을 전부 비교

    # <-- View Table Create -->
    # CREATE OR REPLACE VIEW public.inventory_data as (
    # select
    #     i.inventory_id ,
    #     f.title ,
    #     i.store_id ,
    #     r.rental_date ,
    #     r.return_date ,
    #     case when rank() over (
    #         partition by i.inventory_id , i.store_id order by r.rental_date desc) = 1 then 1
    #     else null end as status ,
    #     f.rental_rate
    # from inventory i
    # inner join film f
    #     on i.film_id = f.film_id
    # inner join rental r
    #     on i.inventory_id = r.inventory_id);

    #############################################
    # menu search rental
    #############################################

    return_total_query\
        = """
        select count(*)
        from rental_data
        where return_date is null
        and store_id = %s
        """

    return_search_total_query \
        = """
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
        and store_id = %s
        order by name
        limit 10 offset %s
        """

    return_overdue_query\
        = """
        select count(*)
        from rental_data
        where return_date is null
        and over_due is not null
        and store_id = %s
        """

    rental_search_overdue_query \
        = """
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
        and store_id = %s
        and over_due is not null
        order by over_due desc 
        limit 10 offset %s
        """

    return_due_today_query\
        = """
        select count(*)
        from rental_data
        where return_date is null
        and due_day = CURRENT_DATE
        and store_id = %s
        """

    rental_search_due_today_query \
        = """
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
        and store_id = %s
        and due_day = CURRENT_DATE
        order by name
        limit 10 offset %s
        """

    rental_search_name_query\
        = """
        select rental_id
        from rental_data
        where store_id = %s
        and name ilike %s
        """

    rental_search_count_query\
        = """
        select count(*)
        from rental_data
        where store_id = %s
        and rental_id = ANY(%s)
        """

    rental_search_id_query\
        = """
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
        where store_id = %s
        and rental_id = ANY(%s)
        order by name , rental_date desc , over_due desc
        limit 10 offset %s
        """

    # <-- View Table Create -->
    # CREATE OR REPLACE VIEW public.rental_data as (
    # select
    # 	r.rental_id ,
    # 	c.first_name ||' '||c.last_name as name ,
    # 	f.title ,
    # 	r.rental_date ,
    # 	(r.rental_date::date + f.rental_duration) as due_day ,
    # 	r.return_date ,
    # 	f.rental_duration ,
    # 	case
    # 		when r.return_date is null
    # 			and CURRENT_DATE > (r.rental_date::date + f.rental_duration)
    # 			then (CURRENT_DATE - (r.rental_date::date + f.rental_duration))
    # 	end as over_due ,
    # 	i.store_id
    # from rental r
    # inner join customer c
    # 	on r.customer_id = c.customer_id
    # inner join inventory i
    # 	on r.inventory_id = i.inventory_id
    # inner join film f
    # 	on i.film_id = f.film_id);

    # <-- View Table Create -->
    # CREATE OR REPLACE VIEW public.rental_full_status as (
    # select
    #     r.customer_id as customer_id , -- "고객 ID"
    #     p.payment_id as payment_id , -- "결제 ID"
    #     r.rental_id as rental_id , -- "대여 ID"
    #     i.inventory_id as inventory_id , -- "재고 ID"
    #     i.store_id as item_store_id ,-- "대여 매장 ID"
    #     c.store_id as customer_store_id , -- "고객 소속 매장 ID"
    #     f.rental_rate as base_rental_rate , -- "기본 대여료($)""
    #     to_char(r.rental_date,'YYYY-MM-DD HH24:MI:SS') as rental_date , -- "대여 시작일"
    #     to_char(p.payment_date,'YYYY-MM-DD HH24:MI:SS') as payment_date , -- "결제일"
    #     to_char(r.return_date,'YYYY-MM-DD HH24:MI:SS') as return_date , -- "반납일"
    #     f.rental_duration * INTERVAL '1 day' as rental_limit_days , -- "대여가능기간"
    #     greatest(0,
    #     case
    #         when r.return_date is not null
    #             then (r.return_date::date - r.rental_date::date)
    #         else (CURRENT_DATE - r.rental_date::date)
    #     end) * INTERVAL '1 day' as days_rented , -- "고객대여기간"
    #     case
    #         when r.return_date is not null
    #         and ((r.return_date::date - r.rental_date::date) * INTERVAL '1 day') - (f.rental_duration * INTERVAL '1 day') > (0 * INTERVAL '1 day')
    #             then ((r.return_date::date - r.rental_date::date) * INTERVAL '1 day') - (f.rental_duration * INTERVAL '1 day')
    #         when r.return_date is null
    #         and (r.rental_date::date + f.rental_duration * INTERVAL '1 day')::date < CURRENT_DATE
    #             then (CURRENT_DATE - (r.rental_date::date + f.rental_duration * INTERVAL '1 day')::date) * INTERVAL '1 day'
    #     end as days_overdue , -- "연체 기간"
    #     case
    #         when r.return_date is not null
    #         and (r.return_date::date - r.rental_date::date) > f.rental_duration
    #             then least(((r.return_date::date - r.rental_date::date) - f.rental_duration) * 1.0 , f.replacement_cost)
    #         when r.return_date is null
    #         and (r.rental_date::date + f.rental_duration * INTERVAL '1 day')::date < CURRENT_DATE
    #             then least((CURRENT_DATE - (r.rental_date::date + f.rental_duration * INTERVAL '1 day')::date) , f.replacement_cost)
    #     end as est_late_fee , -- "연체료"
    #     case
    #         when r.return_date is not null
    #         and ((r.return_date::date - r.rental_date::date) * INTERVAL '1 day') - (f.rental_duration * INTERVAL '1 day') > (0 * INTERVAL '1 day')
    #             then to_char(r.return_date,'YYYY-MM-DD HH24:MI:SS')
    #     end as overdue_paid_date , -- "연체료 결제일"
    #     p.amount as total_amount -- "총 결제액 (기본 대여료)"
    # from payment p
    # left join rental r
    #     on p.rental_id = r.rental_id
    # inner join customer c
    # on r.customer_id = c.customer_id
    # inner join inventory i
    #     on r.inventory_id = i.inventory_id
    # inner join film f
    #     on i.film_id = f.film_id);

class Rental:

    #############################################
    # menu add return
    #############################################

    return_payment_query\
        = """   
        begin;
        update rental 
        set return_date = now() 
        where rental_id = %s;
        update payment
        set 
            payment_date = now() , 
            amount = (
                select	
                    case 
                        when (r.return_date::date - r.rental_date::date) > f.rental_duration
                        then least(((r.return_date::date - r.rental_date::date) - f.rental_duration) * 1.0 , f.replacement_cost)
                    else 0
                    end + f.rental_rate
                from payment p
                left join rental r
                    on p.rental_id = r.rental_id
                inner join customer c
                on r.customer_id = c.customer_id
                inner join inventory i
                    on r.inventory_id = i.inventory_id 
                inner join film f
                    on i.film_id = f.film_id
                where p.rental_id = %s)
        where payment.rental_id = %s;
        commit; 
        """