import flet
from window import Font

def search_customer():
    customer = flet.TextField(width=150, height=30, content_padding=10, max_length=10, autofocus=True)
    lastname = flet.TextField(width=150, height=30, content_padding=10, max_length=10)
    search = flet.Button(
        "Search", on_click="", width=80, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    sc = flet.DataTable(
        columns=[
            flet.DataColumn(flet.Text("ID")),
            flet.DataColumn(flet.Text("Create Date")),
            flet.DataColumn(flet.Text("First Name")),
            flet.DataColumn(flet.Text("Last Name")),
            flet.DataColumn(flet.Text("Email",width=150)),
            flet.DataColumn(flet.Text("Address",width=250)),
        ],
        rows=[],
        border=flet.border.all(1, "flet.Colors.BLUE_GREY_100"), # DataTable Titlebar
        vertical_lines=flet.border.all(1, "flet.Colors.BLUE_GREY_100"), # DataTable Titlebar
        horizontal_lines=flet.border.all(1, "flet.Colors.BLUE_GREY_100"), # DataTable Titlebar
        heading_row_color=flet.Colors.GREY_300, # DataTable Titlebar Inside Color
        heading_row_height=Font.height+4, # DataTable Titlebar Height
        data_row_min_height=Font.height, # DataTable Data Min Height
        data_row_max_height=Font.height, # DataTable Data Max Height
    )
    s_c_r = flet.Column(
        controls=[
            flet.Row([sc], scroll=flet.ScrollMode.ALWAYS)
        ],scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Customer Lookup", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("Customer ID :", style=flet.TextThemeStyle.BODY_LARGE),
                customer,
                search
            ], height=30),
            flet.Divider(),
            flet.Column([
                flet.Container(
                    bgcolor=flet.Colors.GREY_200,
                    content=s_c_r,
                    expand=True,
                    padding=10,
                    border_radius=5,
                    border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
                )
            ],expand=True, alignment=flet.alignment.center)
        ]
    )

def search_inventory():
    inventory = flet.TextField(width=150, height=30, content_padding=10, max_length=10, autofocus=True)
    search = flet.Button("Search", on_click="", width=80,
                        style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Inventory Search", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("Inventory :", style=flet.TextThemeStyle.BODY_LARGE),
                inventory,
                search
            ], height=30),
        ]
    )

def search_film():
    film = flet.TextField(width=150, height=30, content_padding=10, max_length=10, autofocus=True)
    search = flet.Button("Search", on_click="", width=80,
                        style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Film Catalog Search", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([
                flet.Text("Film :", style=flet.TextThemeStyle.BODY_LARGE),
                film,
                search
            ], height=30),
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
                flet.Text("Rental :", style=flet.TextThemeStyle.BODY_LARGE),
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
                flet.Text("Payment :", style=flet.TextThemeStyle.BODY_LARGE),
                payment,
                search
            ], height=30),
        ]
    )
