from menu.menu_search_customer import *
from menu.menu_search_inventory import *
from menu.menu_search_film import *

def search_customer(page, conn):
    customer_id, search_id, s_c_id = search_customer_id(page, conn) # Module Return Value get
    customer_name, search_name, s_c_name = search_customer_name(page, conn)
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Customer Lookup", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("ID :", style=flet.TextThemeStyle.BODY_LARGE, width=100, text_align="right"),
                customer_id,
                search_id
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    alignment=flet.alignment.top_left,
                    height=Font.height + 45,
                    content=s_c_id,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], alignment=flet.alignment.center),
            flet.Divider(),
            flet.Row([
                flet.Text("Name :", style=flet.TextThemeStyle.BODY_LARGE, width=100, text_align="right"),
                customer_name,
                search_name
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    alignment=flet.alignment.top_left,
                    content=s_c_name,
                    expand=True,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], expand=True, alignment=flet.alignment.center),
        ]
    )

def search_inventory(page, conn):
    inventory, search, s_i_id, s_i_rt, s_i_ti = search_inventory_id(page, conn)  # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Inventory Search", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("ID :", style=flet.TextThemeStyle.BODY_LARGE, width=100, text_align="right"),
                inventory,
                search,
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    content=s_i_id,
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
                        content=s_i_rt,
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
                        content=s_i_ti,
                        expand=True,
                        padding=10,
                        border_radius=5,
                        border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                    )
                ], expand=True),
            ], expand=True, alignment=flet.alignment.top_left)
        ]
    )

def search_film(page, conn):
    film_title, search_title, s_f_title = search_film_title(page, conn)
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Film Catalog Search", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("Title & Description :", style=flet.TextThemeStyle.BODY_LARGE, width=200, text_align="right"),
                film_title,
                search_title
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    alignment=flet.alignment.top_left,
                    content=s_f_title,
                    expand=True,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], expand=True, alignment=flet.alignment.center),
        ]
    )

def search_rental():
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

def search_payment():
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
