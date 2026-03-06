# -- Import --
import flet, time
from monitoring import connect_test
from class_popup import Popup
from navigation_tile import navigation
from class_menu.search import view_search_rental, view_search_customer, view_search_payment
from class_menu.menu_ui import view_home
from class_window import Colors

class MainManager:
    def __init__(self, page: flet.Page, conn, staff_user, staff_store_address, staff_store_id):
        self.page = page
        self.conn = conn
        self.staff_user = staff_user
        self.staff_store_address = staff_store_address
        self.staff_store_id = staff_store_id

        self.page_theme = []
        self.page.theme_mode = flet.ThemeMode.SYSTEM

        # -- Statusbar --
        self.server_status = flet.Text(value="Server Status", text_align=flet.TextAlign.RIGHT)
        self.server_time = flet.Text(value="Server Time", text_align=flet.TextAlign.LEFT)
        self.connect_status = flet.Container(
            content=flet.Row([
                self.server_time, self.server_status
            ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
            height=24,
            alignment=flet.alignment.center_left,
            padding=flet.padding.only(left=10, right=10),
            border_radius=5,
            border=flet.border.all(color=Colors.border_color)
        )

        params = {
            "page": self.page,
            "staff_store_id": self.staff_store_id,
            "conn": self.conn,
            "theme_mode":self.page.theme_mode,
        }

        self.basic_container = flet.Container(
            content=view_home(**params),
            alignment=flet.alignment.center,
            expand=True,
            border_radius=5,
            padding=20,
        )

        self.theme_switch = flet.Switch(value=True, on_change=self.toggle_theme)
        self.select_theme = flet.Icon(name=flet.Icons.LIGHT_MODE_OUTLINED)

        self.ex_tile = navigation(
            self.staff_user, self.staff_store_address, self.basic_container, **params)[0]

        self.basic_content = navigation(
            self.staff_user, self.staff_store_address, self.basic_container, **params)[1]

        self.content = flet.Column([self.basic_content, self.connect_status], expand=True)

        self.basic_main_content = flet.Row(
            expand=True,
            vertical_alignment=flet.CrossAxisAlignment.START,
            controls=[
                flet.Column(
                    scroll=flet.ScrollMode.AUTO,
                    horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                    controls=[
                        self.ex_tile,
                        flet.Row(
                            controls=[
                                self.theme_switch, self.select_theme
                        ]),
                ]),
                flet.VerticalDivider(width=1),
                self.content,
            ]
        )

        self.page.add(self.basic_main_content)

        self.page.update()

        self.page.session.set("manager", self)

    def update_main_page(self, index, page_index=None, customer_name=None, rental_id=None):
        params = {
            "page": self.page,
            "conn": self.conn,
            "staff_store_id": self.staff_store_id,
        }
        # -- Main Content --
        if index == 0:
            print(f"Page Update 'Rental' {page_index}")
            self.basic_content.content = view_search_rental(page_index, rental_id, customer_name, **params)
            self.basic_content.update()
        elif index == 1:
            print("Page Update 'Payment'")
            self.basic_content.content = view_search_payment(customer_name, **params)
            self.basic_content.update()
        elif index == 2:
            print("Page Update 'Customer'")
            self.basic_content.content = view_search_customer(customer_name, **params)
            self.basic_content.update()

    def toggle_theme(self, e):
        if self.page.theme_mode != flet.ThemeMode.DARK:
            self.page_theme.append(f"{self.page.theme_mode}")
            self.page.theme_mode = flet.ThemeMode.DARK
            self.select_theme.name = flet.Icons.DARK_MODE
        else:
            if self.page_theme:
                self.page.theme_mode = self.page_theme[0]
                self.select_theme.name = flet.Icons.LIGHT_MODE_OUTLINED
                self.page_theme.clear()
            else:
                return
        if self.page:
            self.page.update()

# -- Module --
def run_main(page: flet.Page, conn, staff_user, staff_store_address, staff_store_id):
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
    time.sleep(0.1)  # Loading Time Force : 옵션 적용 전 시작 방지
    page.update()

    # -- Exit --
    page.window.prevent_close = True
    page.window.on_event = popup.show_open

    # -- Page --
    main_handler = MainManager(page=page, conn=conn, staff_user=staff_user,
                               staff_store_address=staff_store_address, staff_store_id=staff_store_id)
    connect_test(conn, main_handler.server_status, main_handler.server_time, main_handler.connect_status, page)