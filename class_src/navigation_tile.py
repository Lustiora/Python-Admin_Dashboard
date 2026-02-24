from class_menu.m_menu import *
from class_menu.search import *
from class_menu.edit import *
from class_menu.delete import *
from class_menu.add import *
from class_popup import Popup

def navigation(page: flet.Page, conn, login_db, login_host, login_port, staff_user, staff_store_address, staff_store_id):
    popup = Popup(page=page)
    basic_content = flet.Container(
        content=view_search_payment(page, staff_store_id, conn),
        alignment=flet.alignment.center,
        expand=True,
        border_radius=5,
        padding=20
    )
    def on_nav_change(index):
        if index == 0: # 메인화면
            basic_content.content = view_home()
        elif index == 1.1: # 고객 조회
            basic_content.content = view_search_customer(page, staff_store_id, conn)
        elif index == 1.2: # 재고 조회
            basic_content.content = view_search_inventory(page, staff_store_id, conn)
        elif index == 1.3: # 대여상태 조회
            basic_content.content = view_search_rental(page, staff_store_id, conn)
        elif index == 1.4: # 결제이력 조회
            basic_content.content = view_search_payment(page, staff_store_id, conn)
        elif index == 2.1: # 고객정보 변경
            basic_content.content = view_edit_customer()
        elif index == 2.2: # 재고정보 변경
            basic_content.content = view_edit_inventory()
        elif index == 2.3: # 영화정보 변경
            basic_content.content = view_edit_film()
        elif index == 2.4: # 대여상태 변경
            basic_content.content = view_edit_rental()
        elif index == 2.5: # 결제상태 변경
            basic_content.content = view_edit_payment()
        elif index == 3.1: # 고객 삭제
            basic_content.content = view_delete_customer()
        elif index == 3.2: # 재고 삭제
            basic_content.content = view_delete_inventory()
        elif index == 3.3: # 영화 삭제
            basic_content.content = view_delete_film()
        elif index == 3.4: # 대여이력 삭제
            basic_content.content = view_delete_rental()
        elif index == 3.5: # 결제이력 삭제
            basic_content.content = view_delete_payment()
        elif index == 4.1: # 고객 추가
            basic_content.content = view_add_customer()
        elif index == 4.2: # 재고 추가
            basic_content.content = view_add_inventory()
        elif index == 4.3: # 영화 추가
            basic_content.content = view_add_film()
        elif index == 4.4: # 배우 추가
            basic_content.content = view_add_actor()
        elif index == 4.5: # 장르 추가
            basic_content.content = view_add_category()
        elif index == 5: # 통계
            basic_content.content = view_statistic()
        elif index == 6: # 관리
            basic_content.content = view_manager()
        elif index == 7: # 접속 상태
            basic_content.content = view_status(login_db, login_host, login_port, staff_store_address, staff_user)

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
                        title=flet.Text("Rental"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.3)
                    ),flet.ListTile(
                        title=flet.Text("Payment"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.4)
                    ),
                ]
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.ADD_BOX),
                title=flet.Text("Add"),
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
                on_click=lambda e: (setattr(e, "data", "close"), popup.show_open(e))
            )
        ]
    )
    ex_tile = flet.Container(
        width=180,
        padding=2,
        border_radius=5,
        content=tile_column
    )
    return ex_tile, basic_content