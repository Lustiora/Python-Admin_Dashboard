from menu.menu_ui import *
from menu.search import *
from menu.add import *
from menu.customer_status import customer
from menu.rent import view_rent
from window_popup import Popup
from material import list_tile, list_tile_menu

def navigation(basic_content, **kwargs):
    page = kwargs["page"]
    def on_nav_change(index):
        if index == 0: # 메인화면
            basic_content.content = view_home(**kwargs)
        elif index == 0.1: # 고객 조회
            basic_content.content = view_rent(**kwargs)
        elif index == 1.1: # 고객 조회
            basic_content.content = view_search_customer(**kwargs)
        elif index == 1.2: # 재고 조회
            basic_content.content = view_search_inventory(**kwargs)
        elif index == 1.3: # 대여상태 조회
            basic_content.content = view_search_rental(**kwargs)
        elif index == 1.4: # 결제이력 조회
            basic_content.content = view_search_payment(**kwargs)
        elif index == 4.1: # 고객 추가
            customer("add",**kwargs)
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
            basic_content.content = view_status(**kwargs)

        basic_content.update()

    ex_tile = flet.Container(
        width=180,
        padding=2,
        border_radius=5,
        content=tile_column(page, on_nav_change)
    )

    return ex_tile, basic_content

def tile_column(page: flet.Page, on_nav_change):
    popup = Popup(page=page)

    return flet.Column(
        controls=[
            list_tile(icon=flet.Icons.HOME, title="Home", event=on_nav_change, index=0),
            list_tile(title="Rent", event=on_nav_change, index=0.1, icon=flet.Icons.MOVIE_FILTER),
            flet.Divider(),
            list_tile(title="Returns", event=on_nav_change, index=1.3, icon=flet.Icons.SHOPPING_CART),
            list_tile(title="Payment", event=on_nav_change, index=1.4, icon=flet.Icons.PAYMENT),
            list_tile(title="Customer", event=on_nav_change, index=1.1, icon=flet.Icons.PEOPLE),
            list_tile(title="Inventory", event=on_nav_change, index=1.2, icon=flet.Icons.INVENTORY),
            # flet.ExpansionTile(
            #     leading=flet.Icon(flet.Icons.SCREEN_SEARCH_DESKTOP_ROUNDED),
            #     title=flet.Text("Search"),
            #     controls=[
            #         list_tile_menu("Customer", on_nav_change, 1.1),
            #         list_tile_menu("Inventory", on_nav_change, 1.2),
            #         list_tile_menu("Rental", on_nav_change, 1.3),
            #         list_tile_menu("Payment", on_nav_change, 1.4),
            # ]),
            flet.Divider(),
            flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.ADD_BOX),
                title=flet.Text("Add"),
                controls=[
                    list_tile_menu("Add Customer", on_nav_change, 4.1),
                    list_tile_menu("Add Inventory", on_nav_change, 4.2),
                    list_tile_menu("Add Film", on_nav_change, 4.3),
                    list_tile_menu("Add Actor", on_nav_change, 4.4),
                    list_tile_menu("Add Category", on_nav_change, 4.5),
                ]),
            list_tile(icon=flet.Icons.QUERY_STATS, title="Statistic", event=on_nav_change, index=5),
            list_tile(icon=flet.Icons.MANAGE_ACCOUNTS, title="Manager", event=on_nav_change, index=6),
            flet.Divider(),
            list_tile(icon=flet.Icons.SIGNAL_CELLULAR_ALT, title="Dashboard", event=on_nav_change, index=7),
            flet.ListTile(
                leading=flet.Icon(flet.Icons.EXIT_TO_APP),
                title=flet.Text("Exit"),
                on_click=lambda e: (setattr(e, "data", "close"), popup.show_open(e))
            )
        ], spacing=0
    )
