# Log Print
import logging, warnings
level=logging.INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL
# ============================================================================
# [Logging Levels]
# 1. CRITICAL (50) : 🚨 시스템 붕괴 (엔진 폭발) -> 앱이 죽기 직전
# 2. ERROR    (40) : ❌ 기능 실패   (타이어 펑크) -> 배포 환경 (기본)
# 3. WARNING  (30) : ⚠️ 주의 요망   (연료 부족)   -> 예상치 못한 상황
# 4. INFO     (20) : ✅ 정상 작동   (시동 켜짐)   -> 배포 환경 (상세)
# 5. DEBUG    (10) : 🐞 개발 정보   (엔진 회전수) -> 개발 중 (현재)
# ============================================================================
logging.basicConfig(level=level)
warnings.filterwarnings("ignore")

# -- Import --
import flet, time, os, sys, configparser, psycopg2, base64
from monitoring import connect_test
from window_popup import Popup
from navigation_tile import navigation
from menu.search import view_search_rental, view_search_customer, view_search_payment
from menu.menu_ui import view_home
from material import Colors

class MainManager:
    def __init__(self, page: flet.Page, conn, staff_user, staff_store_address, staff_store_id, config, config_file):
        self.page = page
        self.conn = conn
        self.staff_user = staff_user
        self.staff_store_address = staff_store_address
        self.staff_store_id = staff_store_id
        self.config = config
        self.config_file = config_file

        if self.config['Theme']['theme'] == "DARK":
            self.page.theme_mode = flet.ThemeMode.DARK
            self.theme_switch = flet.Switch(value=False, on_change=self.toggle_theme)
            self.select_theme = flet.Icon(name=flet.Icons.DARK_MODE)
        elif self.config['Theme']['theme'] == "LIGHT":
            self.page.theme_mode = flet.ThemeMode.LIGHT
            self.theme_switch = flet.Switch(value=True, on_change=self.toggle_theme)
            self.select_theme = flet.Icon(name=flet.Icons.LIGHT_MODE_OUTLINED)
        else:
            self.page.theme_mode = flet.ThemeMode.SYSTEM
            self.theme_switch = flet.Switch(value=True, on_change=self.toggle_theme)
            self.select_theme = flet.Icon(name=flet.Icons.LIGHT_MODE_OUTLINED)

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
            "staff_user": self.staff_user,
            "staff_store_address": self.staff_store_address,
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

        self.ex_tile = navigation(self.basic_container, **params)[0]

        self.basic_content = navigation(self.basic_container, **params)[1]

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
                        flet.Row(controls=[self.theme_switch, self.select_theme]),
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
        if self.page.theme_mode == flet.ThemeMode.DARK:
            # print(f"save {self.page_theme[0]}")
            self.page.theme_mode = flet.ThemeMode.LIGHT
            self.select_theme.name = flet.Icons.LIGHT_MODE_OUTLINED
            self.config.set("Theme", "theme", "LIGHT")
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
                print(f"{self.config_file} Save")
        elif self.page.theme_mode == flet.ThemeMode.LIGHT or flet.ThemeMode.SYSTEM:
            # print(f"save {self.page_theme[0]}")
            self.page.theme_mode = flet.ThemeMode.DARK
            self.select_theme.name = flet.Icons.DARK_MODE
            self.config.set("Theme", "theme", "DARK")
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
                print(f"{self.config_file} Save")
        if self.page:
            self.page.update()

# -- Module --
def run_main(page: flet.Page):
    # -- Platform --
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")
    else:
        appdata = os.path.expanduser("~/.config")
    # -- Config --
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
    os.makedirs(config_dir, exist_ok=True)
    config = configparser.ConfigParser()

    # -- Decoding --
    if config.read(config_file):
        user_theme = config['Theme']['theme']
        # login_db = config['DB Connect']['db']
        # login_host = config['DB Connect']['host']
        # login_port = config['DB Connect']['port']
        encrypted_pw = config['DB Connect']['password']
        pw_bytes = base64.b64decode(encrypted_pw)
        decrypted_pw = pw_bytes.decode('utf-8')
        conn = psycopg2.connect(
            dbname=config['DB Connect']['db'],
            host=config['DB Connect']['host'],
            port=config['DB Connect']['port'],
            user=config['DB Connect']['user'],
            password=decrypted_pw
        )
    else:
        return

    staff_user = "Superuser"
    staff_store_address = "Test Address"
    staff_store_id = 1

    popup = Popup(page=page)

    # -- Frame --
    page.title = "Sakila"
    page.theme_mode = user_theme
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
    page.window.prevent_close = True
    page.window.on_event = popup.show_open

    # -- Page --
    main_handler = MainManager(page=page, conn=conn, staff_user=staff_user,
                               staff_store_address=staff_store_address, staff_store_id=staff_store_id,
                               config=config, config_file=config_file)
    connect_test(conn, main_handler.server_status, main_handler.server_time, main_handler.connect_status, page)

# -- Run Test --
if __name__ == "__main__":
    import webbrowser
    if os.getenv("FLET_NO_BROWSER"):
        webbrowser.open = lambda *args, **kwargs: None
    flet.app(target=run_main, assets_dir="assets", view=flet.WEB_BROWSER, port=34636) # test