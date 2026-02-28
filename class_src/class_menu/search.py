import flet
from .search_customer_ui import build_customer_ui
from .menu_search_inventory import build_inventory_ui
from .search_rental_ui import build_rental_ui
from .search_payment_ui import build_payment_ui

def view_container(view_content):
    return flet.Container(
        alignment=flet.alignment.top_left,
        expand=True,
        content=flet.SelectionArea(content=view_content),
        border_radius=5,
        border=flet.border.all(color=flet.Colors.BLACK),
    )

def view_search_customer(**kwargs):
    input_customer, view_customer = build_customer_ui(**kwargs) # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Customer Lookup", style=flet.TextThemeStyle.TITLE_LARGE,
                          weight=flet.FontWeight.BOLD)], height=40),
            flet.Divider(),
            flet.Row([input_customer], height=60),
            flet.Column([
                view_container(view_customer)
            ], alignment=flet.alignment.center, expand=True),
        ], spacing=20
    )

def view_search_inventory(**kwargs):
    input_inventory, view_inventory = build_inventory_ui(**kwargs)  # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Inventory Search", style=flet.TextThemeStyle.TITLE_LARGE,
                          weight=flet.FontWeight.BOLD)], height=40),
            flet.Divider(),
            flet.Row([input_inventory,], height=60),
            flet.Column([
                view_container(view_inventory)
            ], alignment=flet.alignment.center, expand=True),
        ], spacing=20
    )

def view_search_rental(customer_name=None, **kwargs):
    total_rentals, overdue, due_today, input_rental, view_rental = build_rental_ui(customer_name, **kwargs)
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Rental Status Overview", style=flet.TextThemeStyle.TITLE_LARGE,
                          weight=flet.FontWeight.BOLD)], height=40),
            flet.Divider(),
            flet.Row([total_rentals, overdue, due_today], spacing=20),
            flet.Row([input_rental, ], height=60),
            flet.Column([
                view_container(view_rental)
            ], alignment=flet.alignment.center, expand=True),
        ], spacing=20
    )

def view_search_payment(customer_name=None, **kwargs):
    input_payment, view_payment, receipt_details = build_payment_ui(customer_name, **kwargs)
    return flet.Row([
        flet.Column(
            controls=[
                flet.Row([
                    flet.Text("Payment History Search", style=flet.TextThemeStyle.TITLE_LARGE,
                              weight=flet.FontWeight.BOLD)], height=40),
                flet.Divider(),
                flet.Row([input_payment, ], height=60),
                flet.Column([
                    view_container(view_payment)
                ], alignment=flet.alignment.center, expand=True)
            ], expand=5, spacing=20
        ),
        receipt_details
    ], spacing=20)
