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
    # -- Main Area --
    basic_content = flet.Container(
        content=flet.Text("Welcome Sakila"),
        alignment=flet.alignment.center,
        expand=True,
        border_radius=5,
        bgcolor=flet.Colors.AMBER_100
    )
    def toggle_rail(e):
        rail.extended = not rail.extended
        page.update()
    def on_nav_change(e):
        index = e.control.selected_index
        print(index)
        if index == 0:
            basic_content.content.value = "메뉴"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.PURPLE
        elif index == 1:
            basic_content.content.value = "조회"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BLUE
        elif index == 2:
            basic_content.content.value = "변경"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BROWN_500
        elif index == 3:
            basic_content.content.value = "삭제"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.YELLOW_200
        elif index == 4:
            basic_content.content.value = "추가"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.LIGHT_BLUE_100
        elif index == 5:
            basic_content.content.value = "통계"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.DEEP_ORANGE_200
        elif index == 6:
            basic_content.content.value = "관리"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.CYAN_400
        basic_content.update()

    rail = flet.NavigationRail(
        selected_index=0,
        label_type=flet.NavigationRailLabelType.ALL,
        min_width=100,
        group_alignment=-0.9,
        destinations=[
            flet.NavigationRailDestination(
                icon=flet.Icons.MENU,
                selected_icon=flet.Icons.MENU_ROUNDED,
                label="Menu"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.SCREEN_SEARCH_DESKTOP_ROUNDED,
                selected_icon=flet.Icons.SCREEN_SEARCH_DESKTOP_OUTLINED,
                label="Search"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.CHANGE_CIRCLE,
                selected_icon=flet.Icons.CHANGE_CIRCLE_OUTLINED,
                label="Change"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.DELETE,
                selected_icon=flet.Icons.DELETE_OUTLINE,
                label="Delete"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.ADD_BOX,
                selected_icon=flet.Icons.ADD_BOX_OUTLINED,
                label="Add"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.QUERY_STATS,
                selected_icon=flet.Icons.QUERY_STATS_ROUNDED,
                label="Statistic"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.MANAGE_ACCOUNTS,
                selected_icon=flet.Icons.MANAGE_ACCOUNTS_OUTLINED,
                label="Manager"
            )
        ], on_change=on_nav_change,
    )
    # -- Statusbar --
    con_status = flet.Container(
        content=flet.Text(value="status"),
        alignment=flet.Alignment(1, 1),
        height=24,
        padding=2,
        border_radius=5,
        bgcolor=flet.Colors.OUTLINE
    )
    # -- Page --
    page.add(
        flet.Row([rail, flet.VerticalDivider(width=1),
                  flet.Column([basic_content, con_status]
                              ,expand=True)]
                 , expand=True)
    )
    connect_test(conn, con_status, page)
    # -- Update --
    page.update()
# -- Run Test --
# flet.app(target=main_window)