import flet

logo_src = "/logo.png"
welcome_text = "Welcome to the Sakila Management System"
project_text = """
Get started by navigating through the sidebar class_menu on the left. \
You can quickly look up customer records, check real-time stock levels, or process new rentals. \
If you need to update system configurations or view staff details, please visit the Manager section. \
Your efficient workflow starts here.
"""

def view_home():
    return flet.Container(
        margin=flet.padding.all(10),
        content=flet.Row([
            flet.Image(src=logo_src, width=200, height=200),
            flet.Column([
                flet.Text(
                    value=welcome_text,
                    style=flet.TextThemeStyle.BODY_LARGE,
                    size=30,
                    italic=True,
                    weight=flet.FontWeight.BOLD,
                    text_align=flet.TextAlign.CENTER,
                    width=650,
                ),flet.Text(
                    value=project_text,
                    color=flet.Colors.GREY_700,
                    style=flet.TextThemeStyle.BODY_LARGE,
                    text_align=flet.TextAlign.JUSTIFY,
                    size=16,
                    width=650,
                )
            ],alignment=flet.MainAxisAlignment.CENTER)
        ],alignment=flet.MainAxisAlignment.CENTER,)
    )

def view_status(staff_user, staff_store_address):
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("System Dashboard", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Container(height=7),
            flet.Row([
                flet.Container(
                    bgcolor=flet.Colors.BLUE_GREY_100,
                    border_radius=10,
                    alignment=flet.alignment.center,
                    width=280,
                    height=250,
                    content=flet.Column([
                        flet.Text("Connect Status",
                                  size=20,
                                  style=flet.TextThemeStyle.BODY_LARGE,
                                  italic=True),
                        flet.Divider(),
                        flet.Row([
                            flet.Column([
                                flet.Text("Store :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Staff :", style=flet.TextThemeStyle.BODY_MEDIUM)
                            ], horizontal_alignment=flet.CrossAxisAlignment.END
                            ),flet.Column([
                                flet.Text(
                                    value=staff_store_address, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(
                                    value=staff_user, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD)
                            ])
                        ], alignment=flet.MainAxisAlignment.CENTER)
                    ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, alignment=flet.MainAxisAlignment.CENTER)
                ),flet.Container(
                    width=40
                ),flet.Container(
                    bgcolor=flet.Colors.BLUE_GREY_100,
                    border_radius=10,
                    alignment=flet.alignment.center,
                    width=280,
                    height=250,
                    content=flet.Column([
                        flet.Text("Connect Status",
                                  size=20,
                                  style=flet.TextThemeStyle.BODY_LARGE,
                                  italic=True),
                        flet.Divider(),
                        flet.Row([
                            flet.Column([
                                flet.Text("Store :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Staff :", style=flet.TextThemeStyle.BODY_MEDIUM)
                            ], horizontal_alignment=flet.CrossAxisAlignment.END
                            ),flet.Column([
                                flet.Text(
                                    value=staff_store_address, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(
                                    value=staff_user, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD)
                            ])
                        ], alignment=flet.MainAxisAlignment.CENTER)
                    ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, alignment=flet.MainAxisAlignment.CENTER)
                )
            ])
        ]
    )

def view_statistic():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Business Analytics", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_manager():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Admin Management", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )