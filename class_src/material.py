import flet
from class_window import Font, Ratios
# from test_main_ui import MainPage

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

def context_customer_id_data(e, page, customer_name, connect_page):
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
    # elif connect_page == "edit":
    #     print(f"{customer_name}, {connect_page} | Edit 21")
    # elif connect_page == "delete":
    #     print(f"{customer_name}, {connect_page} | Delete")
