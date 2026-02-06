import flet

from menu.menu_search_customer import *
from menu.menu_search_inventory import *
from menu.menu_search_rental import *
from menu.menu_search_payment import *

def view_search_customer(page, store_id, conn):
    input_customer, view_customer = build_customer_ui(page, store_id, conn) # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Customer Lookup", style=flet.TextThemeStyle.TITLE_LARGE,
                          weight=flet.FontWeight.BOLD)], height=40),
            flet.Divider(),
            flet.Row([input_customer], height=60),
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
    input_inventory, view_inventory = build_inventory_ui(page, store_id, conn)  # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Inventory Search", style=flet.TextThemeStyle.TITLE_LARGE,
                          weight=flet.FontWeight.BOLD)], height=40),
            flet.Divider(),
            flet.Row([input_inventory,], height=60),
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

def view_search_rental(page, store_id, conn):
    dummy = flet.Container()
    total_rentals, overdue, due_today, input_rental, view_rental = build_rental_ui(page, store_id, conn)
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Rental Status Overview", style=flet.TextThemeStyle.TITLE_LARGE,
                          weight=flet.FontWeight.BOLD)], height=40),
            flet.Divider(),
            flet.Row([total_rentals, dummy, overdue, dummy, due_today]),
            dummy,
            flet.Row([input_rental, ], height=60),
            dummy,
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    content=view_rental,
                    alignment=flet.alignment.top_left,
                    expand=True,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ], alignment=flet.alignment.center, expand=True),
        ]
    )

def view_search_payment():
    input_payment, receipt_details = build_payment_ui()
    return flet.Row([
            flet.Column(
                controls=[
                    flet.Row([
                        flet.Text("Payment History Search", style=flet.TextThemeStyle.TITLE_LARGE,
                                  weight=flet.FontWeight.BOLD)], height=40),
                    flet.Divider(),
                    flet.Row([input_payment, ], height=60),
                ], expand=5
            ),flet.VerticalDivider(width=1),
            flet.Column(
                controls=[
                    flet.Row([
                        flet.Text("Receipt Details", style=flet.TextThemeStyle.TITLE_LARGE,
                                  weight=flet.FontWeight.BOLD)], height=40),
                    flet.Container(
                        bgcolor=flet.Colors.GREY_200,
                        content=receipt_details,
                        expand=True,
                        padding=10,
                        border_radius=5,
                        border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                        width=200
                    ),
                ]
            )
        ], spacing=20
    )
