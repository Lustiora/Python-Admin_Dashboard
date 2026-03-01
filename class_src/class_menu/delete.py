from class_query import Delete

def customer_delete(**kwargs):
    page = kwargs["page"]
    conn = kwargs["conn"]
    customer_id = kwargs["customer_id"]
    customer_name = kwargs["customer_name"]
    input_data = kwargs["input_data"]
    try:
        cursor = conn.cursor()
        cursor.execute(Delete.customer_delete_query,(customer_id,customer_name,))
        conn.commit()
        print(f"Customer Deleted Successfully. ID: {customer_id}, Name: {customer_name}")
        my_manager = page.session.get("manager")
        if my_manager:
            my_manager.update_main_page(index=2, customer_name=input_data)
    except Exception as err:
        print(err)
        conn.rollback()