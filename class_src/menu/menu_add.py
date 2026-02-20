import flet

def view_add_customer():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Register New Customer", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_add_inventory():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Add New Stock", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_add_film():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Register New Film", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_add_actor():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Register New Actor", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_add_category():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Add New Category", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )
