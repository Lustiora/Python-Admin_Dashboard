from menu.menu_search_customer import *
from menu.menu_search_inventory import *
from menu.menu_search_film import *

def view_search_customer(page, store_id, conn):
    customer_id_text, search_id, customer_id = build_customer_id_ui(page, conn) # Module Return Value get
    customer_name_text, search_name, customer_name = build_customer_name_ui(page, store_id, conn)
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Customer Lookup", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("ID :", style=flet.TextThemeStyle.BODY_LARGE, width=200, text_align="right"),
                customer_id_text,
                search_id
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    alignment=flet.alignment.top_left,
                    height=Font.height + 45,
                    content=customer_id,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], alignment=flet.alignment.center),
            flet.Divider(),
            flet.Row([
                flet.Text("Name :", style=flet.TextThemeStyle.BODY_LARGE, width=200, text_align="right"),
                customer_name_text,
                search_name
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    alignment=flet.alignment.top_left,
                    content=customer_name,
                    expand=True,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], expand=True, alignment=flet.alignment.center),
        ]
    )

def view_search_inventory(page, store_id, conn):
    input_inventory_id, btn_search, ui_basic_info, ui_rental_history, ui_current_status = build_inventory_ui(page, store_id, conn)  # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Inventory Search", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("ID :", style=flet.TextThemeStyle.BODY_LARGE, width=100, text_align="right"),
                input_inventory_id,
                btn_search,
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    content=ui_basic_info,
                    alignment=flet.alignment.top_left,
                    height=Font.height + 45,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], alignment=flet.alignment.center),
            flet.Divider(),
            flet.Row([
                flet.Column([
                    flet.Row([flet.Text("Rental Data", width=200, text_align="center", theme_style=flet.TextThemeStyle.TITLE_LARGE, italic=True)],height=40),
                    flet.Divider(),
                    flet.Container(
                        bgcolor=flet.Colors.GREY_200,
                        alignment=flet.alignment.top_left,
                        content=ui_rental_history,
                        expand=True,
                        padding=10,
                        border_radius=5,
                        border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                    )
                ], expand=True),
                flet.Column([
                    flet.Row([flet.Text("Inventory Status", width=200, text_align="center", theme_style=flet.TextThemeStyle.TITLE_LARGE, italic=True)],height=40),
                    flet.Divider(),
                    flet.Container(
                        bgcolor=flet.Colors.GREY_200,
                        alignment=flet.alignment.top_left,
                        content=ui_current_status,
                        expand=True,
                        padding=10,
                        border_radius=5,
                        border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                    )
                ], expand=True),
            ], expand=True, alignment=flet.alignment.top_left)
        ]
    )

def view_search_film(page, conn):
    input_film_title, search_title, ui_film_list = build_film_ui(page, conn)
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Film Catalog Search", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("Title & Description & Actor :", style=flet.TextThemeStyle.BODY_LARGE, width=200, text_align="right"),
                input_film_title,
                search_title
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    alignment=flet.alignment.top_left,
                    content=ui_film_list,
                    expand=True,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], expand=True, alignment=flet.alignment.center),
        ]
    )

def view_search_rental():
    rental = flet.TextField(width=150, height=30, content_padding=10, max_length=10, autofocus=True)
    search = flet.Button("Search", on_click="", width=80,
                        style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Rental Status Lookup", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("ID :", style=flet.TextThemeStyle.BODY_LARGE, width=100, text_align="right"),
                rental,
                search
            ], height=30),
        ]
    )

def view_search_payment():
    payment = flet.TextField(width=150, height=30, content_padding=10, max_length=10, autofocus=True)
    search = flet.Button("Search", on_click="", width=80,
                        style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Payment History Search", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("ID :", style=flet.TextThemeStyle.BODY_LARGE, width=100, text_align="right"),
                payment,
                search
            ], height=30),
        ]
    )
