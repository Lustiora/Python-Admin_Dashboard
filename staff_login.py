# -- Import --
import sys, os, configparser, base64, hashlib
import psycopg2
import flet, time
from window import Font
# -- Variable --
count = 3
current_login_data = None
user = None
password = None
user_data = []
call = "010-1234-5678"
# -- Module --
# -- AlertDialog --
def close_connect_error(e):
    e.page.close(dlg_connect_error) # 팝업창 종료 명령어
def exit_connect_error(e):
    e.page.window.prevent_close = False
    e.page.window.close()
    e.page.window.destroy()
dlg_connect_error = flet.AlertDialog(
    title=flet.Text("Login Failed"),
    content=flet.Text("Your ID or password is incorrect."),
    actions=[flet.TextButton("Cancel", on_click=close_connect_error),
    ], actions_alignment=flet.MainAxisAlignment.END)
# -- Staff Login GUI
def run_staff_login(page: flet.Page):
    global user, password
    # -- Frame --
    page.clean()
    page.title = "Staff Login"
    page.bgcolor = flet.Colors.BLUE_GREY_50
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
    page.window.prevent_close = True  # X 이벤트 옵션 추가
    def close_pop(e):
        e.page.close(main_quit)  # 팝업창 종료 명령어
    def close_main(e):
        e.page.window.close()
        e.page.window.destroy()  # 윈도우 창 종료 명령어
    main_quit = flet.AlertDialog(
        title=flet.Text("Quit"),
        content=flet.Text("Exit?"),
        actions=[flet.TextButton("OK", on_click=close_main),
                 flet.TextButton("Cancel", on_click=close_pop)
                 ], actions_alignment=flet.MainAxisAlignment.END)
    def window_event(e):
        if e.data == "close":
            e.page.open(main_quit)
    page.window.on_event = window_event
    # -- -- -- -- -- -- -- -- -- --
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.window.center()
    # -- Label --
    staff_user = flet.Text(value="Staff ID")
    staff_password = flet.Text(value="Password")
    # -- Entry --
    user = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=10, max_length=10, autofocus=True)
    password = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=10, max_length=20)
    # -- Button --
    login = flet.Button("Login", on_click=check_login_process, width=230, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    # -- Layout --
    page.add(
        flet.Row([
            flet.Column([
                flet.Container(height=1),
                flet.Row([staff_user, user]),
                flet.Row([staff_password, password]),
                flet.Row([login])
            ], horizontal_alignment=flet.CrossAxisAlignment.END)
        ], alignment=flet.MainAxisAlignment.CENTER,)
    )
    # -- Option --
    password.password = True
    password.can_reveal_password = True
    # -- Update --
    page.update()
# -- Check Login Process Module --
def check_login_process(e):
    global current_login_data
    global count
    global user_data
    user_data = []
    # -- Load Config --
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")  # %appdata% 경로 변환
    else:
        appdata = os.path.expanduser("~/.config")
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
    print(f"\nConfig Load : {config_file}")
    config = configparser.ConfigParser()
    current_login_data = None
    if config.read(config_file):
        # -- DB Connect --
        login_db = config['DB Connect']['db']
        login_host = config['DB Connect']['host']
        login_port = config['DB Connect']['port']
        login_id = config['DB Connect']['user']
        # -- Password Base64 Decode --
        encrypted_pw = config['DB Connect']['password']  # Encode Text Call
        pw_bytes = base64.b64decode(encrypted_pw)  # base64.b64decode Decode
        decrypted_pw = pw_bytes.decode('utf-8')  # utf-8 Decode
        # --
        conn = psycopg2.connect(dbname=login_db,
                                        host=login_host, # Default : localhost
                                        port=login_port, # Default : 5432
                                        user=login_id,
                                        password=decrypted_pw)
        print("DB Connected")
        # -- Staff Login --
        cursor = conn.cursor()
        count = count - 1
        input_id = user.value
        raw_pw = password.value
        input_pw = hashlib.sha1(raw_pw.encode('utf-8')).hexdigest()
            # 1. 문자열을 바이트(byte)로 인코딩 (.encode('utf-8'))
            # 2. sha1 알고리즘 적용
            # 3. 16진수 문자열로 변환 (.hexdigest())
        try:
            cursor.execute(""" 
               select s.username, s.password, a.address , s.active , s.store_id
               from staff s
               inner join store s2 
                  on s.store_id = s2.store_id 
               inner join address a
                  on s2.address_id = a.address_id 
               where s.username = %s
                 and s.password = %s
                 and s.active is true""", (input_id, input_pw,))
            user_data = cursor.fetchone()
            print("User Login ...")
            if user_data:  # 쿼리값 존재시
                print(f"ID : {user_data[0]} | PW : {user_data[1]}")
                e.page.window.min_width = None
                e.page.window.min_height = None
                e.page.window.resizable = True
                e.page.window.maximizable = True
                e.page.update()
                e.page.clean()
                from main_window import run_main
                run_main(e.page, conn, login_db, login_host, login_port, user_data[2], user_data[0], user_data[4])
            else:  # 쿼리값 미존재시
                if count <= 0:
                    print(f"Login Failed")
                    dlg_connect_error.content.value = f"Please Contact the Administrator\nPhone : {call}"
                    dlg_connect_error.actions = [flet.TextButton("Cancel", on_click=exit_connect_error),]
                    e.page.open(dlg_connect_error)
                else:
                    print(f"Login Failed | Count (3) : {count}")
                    dlg_connect_error.content.value = f"Connect Failed\nCount (3) : {count}"
                    e.page.open(dlg_connect_error)
                    e.page.update()
        except Exception as e:
            print(f"[staff_login] error : {e}")
# -- Run Test --
# flet.app(target=run_staff_login)