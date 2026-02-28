import flet

class Font:
    login_ui = 14
    height = login_ui + 8
    big_fontsize = 20
    status_normal = flet.Colors.BLACK
    status_overdue = flet.Colors.ERROR
    status_unreturned = flet.Colors.BLUE
    status_returned = flet.Colors.GREEN
    status_normal_btn_color = flet.Colors.ON_PRIMARY_CONTAINER
    status_normal_btn_bgcolor = flet.Colors.PRIMARY_CONTAINER
    status_overdue_btn_color = flet.Colors.ON_ERROR_CONTAINER
    status_overdue_btn_bgcolor = flet.Colors.ERROR_CONTAINER
    status_unreturned_btn_color = flet.Colors.ON_TERTIARY_CONTAINER
    status_unreturned_btn_bgcolor = flet.Colors.TERTIARY_CONTAINER

class Ratios:
    # Menu Search Customer
    store = 2
    id = 2
    name = 2
    email = 2
    title = 3
    phone = 2
    address = 2
    date = 2
    last_date = 3
    status = 2
    rate = 2