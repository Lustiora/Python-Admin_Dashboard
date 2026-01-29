from menu.menu import *
from menu.menu_search import *
from menu.menu_edit import *
from menu.menu_delete import *
from menu.menu_add import *

def nav(page: flet.Page, login_db, login_host, login_port, store_address, staff_user, store_id, conn):
    basic_content = flet.Container(
        content=c_home(),
        alignment=flet.alignment.center,
        expand=True,
        border_radius=5,
        padding=20
    )
    def close_pop_open(e):
        page.open(main_quit)
    def close_pop(e):
        page.close(main_quit)  # 팝업창 종료 명령어
    def close_main(e):
        page.window.prevent_close = False
        page.window.close()
        page.window.destroy()
    main_quit = flet.AlertDialog(
        title=flet.Text("Quit"),
        content=flet.Text("Exit?"),
        actions=[flet.TextButton("OK", on_click=close_main),
                 flet.TextButton("Cancel", on_click=close_pop)
                 ], actions_alignment=flet.MainAxisAlignment.END)
    def on_nav_change(index):
        if index == 0: # 메인화면
            basic_content.content = c_home()
        elif index == 1.1: # 고객 조회
            basic_content.content = search_customer(page, store_id, conn)
        elif index == 1.2: # 재고 조회
            basic_content.content = search_inventory(page, conn)
        elif index == 1.3: # 영화 조회
            basic_content.content = search_film(page, conn)
        elif index == 1.4: # 대여상태 조회
            basic_content.content = search_rental()
        elif index == 1.5: # 결제이력 조회
            basic_content.content = search_payment()
        elif index == 2.1: # 고객정보 변경
            basic_content.content = edit_customer()
        elif index == 2.2: # 재고정보 변경
            basic_content.content = edit_inventory()
        elif index == 2.3: # 영화정보 변경
            basic_content.content = edit_film()
        elif index == 2.4: # 대여상태 변경
            basic_content.content = edit_rental()
        elif index == 2.5: # 결제상태 변경
            basic_content.content = edit_payment()
        elif index == 3.1: # 고객 삭제
            basic_content.content = delete_customer()
        elif index == 3.2: # 재고 삭제
            basic_content.content = delete_inventory()
        elif index == 3.3: # 영화 삭제
            basic_content.content = delete_film()
        elif index == 3.4: # 대여이력 삭제
            basic_content.content = delete_rental()
        elif index == 3.5: # 결제이력 삭제
            basic_content.content = delete_payment()
        elif index == 4.1: # 고객 추가
            basic_content.content = add_customer()
        elif index == 4.2: # 재고 추가
            basic_content.content = add_inventory()
        elif index == 4.3: # 영화 추가
            basic_content.content = add_film()
        elif index == 4.4: # 배우 추가
            basic_content.content = add_actor()
        elif index == 4.5: # 장르 추가
            basic_content.content = add_category()
        elif index == 5: # 통계
            basic_content.content = c_statistic()
        elif index == 6: # 관리
            basic_content.content = c_manager()
        elif index == 7: # 접속 상태
            basic_content.content = c_status(login_db, login_host, login_port, store_address, staff_user)

        basic_content.update()
    tile_column = flet.Column(
        controls=[
            flet.ListTile(
                leading=flet.Icon(flet.Icons.HOME),
                title=flet.Text("Home"),
                on_click=lambda e: on_nav_change(0)
            ),flet.Divider(
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.SCREEN_SEARCH_DESKTOP_ROUNDED),
                title=flet.Text("Search"),
                bgcolor=flet.Colors.BLUE_GREY_200,
                controls=[
                    flet.ListTile(
                        title=flet.Text("Customer"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.1)
                    ),flet.ListTile(
                        title=flet.Text("Inventory"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.2)
                    ),flet.ListTile(
                        title=flet.Text("Film"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.3)
                    ),flet.ListTile(
                        title=flet.Text("Rental"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.4)
                    ),flet.ListTile(
                        title=flet.Text("Payment"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.5)
                    ),
                ]
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.ADD_BOX),
                title=flet.Text("Add"),
                bgcolor=flet.Colors.BLUE_GREY_200,
                controls=[
                    flet.ListTile(
                        title=flet.Text("Customer"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.1)
                    ),flet.ListTile(
                        title=flet.Text("Inventory"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.2)
                    ),flet.ListTile(
                        title=flet.Text("Film"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.3)
                    ),flet.ListTile(
                        title=flet.Text("Actor"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.4)
                    ),flet.ListTile(
                        title=flet.Text("Category"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.5)
                    ),
                ]
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.CHANGE_CIRCLE),
                title=flet.Text("Edit"),
                bgcolor=flet.Colors.BLUE_GREY_200,
                controls=[
                    flet.ListTile(
                        title=flet.Text("Customer"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.1)
                    ),flet.ListTile(
                        title=flet.Text("Inventory"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.2)
                    ),flet.ListTile(
                        title=flet.Text("Film"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.3)
                    ),flet.ListTile(
                        title=flet.Text("Rental"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.4)
                    ),flet.ListTile(
                        title=flet.Text("Payment"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.5)
                    ),
                ]
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.DELETE),
                title=flet.Text("Delete"),
                bgcolor=flet.Colors.BLUE_GREY_200,
                controls=[
                    flet.ListTile(
                        title=flet.Text("Customer"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.1)
                    ),flet.ListTile(
                        title=flet.Text("Inventory"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.2)
                    ),flet.ListTile(
                        title=flet.Text("Film"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.3)
                    ),flet.ListTile(
                        title=flet.Text("Rental"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.4)
                    ),flet.ListTile(
                        title=flet.Text("Payment"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.5)
                    ),
                ]
            ),flet.Divider(
            ),flet.ListTile(
                leading=flet.Icon(flet.Icons.QUERY_STATS),
                title=flet.Text("Statistic"),
                on_click=lambda e: on_nav_change(5)
            ),flet.ListTile(
                leading=flet.Icon(flet.Icons.MANAGE_ACCOUNTS),
                title=flet.Text("Manager"),
                on_click=lambda e: on_nav_change(6)
            ),flet.Divider(
            ),flet.ListTile(
                leading=flet.Icon(flet.Icons.SIGNAL_CELLULAR_ALT),
                title=flet.Text("Dashboard"),
                on_click=lambda e: on_nav_change(7)
            ),flet.ListTile(
                leading=flet.Icon(flet.Icons.EXIT_TO_APP),
                title=flet.Text("Exit"),
                on_click=close_pop_open
            )
        ]
    )
    ex_tile = flet.Container(
        width=180,
        bgcolor=flet.Colors.BLUE_GREY_100,
        padding=2,
        border_radius=5,
        content=tile_column
    )
    return ex_tile, basic_content