import flet
import time, hashlib
from window_setting import Colors
from window_popup import Popup
from window_setting import Font

class LoginManager:
    def __init__(self, page: flet.Page, conn, config, config_file):
        self.page = page
        self.conn = conn
        self.config = config
        self.config_file = config_file
        self.count = 3
        self.current_login_data = None
        self.user = None
        self.password = None
        self.user_data = None
        self.call = "010-1234-5678"
        self.query =\
        """ select s.username , s.password , a.address , s.store_id
            from staff s
            inner join store s2 on s.store_id = s2.store_id 
            inner join address a on s2.address_id = a.address_id 
            where s.username = %s and s.password = %s and s.active is true """

    def check_login_process(self, e):
        popup = Popup(page=self.page)
        # -- Staff Login --
        cursor = self.conn.cursor()
        self.count = self.count - 1
        input_id = self.user.value
        raw_pw = self.password.value
        input_pw = hashlib.sha1(raw_pw.encode('utf-8')).hexdigest()
        try:
            cursor.execute(self.query, (input_id, input_pw,))
            user_data = cursor.fetchone()
            print("User Login ...")
            if user_data:
                staff_user = user_data[0]
                staff_pw = user_data[1]
                staff_store_address = user_data[2]
                staff_store_id = user_data[3]
                print(f"ID : {staff_user} | PW : {staff_pw}")
                self.page.window.min_width = None
                self.page.window.min_height = None
                self.page.window.resizable = True
                self.page.window.maximizable = True
                self.page.update()
                self.page.clean()
                self.conn.commit()
                from main_ui import run_main
                run_main(self.page, self.conn, staff_user, staff_store_address, staff_store_id, self.config, self.config_file)
            else:
                self.conn.commit()
                if self.count <= 0:
                    print(f"Login Failed : OUT")
                    popup.show_popup_open(
                        title="Login Attempt Failed",
                        message = "Access restricted due to repeated authentication failures. \n"
                                  "The program will exit for security purposes. \n"
                                  f"HQ Liaison Contact : {self.call}",
                        actions=[flet.TextButton("Exit", on_click=popup.show_main_close, autofocus=True)]
                    )
                else:
                    self.conn.rollback()
                    print(f"Remaining Attempts: {self.count} / 3")
                    popup.show_popup_open(
                        title="Login Attempt Failed",
                        message = f"Invalid ID or Password. \n[Remaining Attempts: {self.count} / 3]"
                    )
                    return
        except Exception as err:
            self.conn.rollback()
            print(f"[staff_login] error : {err}")

def staff_login_ui(page: flet.Page, conn, config, config_file):
    login_handler = LoginManager(page=page, conn=conn, config=config, config_file=config_file)
    popup = Popup(page=page)
    # -- Frame --
    page.title = "Staff Login"
    page.window.resizable = False
    page.window.maximizable = False
    page.window.width = 400
    page.window.height = 310
    if config['Theme']['theme'] == "DARK":
        page.theme_mode = flet.ThemeMode.DARK
    elif config['Theme']['theme'] == "LIGHT":
        page.theme_mode = flet.ThemeMode.LIGHT
    else:
        page.theme_mode = flet.ThemeMode.SYSTEM
    page.window.min_width = page.window.width
    page.window.min_height = page.window.height
    page.window.center()
    time.sleep(0.1)  # Loading Time Force : 옵션 적용 전 시작 방지
    page.update()
    # -- Exit --
    page.window.prevent_close = True
    page.window.on_event = popup.show_open
    # -- -- -- -- -- -- -- -- -- --
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.window.center()
    # -- Label --
    staff_user = flet.Text(value="Staff ID")
    staff_password = flet.Text(value="Password")
    # -- Entry --
    login_handler.user = flet.TextField(
        text_size=Font.login_ui, width=150, height=30, content_padding=10, max_length=10, autofocus=True, border_color=Colors.border_color)
    login_handler.password = flet.TextField(
        text_size=Font.login_ui, width=150, height=30, content_padding=10, max_length=20, border_color=Colors.border_color,
        on_submit=login_handler.check_login_process)
    # -- Button --
    login_btn = flet.Button("Login", on_click=login_handler.check_login_process, width=230,
                        style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    # -- Layout --
    page.add(
        flet.Row([
            flet.Column([
                flet.Container(height=1),
                flet.Row([staff_user, login_handler.user]),
                flet.Row([staff_password, login_handler.password]),
                flet.Row([login_btn])
            ], horizontal_alignment=flet.CrossAxisAlignment.END)
        ], alignment=flet.MainAxisAlignment.CENTER,)
    )
    # -- Option --
    login_handler.password.password = True
    login_handler.password.can_reveal_password = True
    # -- Update --
    page.update()