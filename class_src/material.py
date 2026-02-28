import flet
from class_window import Font, Ratios

def input_text(content=None, on_submit=None, hint_text=None, value=None, autofocus=True):
    return flet.TextField(label=content, on_submit=on_submit, hint_text=hint_text, value=value,
       text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=autofocus
    )

def header_text(content=None, expand=None):
    return flet.Text(
        content, expand=expand, text_align="center", no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS,
    )

def data_text(content=None, expand=None, color=None, max_lines=None, text_align="center"):
    return flet.Text(
        content, expand=expand, text_align=text_align,
        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=content, color=color, max_lines=max_lines
    )

def context_menu(content, disabled=False, height=35, color=flet.Colors.BLACK, weight=None, alignment=flet.alignment.center_left, icon=None, on_click=None):
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

    def show_location_error_open(e):
        page.open(location_error)

    def show_location_error_close(e):
        page.close(location_error)
        connect(connect_page, **kwargs)

    location_error = flet.AlertDialog(
        modal=True,
        title=flet.Text("Warning"),
        content=flet.Text("Last rental location does not match the current store.\n"
                          "Data may not be available.\n\n"
                          "Please use 'APage' for inquiries."),
        actions_alignment=flet.MainAxisAlignment.END,
        actions=[
            flet.TextButton("OK", on_click=show_location_error_close, autofocus=True),
        ]
    )

    if staff_store_id != customer_last_rental_store_id:
        show_location_error_open(None)
    else:
        connect(connect_page, **kwargs)

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