# -- Import --
import sys, os, time, configparser, base64
import psycopg2
import flet
from class_window import Font
from class_popup import Popup

class DBConnect:
    def __init__(self, page: flet.Page, popup: Popup):
        self.page = page
        self.popup = popup
        self.db = None
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        # -- Platform --
        if sys.platform == "win32":
            appdata = os.getenv("APPDATA")
        else:
            appdata = os.path.expanduser("~/.config")
        # -- Config --
        config_dir = os.path.join(appdata, "sakila", "db")
        self.config_file = os.path.join(config_dir, "config.ini")
        os.makedirs(config_dir, exist_ok=True)
        self.config = configparser.ConfigParser()

    def login_ui(self):
        # -- Label --
        db_name = flet.Text(value="Database")
        db_host = flet.Text(value="Host")
        db_port = flet.Text(value="Port")
        db_username = flet.Text(value="Username")
        db_password = flet.Text(value="Password")
        # -- Entry --
        self.db = flet.TextField(text_size=Font.login_ui, width=150, height=30, content_padding=5, max_length=10,
                            autofocus=True)
        self.host = flet.TextField(text_size=Font.login_ui, width=150, height=30, content_padding=5, max_length=40)
        self.port = flet.TextField(text_size=Font.login_ui, width=150, height=30, content_padding=5, max_length=6)
        self.username = flet.TextField(text_size=Font.login_ui, width=150, height=30, content_padding=5, max_length=10)
        self.password = flet.TextField(text_size=Font.login_ui, width=150, height=30, content_padding=5, max_length=20,
                                  on_submit=self.db_connect_event)
        # -- Button --
        connect = flet.Button("Connect", on_click=self.db_connect_event, width=230,
                              style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=5)))
        # -- Layout --
        self.page.vertical_alignment = flet.MainAxisAlignment.CENTER  # 세로 중앙
        self.page.horizontal_alignment = flet.CrossAxisAlignment.CENTER  # 가로 중앙
        self.page.add(
            flet.Row([
                flet.Column(
                    [
                        flet.Container(height=1)
                        , flet.Row([db_name, self.db])
                        , flet.Row([db_host, self.host])
                        , flet.Row([db_port, self.port])
                        , flet.Row([db_username, self.username])
                        , flet.Row([db_password, self.password])
                        , flet.Row([connect])
                    ], horizontal_alignment=flet.CrossAxisAlignment.END, alignment=flet.MainAxisAlignment.CENTER
                ),
            ], alignment=flet.MainAxisAlignment.CENTER, )
        )
        # -- Option --
        self.password.password = True # Snow Password
        self.password.can_reveal_password = True # Snow Password Toggle Button
        # -- Update --
        self.page.update()

    def db_connect_event(self, e):
        # type: ignore : .value 경고 제거
        if not self.db.value: # type: ignore
            self.popup.show_error_message("Please Login Database")
            return
        if not self.host.value: # type: ignore
            self.popup.show_error_message("Please Login Host")
            return
        if not self.port.value: # type: ignore
            self.popup.show_error_message("Please Login Port")
            return
        if not self.username.value: # type: ignore
            self.popup.show_error_message("Please Login ID")
            return
        if not self.password.value: # type: ignore
            self.popup.show_error_message("Please Login Password")
            return
        print(f"Connecting to {self.host.value}...") # type: ignore
        self.login_try()

    def login_try(self):
        if self.config.read(self.config_file):
            print("Loading Config")
            try:
                # -- Decoding --
                encrypted_pw = self.config['DB Connect']['password']
                pw_bytes = base64.b64decode(encrypted_pw)
                decrypted_pw = pw_bytes.decode('utf-8')
                conn = psycopg2.connect(
                    dbname=self.config['DB Connect']['db'],
                    host=self.config['DB Connect']['host'],
                    port=self.config['DB Connect']['port'],
                    user=self.config['DB Connect']['user'],
                    password=decrypted_pw
                )
                print("Auto Login Connection Established")
                self.staff_view()
            except Exception as e:
                print(f"Auto Login Failed:\n{e}")
                self.popup.show_error_message("Auto-Login Failed")
                self.page.clean()
                self.login_ui()
        else:
            print("Unable to Load")
            try:
                conn = psycopg2.connect(
                    dbname=self.db.value, # type: ignore
                    host=self.host.value, # type: ignore
                    port=self.port.value, # type: ignore
                    user=self.username.value, # type: ignore
                    password=self.password.value # type: ignore
                )
                self.save_config()
                self.staff_view()
            except Exception as err:
                print(f"Unable [load] Error : {err}")
                self.popup.show_error_message("Connection Failed")
                # noinspection PyCallingNonCallable
                self.page.open(self.popup.error)
                return

    def save_config(self):
        print("Saving Config")
        if not self.config.read(self.config_file):
            # -- encoding --
            pw_bytes = self.password.value.encode('utf-8') # type: ignore
            base64_bytes = base64.b64encode(pw_bytes)
            encrypted_pw = base64_bytes.decode('utf-8')

            self.config["DB Connect"] = {
                "db": self.db.value, # type: ignore
                "host": self.host.value, # type: ignore
                "port": self.port.value, # type: ignore
                "user": self.username.value, # type: ignore
                "password": encrypted_pw
            }
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
                print(f"{self.config_file} Save")

    def staff_view(self):
        print("DB Connect UI >> Staff Login UI")
        self.page.window.min_width = None
        self.page.window.min_height = None
        self.page.window.resizable = True
        self.page.window.maximizable = True
        self.page.clean()
        from staff_login_ui import staff_login_ui
        staff_login_ui(self.page, self.config, self.config_file)

def login_start(page: flet.Page):
    popup = Popup(page=page)
    app = DBConnect(page=page, popup=popup)
    page.clean()
    page.title = "DB Connect" # 창 타이틀
    page.vertical_alignment = flet.MainAxisAlignment.CENTER # 세로 중앙
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER # 가로 중앙
    page.window.resizable = False
    page.window.maximizable = False
    page.window.width = 400
    page.window.height = 310
    page.window.min_width = page.window.width
    page.window.min_height = page.window.height
    page.window.center()
    time.sleep(0.1) # Loading Time Force
    page.update()
    page.window.prevent_close = True # Exit Event
    page.window.on_event = popup.show_open
    connect = flet.Text(value="Connecting to Database", theme_style=flet.TextThemeStyle.TITLE_LARGE)
    page.add(
        flet.Column([
            flet.Row([connect], alignment=flet.MainAxisAlignment.CENTER),
            flet.Container(height=0),
            flet.Row([flet.ProgressRing()], alignment=flet.MainAxisAlignment.CENTER)
        ], horizontal_alignment=flet.MainAxisAlignment.CENTER)
    )
    if not app.config.read(app.config_file):
        print("No Config File Found. DB Connecting Setup...")
        page.clean()
        app.login_ui()
        return
    # -- Delay min 1.5s --
    start_time = time.time()
    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time < 1.5:
        time.sleep(1.5 - elapsed_time)
    app.login_try()

if __name__ == "__main__":
    flet.app(target=login_start, assets_dir="assets") # 모듈 실행을 정의