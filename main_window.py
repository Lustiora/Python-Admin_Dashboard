# -- Import --
import flet
from db_monitor import connect_test
from nav_tile import nav
# -- Variable --
staff_user = None
staff_store = None
# -- Module --
def staff_user_id(user_id, store):
    global staff_user
    global staff_store
    staff_store = store
    staff_user = user_id
    return staff_user, staff_store
def run_main(page: flet.Page, conn):
    # -- Frame --
    page.title = "Sakila"
    page.window.width = 1024
    page.window.height = 768
    page.bgcolor = flet.Colors.BLUE_GREY_50
    page.update()
    page.window.resizable = True
    page.window.min_width = page.window.width
    page.window.min_height = page.window.height
    page.vertical_alignment = flet.MainAxisAlignment.START
    page.window.center()
    # -- Exit --
    page.window.prevent_close = True # X 이벤트 옵션 추가
    def close_pop_open(e):
        e.page.open(main_quit)
    def close_pop(e):
        e.page.close(main_quit)  # 팝업창 종료 명령어
    def close_main(e):
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
        content=flet.Text(value="status"),
        alignment=flet.Alignment(1, 1),
        height=24,
        padding=2,
        border_radius=5,
        bgcolor=flet.Colors.OUTLINE
    )
    # -- Main Area --
    ex_tile, basic_content = nav(page) # Return 값 변수 수거
    # -- Page --
    page.add(
        flet.Row([ex_tile, flet.VerticalDivider(width=1),
                  flet.Column([basic_content, con_status],expand=True)]
        , expand=True)
    )
    connect_test(conn, con_status, page)
    # -- Update --
    page.update()
# -- Run Test --
# flet.app(target=main_window)