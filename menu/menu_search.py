from menu.menu_search_customer import *
from menu.menu_search_inventory import *
from menu.menu_search_film import *

def view_search_customer(page, store_id, conn):
    input_customer, search_customer, view_customer = build_customer_ui(page, store_id, conn) # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Customer Lookup", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                input_customer,
                search_customer
            ], height=60),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    alignment=flet.alignment.top_left,
                    expand=True,
                    content=view_customer,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], alignment=flet.alignment.center, expand=True),
        ]
    )

def view_search_inventory(page, store_id, conn):
    input_inventory, search_inventory, view_inventory = build_inventory_ui(page, store_id, conn)  # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Inventory Search", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                input_inventory,
                search_inventory,
            ], height=60),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    content=view_inventory,
                    alignment=flet.alignment.top_left,
                    expand=True,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], alignment=flet.alignment.center, expand=True),
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
                flet.Text("Keyword :",
                          style=flet.TextThemeStyle.BODY_LARGE, width=100, text_align="right"),
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
