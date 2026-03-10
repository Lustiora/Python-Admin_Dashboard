import flet
from .search_customer_ui import build_customer_ui
from .search_inventory_ui import build_inventory_ui
from .search_returns_ui import build_rental_ui
from .search_payment_ui import build_payment_ui
from material import view_container

def view_search_customer(customer_name=None, **kwargs):
    input_customer, view_customer, export_btn = build_customer_ui(customer_name, **kwargs) # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Customer Lookup", style=flet.TextThemeStyle.TITLE_LARGE,
                          weight=flet.FontWeight.BOLD)], height=40),
            flet.Divider(),
            flet.Row([input_customer], height=60),
            flet.Column([
                view_container(view_customer),
                flet.Row([export_btn], alignment=flet.MainAxisAlignment.END),
            ], expand=True),
        ], spacing=20
    )

def view_search_inventory(**kwargs):
    input_inventory, view_inventory, export_btn = build_inventory_ui(**kwargs)  # Module Return Value get
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Inventory Search", style=flet.TextThemeStyle.TITLE_LARGE,
                          weight=flet.FontWeight.BOLD)], height=40),
            flet.Divider(),
            flet.Row([input_inventory,], height=60),
            flet.Column([view_container(view_inventory),
                flet.Row([export_btn], alignment=flet.MainAxisAlignment.END),], expand=True),
        ], spacing=20
    )

def view_search_rental(page_index=None, rental_id=None, customer_name=None, **kwargs):
    total_rentals, overdue, due_today, input_rental, view_rental, rental_history, export_btn = build_rental_ui(page_index, rental_id, customer_name, **kwargs)
    return flet.Row([
        flet.Column(
            controls=[
                flet.Row([
                    flet.Text("Rental Status Overview", style=flet.TextThemeStyle.TITLE_LARGE,
                              weight=flet.FontWeight.BOLD),
                ], height=40, spacing=10),
                flet.Divider(),
                flet.Row([total_rentals, overdue, due_today], spacing=20),
                flet.Row([input_rental, ], height=60),
                flet.Column([view_container(view_rental),
                flet.Row([export_btn], alignment=flet.MainAxisAlignment.END),], expand=True),
            ], expand=5, spacing=20
        ),
        rental_history
    ], spacing=20)

def view_search_payment(customer_name=None, **kwargs):
    input_payment, view_payment, receipt_details, export_btn = build_payment_ui(customer_name, **kwargs)
    return flet.Row([
        flet.Column(
            controls=[
                flet.Row([
                    flet.Text("Payment History Search", style=flet.TextThemeStyle.TITLE_LARGE,
                              weight=flet.FontWeight.BOLD)
                ], height=40, spacing=10),
                flet.Divider(),
                flet.Row([input_payment, ], height=60),
                flet.Column([view_container(view_payment),
                flet.Row([export_btn], alignment=flet.MainAxisAlignment.END),], expand=True),
            ], expand=5, spacing=20
        ),
        receipt_details
    ], spacing=20)
