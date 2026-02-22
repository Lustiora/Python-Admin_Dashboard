import flet

def view_delete_customer():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Delete Customer Account", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_delete_inventory():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Remove Inventory Item", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_delete_film():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Delete Film Record", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_delete_rental():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Delete Rental Log", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )

def view_delete_payment():
    return flet.Column(
        controls=[
            flet.Row([
                flet.Text("Void Payment Transaction", style=flet.TextThemeStyle.DISPLAY_MEDIUM, italic=True)
            ], height=80),
            flet.Divider(),
            flet.Row([flet.Text("Database :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Host :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Port :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
            flet.Row([flet.Text("Staff :", style=flet.TextThemeStyle.BODY_LARGE), ], height=30),
        ]
    )
