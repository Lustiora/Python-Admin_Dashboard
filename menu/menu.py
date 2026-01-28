import flet

def c_home():
    return flet.Column(
        alignment=flet.MainAxisAlignment.CENTER,
        controls=[
            flet.Row([
                flet.Row([
                    flet.Image(src="/logo.png",width=200,height=200),
                    flet.Container(
                        margin=flet.margin.only(left=20),
                        content=flet.Column([
                            flet.Row([
                                flet.Text(
                                    "Welcome to the Sakila Management System", # Title
                                    style=flet.TextThemeStyle.BODY_LARGE,
                                    size=30,
                                    italic=True,
                                    weight=flet.FontWeight.BOLD),
                            ], height=50),
                            flet.Row([
                                flet.Text(
                                    "Get started by navigating through the sidebar menu on the left. " # Body
                                    "You can quickly look up customer records, check real-time stock levels, or process new rentals. "
                                    "If you need to update system configurations or view staff details, please visit the Manager section. "
                                    "Your efficient workflow starts here.",
                                    color=flet.Colors.GREY_700,
                                    style=flet.TextThemeStyle.BODY_LARGE,
                                    width=650,
                                    text_align=flet.TextAlign.JUSTIFY,
                                    size=16
                                    ),
                                ]),
                        ],)
                    )
                ], vertical_alignment=flet.CrossAxisAlignment.START)
            ], alignment=flet.MainAxisAlignment.CENTER,)
        ]
    )

def c_status(login_db, login_host, login_port, staff_store, staff_user):
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
                                flet.Text("Database :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Host :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Port :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Store :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Staff :", style=flet.TextThemeStyle.BODY_MEDIUM)
                            ], horizontal_alignment=flet.CrossAxisAlignment.END
                            ),flet.Column([
                                flet.Text(value=login_db, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(value=login_host, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(value=login_port, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(value=staff_store, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(value=staff_user, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD)
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
                                flet.Text("Database :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Host :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Port :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Store :", style=flet.TextThemeStyle.BODY_MEDIUM),
                                flet.Text("Staff :", style=flet.TextThemeStyle.BODY_MEDIUM)
                            ], horizontal_alignment=flet.CrossAxisAlignment.END
                            ),flet.Column([
                                flet.Text(value=login_db, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(value=login_host, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(value=login_port, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(value=staff_store, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD),
                                flet.Text(value=staff_user, style=flet.TextThemeStyle.BODY_MEDIUM, weight=flet.FontWeight.BOLD)
                            ])
                        ], alignment=flet.MainAxisAlignment.CENTER)
                    ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, alignment=flet.MainAxisAlignment.CENTER)
                )
            ])
        ]
    )

def c_statistic():
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

def c_manager():
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