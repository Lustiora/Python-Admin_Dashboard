import flet
from class_menu.customer_status import customer, customer_delete
from class_window import Colors

def context_menu(
        content, disabled=False, height=35, color=Colors.status_normal, weight=None,
        alignment=flet.alignment.center_left, icon=None, on_click=None):
    return flet.PopupMenuItem(
        content=flet.Container(
            content=flet.Row([flet.Icon(icon, color=color),flet.Text(value=content, color=color, weight=weight)]),
            expand=True,
            alignment=alignment
        ), disabled=disabled, height=height, on_click=on_click
    )

def context_customer_id_data(e, connect_page, **kwargs):
    page = kwargs.get("page")
    staff_store_id = kwargs.get("staff_store_id")
    customer_last_rental_store_id = kwargs.get("customer_last_rental_store_id")
    customer_name = kwargs.get("customer_name")

    def show_location_error_open(e):
        if connect_page == "delete":
            delete_popup()
        elif connect_page == "edit":
            customer("edit", **kwargs)
        else:
            if staff_store_id != customer_last_rental_store_id:
                page.open(location_error)
            else:
                connect(connect_page, **kwargs)

    def show_location_error_close_and_connect(e):
        page.close(location_error)
        connect(connect_page, **kwargs)

    def delete_popup():
        location_error.icon = flet.Icon(
            flet.Icons.WARNING, color=flet.Colors.AMBER_700, size=30, shadows=flet.BoxShadow(
                spread_radius=2, blur_radius=2, color=flet.Colors.BLACK))
        location_error.content = flet.Text(
            spans=[
                flet.TextSpan("Are you sure you want to "),
                flet.TextSpan(
                    "DELETE",
                    style=flet.TextStyle(weight=flet.FontWeight.BOLD, color="red")
                ), flet.TextSpan(" this customer "),
                flet.TextSpan(
                    customer_name,
                    style=flet.TextStyle(weight=flet.FontWeight.BOLD, color="teal")
                ), flet.TextSpan(" ?"),
            ]
        )
        location_error.actions = [
            flet.TextButton("Delete", on_click=show_location_error_customer_delete),
            flet.TextButton("Cancel", on_click=show_location_error_close, autofocus=True),
        ]
        page.open(location_error)

    def show_location_error_customer_delete(e):
        page.close(location_error)
        customer_delete(**kwargs)

    def show_location_error_close(e):
        page.close(location_error)

    location_error = flet.AlertDialog(
        modal=True,
        title=flet.Text("Warning"),
        content=flet.Text("Last rental location does not match the current store.\n"
                          "Data may not be available.\n\n"
                          "Please use 'APage' for inquiries."),
        actions_alignment=flet.MainAxisAlignment.END,
        actions=[
            flet.TextButton("OK", on_click=show_location_error_close_and_connect, autofocus=True),
        ]
    )

    show_location_error_open(None)

def connect(connect_page, **kwargs):
    page = kwargs.get("page")
    customer_name = kwargs.get("customer_name")
    if connect_page == "rental":
        try:
            my_manager = page.session.get("manager")
            if my_manager:
                my_manager.update_main_page(index=0, customer_name=customer_name)
        except Exception as err:
            print(err)
    elif connect_page == "payment":
        try:
            my_manager = page.session.get("manager")
            if my_manager:
                my_manager.update_main_page(index=1, customer_name=customer_name)
        except Exception as err:
            print(err)