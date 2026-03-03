class Search:
    #############################################
    # class_menu search customer
    #############################################

    customer_name_query\
        = """
        select customer_id
        from customer_data
        where activebool is true
        and name ilike %s
        """

    customer_id_query\
        = """
        select 
            customer_id ,
	        customer_store ,
            name ,
            email ,
            phone ,
            address ,
            last_rental_date ,
            status ,
            customer_store ,
            last_rental_store
        from customer_data
        where activebool is true
        and customer_id = ANY(%s)
        """

    #############################################
    # class_menu search inventory
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
        """

    #############################################
    # class_menu search rental
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
                else 'Overdue'
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
                else 'Overdue'
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
                else 'Overdue'
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
                when return_date is null and over_due is not null then 'Overdue'
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

    rental_history_data_query \
        = """
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
        where rental_id = %s
        order by title desc
        """

    #############################################
    # class_menu search payment
    #############################################

    payment_search_name_query\
        = """
        select p.payment_id
        from payment p
        inner join rental_data r on p.rental_id = r.rental_id 
        where r.store_id = %s
        and r.name ilike %s
        """

    payment_search_count_query\
        ="""
        select count(*)
        from payment p
        inner join rental_data r on p.rental_id = r.rental_id 
        where r.store_id = %s
        and p.payment_id = ANY(%s)
        """

    payment_search_id_query\
        = """
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
        where r.store_id = %s
        and p.payment_id = ANY(%s)
        order by payment_date desc, name
        limit 10 offset %s
        """

    payment_receipt_query\
        = """
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
        where payment_id = %s
        order by 
            amount asc , 
            title asc
        """

class Rental:
    #############################################
    # class_menu add return
    #############################################

    payment_return_query\
        = """   
        begin;
        update rental 
        set return_date = now() 
        where rental_id = %(rid)s;
        update payment
        set 
            payment_date = now() , 
            amount = (
                select	
                    sum(case 
                        when (coalesce(r.return_date::date, current_date) - r.rental_date::date) > f.rental_duration
                            then least(((coalesce(r.return_date::date, current_date) - r.rental_date::date) - f.rental_duration) * 1.0 , f.replacement_cost)
                    else 0
                    end + f.rental_rate)
                from payment p
                left join rental r on p.rental_id = r.rental_id
                inner join inventory i on i.inventory_id = any(r.inventory_id)
                inner join film f on i.film_id = f.film_id
                where p.rental_id = %(rid)s
            )
        where payment.rental_id = %(rid)s;
        commit;
        """

class Delete:
    customer_delete_query\
        = """
        begin;
        update customer
        set activebool = False
        where customer_id = %s
        and first_name || ' ' || last_name = %s;
        commit;
        """