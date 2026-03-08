import flet
from menu.customer_status import customer, customer_delete
from window_setting import Colors

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
    customer_name = kwargs.get("customer_name")

    def show_warning_popup_open(e):
        if connect_page == "delete":
            delete_popup()
        elif connect_page == "edit":
            customer("edit", **kwargs)
        else:
            connect(connect_page, **kwargs)

    def show_close_and_connect(e):
        page.close(warning_popup)
        connect(connect_page, **kwargs)

    def delete_popup():
        warning_popup.icon = flet.Icon(
            flet.Icons.WARNING, color=flet.Colors.AMBER_700, size=30, shadows=flet.BoxShadow(
                spread_radius=2, blur_radius=2, color=flet.Colors.BLACK))
        warning_popup.content = flet.Text(
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
        warning_popup.actions = [
            flet.TextButton("Delete", on_click=show_warning_popup_customer_delete),
            flet.TextButton("Cancel", on_click=show_warning_popup_close, autofocus=True),
        ]
        page.open(warning_popup)

    def show_warning_popup_customer_delete(e):
        page.close(warning_popup)
        customer_delete(**kwargs)

    def show_warning_popup_close(e):
        page.close(warning_popup)

    warning_popup = flet.AlertDialog(
        modal=True,
        title=flet.Text("Warning"),
        actions_alignment=flet.MainAxisAlignment.END,
        actions=[
            flet.TextButton("OK", on_click=show_close_and_connect, autofocus=True),
        ]
    )

    show_warning_popup_open(None)

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