import flet
import time, base64, hashlib
import psycopg2
from db_connect import Popup
from window import Font

class LoginManager:
    def __init__(self, page: flet.Page, config, config_file):
        self.page = page
        self.config = config
        self.config_file = config_file
        self.count = 3
        self.current_login_data = None
        self.user = None
        self.password = None
        self.user_data = None
        self.call = "010-1234-5678"
        self.query =\
        """ select s.username , s.password , a.address , s.active , s.store_id
            from staff s
            inner join store s2 on s.store_id = s2.store_id 
            inner join address a on s2.address_id = a.address_id 
            where s.username = %s and s.password = %s and s.active is true """

    def check_login_process(self, e):
        popup = Popup(page=self.page)
        if self.config.read(self.config_file):
            # -- DB Connect --
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
            # -- Staff Login --
            cursor = conn.cursor()
            self.count = self.count - 1
            input_id = self.user.value
            raw_pw = self.password.value
            input_pw = hashlib.sha1(raw_pw.encode('utf-8')).hexdigest()
            try:
                cursor.execute(self.query, (input_id, input_pw,))
                user_data = cursor.fetchone()
                print("User Login ...")
                if user_data:
                    print(f"ID : {user_data[0]} | PW : {user_data[1]}")
                    self.page.window.min_width = None
                    self.page.window.min_height = None
                    self.page.window.resizable = True
                    self.page.window.maximizable = True
                    self.page.update()
                    self.page.clean()
                    self.page.window.destroy()
                else:
                    if self.count <= 0:
                        print(f"Login Failed : OUT")
                        popup.show_error_actions_message(
                            [flet.TextButton("Exit", on_click=popup.show_main_close, autofocus=True)],
                            f"Please Contact the Administrator\nPhone : {self.call}"
                        )
                    else:
                        print(f"Login Failed | Count (3) : {self.count}")
                        popup.show_error_message(f"Connect Failed\nCount (3) : {self.count}")
                        return
            except Exception as err:
                print(f"[staff_login] error : {err}")

def run_staff_login(page: flet.Page, config, config_file):
    login_handler = LoginManager(page=page, config=config, config_file=config_file)
    popup = Popup(page=page)
    # -- Frame --
    page.title = "Staff Login"
    page.window.resizable = False
    page.window.maximizable = False
    page.window.width = 400
    page.window.height = 310
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
        text_size=Font.login_ui, width=150, height=30, content_padding=10, max_length=10, autofocus=True)
    login_handler.password = flet.TextField(
        text_size=Font.login_ui, width=150, height=30, content_padding=10, max_length=20,
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