import flet

def view_rent(**kwargs):
    print("Rent Page")
    page = kwargs.get("page")
    staff_store_id = kwargs.get("staff_store_id")
    conn = kwargs.get("conn")
