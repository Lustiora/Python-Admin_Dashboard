# -- Import --
import flet, time
from monitoring import connect_test
from class_popup import Popup
from navigation_tile import navigation
from class_menu.search import view_search_rental, view_search_customer, view_search_payment

class MainManager:
    def __init__(self, page: flet.Page, conn, staff_user, staff_store_address, staff_store_id):
        self.page = page
        self.conn = conn
        self.staff_user = staff_user
        self.staff_store_address = staff_store_address
        self.staff_store_id = staff_store_id

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
            border=flet.border.all(color=flet.Colors.BLACK)
        )

        params = {
            "page": self.page,
            "staff_store_id": self.staff_store_id,
            "conn": self.conn,
        }

        self.basic_container = flet.Container(
            content=view_search_customer(**params),
            alignment=flet.alignment.center,
            expand=True,
            border_radius=5,
            padding=20,
        )

        self.ex_tile = navigation(
            self.staff_user, self.staff_store_address, self.basic_container, **params)[0]

        self.basic_content = navigation(
            self.staff_user, self.staff_store_address, self.basic_container, **params)[1]

        self.content = flet.Column([self.basic_content, self.connect_status], expand=True)

        self.basic_main_content = flet.Row(
            [
                flet.Column([self.ex_tile
                             ], scroll=flet.ScrollMode.AUTO, alignment=flet.MainAxisAlignment.START),
                flet.VerticalDivider(width=1),
                self.content,
            ], expand=True, vertical_alignment=flet.CrossAxisAlignment.START
        )

        self.page.add(self.basic_main_content)

        self.page.update()

        self.page.session.set("manager", self)

    def update_main_page(self, index, customer_name):
        params = {
            "page": self.page,
            "conn": self.conn,
            "staff_store_id": self.staff_store_id,
        }
        # -- Main Content --
        if index == 0:
            print("Page Update 'Rental'")
            self.basic_content.content = view_search_rental(customer_name, **params)
            self.basic_content.update()
        elif index == 1:
            print("Page Update 'Payment'")
            self.basic_content.content = view_search_payment(customer_name, **params)
            self.basic_content.update()
        # elif index == 2:
        #     self.basic_content.content = view_search_rental(self.page, self.staff_store_id, self.conn)
        #     self.basic_content.update()

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