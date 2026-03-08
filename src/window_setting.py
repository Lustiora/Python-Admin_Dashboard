import flet

class Font:
    login_ui = 14
    height = login_ui + 8
    big_fontsize = 20

class Ratios:
    # Menu Search Customer
    store = 2
    id = 1
    name = 2
    email = 2
    title = 3
    phone = 2
    address = 2
    date = 2
    last_date = 2
    status = 1
    rate = 1
    total_rate = 2

class Colors:
    border_color = flet.Colors.OUTLINE

    customer_id = flet.Colors.PRIMARY

    status_normal = flet.Colors.ON_SURFACE

    status_returned = flet.Colors.GREEN
    status_normal_btn_color = flet.Colors.ON_SECONDARY_CONTAINER
    status_normal_btn_bgcolor = flet.Colors.SECONDARY_CONTAINER
    status_normal_btn_overlay = flet.Colors.with_opacity(0.12, status_normal_btn_color)

    status_overdue = flet.Colors.ERROR
    status_overdue_btn_color = flet.Colors.ON_ERROR_CONTAINER
    status_overdue_btn_bgcolor = flet.Colors.ERROR_CONTAINER
    status_overdue_btn_overlay = flet.Colors.with_opacity(0.12, status_overdue_btn_color)

    status_unreturned = flet.Colors.PRIMARY
    status_unreturned_btn_color = flet.Colors.ON_PRIMARY_CONTAINER
    status_unreturned_btn_bgcolor = flet.Colors.PRIMARY_CONTAINER
    status_unreturned_btn_overlay = flet.Colors.with_opacity(0.12, status_unreturned_btn_color)

    status_disabled_btn_color = flet.Colors.OUTLINE
    status_disabled_btn_bgcolor = flet.Colors.SURFACE_CONTAINER_HIGHEST

    store_Lethbridge = flet.Colors.ORANGE
    store_Woodridge = flet.Colors.BLUE