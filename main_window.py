# -- Import --
import flet, time
from db_monitor import connect_test
from nav_tile import nav
# -- Variable --
# -- Module --
def run_main(page: flet.Page, conn, login_db, login_host, login_port, store_address, staff_user, store_id):
    # -- Frame --
    page.clean()
    page.title = "Sakila"
    page.bgcolor = flet.Colors.BLUE_GREY_50
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
    page.window.prevent_close = True # X 이벤트 옵션 추가
    def close_pop(e):
        e.page.close(main_quit)  # 팝업창 종료 명령어
    def close_main(e):
        page.window.prevent_close = False
        e.page.window.close()
        e.page.window.destroy()
    main_quit = flet.AlertDialog(
        title=flet.Text("Quit"),
        content=flet.Text("Exit?"),
        actions=[flet.TextButton("OK", on_click=close_main),
                 flet.TextButton("Cancel", on_click=close_pop)
                 ], actions_alignment=flet.MainAxisAlignment.END)
    def window_event(e):
        if e.data == "close":
            e.page.open(main_quit)
    page.window.on_event = window_event
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
    ex_tile, basic_content = nav(page, login_db, login_host, login_port, store_address, staff_user, store_id, conn) # Return 값 변수 수거
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