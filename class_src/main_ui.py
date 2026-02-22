# -- Import --
import flet, time
from monitoring import connect_test
from class_popup import Popup
from navigation_tile import navigation

# -- Module --
def run_main(page: flet.Page, conn, login_db, login_host, login_port, staff_user, staff_store_address, staff_store_id):
    popup = Popup(page=page)

    # -- Frame --
    page.clean()
    page.title = "Sakila"
    page.vertical_alignment = flet.MainAxisAlignment.START
    page.window.resizable = True
    page.window.width = 1280
    page.window.height = 720
    page.window.min_width = page.window.width
    page.window.min_height = page.window.height
    page.window.center()
    time.sleep(0.1) # Loading Time Force : 옵션 적용 전 시작 방지
    page.update()

    # -- Exit --
    page.window.prevent_close = True
    page.window.on_event = popup.show_open

    # -- Statusbar --
    con_status = flet.Container(
        content=flet.Text(value="status "),
        alignment=flet.Alignment(1, 1),
        height=24,
        padding=2,
        border_radius=5,
        bgcolor=flet.Colors.OUTLINE
    )

    # -- Main Area --
    ex_tile, basic_content = navigation(
        page, conn, login_db, login_host, login_port, staff_user, staff_store_address, staff_store_id
    )
    # -- Page --
    page.add(
        flet.Row([
            flet.Column([ex_tile
                ],scroll=flet.ScrollMode.AUTO, alignment=flet.MainAxisAlignment.START),
            flet.VerticalDivider(width=1),
            flet.Column([basic_content, con_status],expand=True),
                ], expand=True, vertical_alignment=flet.CrossAxisAlignment.START
        )
    )
    connect_test(conn, con_status, page)

    # -- Update --
    page.update()