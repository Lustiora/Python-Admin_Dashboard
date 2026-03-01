from class_menu.m_menu import *
from class_menu.search import *
from class_menu.add import *
from class_popup import Popup

def navigation(staff_user, staff_store_address, basic_content, **kwargs):
    page = kwargs["page"]
    def on_nav_change(index):
        if index == 0: # 메인화면
            basic_content.content = view_home()
        elif index == 1.1: # 고객 조회
            basic_content.content = view_search_customer(**kwargs)
        elif index == 1.2: # 재고 조회
            basic_content.content = view_search_inventory(**kwargs)
        elif index == 1.3: # 대여상태 조회
            basic_content.content = view_search_rental(**kwargs)
        elif index == 1.4: # 결제이력 조회
            basic_content.content = view_search_payment(**kwargs)
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
            basic_content.content = view_status(staff_user, staff_store_address)

        basic_content.update()

    ex_tile = flet.Container(
        width=180,
        padding=2,
        border_radius=5,
        content=tile_column(page, on_nav_change)
    )

    return ex_tile, basic_content

def list_tile_menu(title, event, index):
    return flet.ListTile(
        title=flet.Text(title),
        content_padding=flet.padding.only(left=40),
        on_click=lambda e: event(index)
    )

def tile_column(page: flet.Page, on_nav_change):
    popup = Popup(page=page)

    return flet.Column(
        controls=[
            flet.ListTile(
                leading=flet.Icon(flet.Icons.HOME),
                title=flet.Text("Home"),
                on_click=lambda e: on_nav_change(0)
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.SCREEN_SEARCH_DESKTOP_ROUNDED),
                title=flet.Text("Search"),
                controls=[
                    list_tile_menu("Customer", on_nav_change, 1.1),
                    list_tile_menu("Inventory", on_nav_change, 1.2),
                    list_tile_menu("Rental", on_nav_change, 1.3),
                    list_tile_menu("Payment", on_nav_change, 1.4),
                ]
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.ADD_BOX),
                title=flet.Text("Add"),
                controls=[
                    list_tile_menu("Customer", on_nav_change, 4.1),
                    list_tile_menu("Inventory", on_nav_change, 4.2),
                    list_tile_menu("Film", on_nav_change, 4.3),
                    list_tile_menu("Actor", on_nav_change, 4.4),
                    list_tile_menu("Category", on_nav_change, 4.5),
                ]
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
