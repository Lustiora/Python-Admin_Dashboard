# -- Import --
import flet
from db_monitor import connect_test
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
    page.update()
    page.window.resizable = True
    page.window.min_width = page.window.width
    page.window.min_height = page.window.height
    page.vertical_alignment = flet.MainAxisAlignment.START
    page.window.center()
    # -- Exit --
    page.window.prevent_close = True # X 이벤트 옵션 추가
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
    # -- Menubar --
    # page.add(menu_bar())
    # -- Statusbar --
    status = flet.Text(value="status")
    connect_test(conn, status, page)
    page.add(flet.Container(
        content=status,
        expand=True,
        alignment=flet.Alignment(1,1)))
    # -- Update --
    page.update()
# -- Run Test --
# flet.app(target=main_window)