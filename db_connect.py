# -- Import --
import sys, os, configparser, base64
import psycopg2
import flet
from window import Font
# -- Variable --
db = []
host = []
port = []
username = []
password = []
# -- Module --
# -- AlertDialog --
def close_connect_error(e):
    e.page.close(dlg_connect_error)
dlg_connect_error = flet.AlertDialog(
    title=flet.Text("Connected Failed"),
    content=flet.Text("Your ID or password is incorrect."),
    actions=[flet.TextButton("Cancel", on_click=close_connect_error),
    ], actions_alignment=flet.MainAxisAlignment.END)
# -- Save Config Module --
def save_config(login_db, login_host, login_port, login_id, login_pw):
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")
    else:
        appdata = os.path.expanduser("~/.config")
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
    os.makedirs(config_dir, exist_ok=True)
    config = configparser.ConfigParser()

    pw_bytes = login_pw.encode('utf-8')
    base64_bytes = base64.b64encode(pw_bytes)
    encrypted_pw = base64_bytes.decode('utf-8')

    config["DB Connect"] = {
        "db": login_db,
        "host": login_host,
        "port": login_port,
        "user": login_id,
        "password": encrypted_pw
    }
    with open(config_file, "w") as configfile:
        config.write(configfile)
        print(f"{config_file} Save")
# -- Load Config Helper (GUI용) --
def load_config_to_gui():
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")
    else:
        appdata = os.path.expanduser("~/.config")
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
    config = configparser.ConfigParser()

    if config.read(config_file):
        print(f"Load root : {config_file}")
        try:
            password.value = ""
            encrypted_pw = config['DB Connect']['password']
            pw_bytes = base64.b64decode(encrypted_pw)
            decrypted_pw = pw_bytes.decode('utf-8')
            password.value = decrypted_pw

            db.value = ""
            host.value = ""
            port.value = ""
            username.value = ""

            db.insert(0, config['DB Connect']['db'])
            host.insert(0, config['DB Connect']['host'])
            port.insert(0, config['DB Connect']['port'])
            username.insert(0, config['DB Connect']['user'])
        except Exception as e:
            print(f"Error : {e}")
# -- Auto Login Logic (Launcher) --
def auto_login_start(page: flet.Page):
    if sys.platform == "win32": # windows OS 의 경우
        appdata = os.getenv("APPDATA")
    else: # 그외 OS(Linux)의 경우
        appdata = os.path.expanduser("~/.config")
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
    config = configparser.ConfigParser()
    # 1. 설정 파일이 없으면 -> 설정창(run_db_connect) 실행
    if not config.read(config_file):
        print("No Config File Found. Starting Setup...")
        run_db_connect(page)
        return
    # 2. 설정 파일이 있으면 -> 연결 시도
    try:
        login_db = config['DB Connect']['db']
        login_host = config['DB Connect']['host']
        login_port = config['DB Connect']['port']
        login_id = config['DB Connect']['user']
        encrypted_pw = config['DB Connect']['password']

        pw_bytes = base64.b64decode(encrypted_pw)
        decrypted_pw = pw_bytes.decode('utf-8')

        conn = psycopg2.connect(
            dbname=login_db,
            host=login_host,
            port=login_port,
            user=login_id,
            password=decrypted_pw
        )
        print("Auto-Login Successful. Launching Main Window...")
        page.window.min_width = None
        page.window.min_height = None
        page.window.resizable = True
        page.window.maximizable = True
        page.clean()
        from staff_login import run_staff_login
        run_staff_login(page)
    except Exception as err:
        print(f"Auto-Login Failed:\n{err}")
        run_db_connect(page)
        dlg_connect_error.content.value = "Auto-Login Failed"
        page.open(dlg_connect_error)
        page.update()
# -- Database Connect Module (Button Event) --
def db_connect_event(e):
    global db, host, port, username, password
    login_db = db.value
    login_host = host.value
    login_port = port.value
    login_id = username.value
    login_pw = password.value
    print(f"Connecting to {login_host}...")
    try:
        conn = psycopg2.connect(dbname=login_db,
                                host=login_host,
                                port=login_port,
                                user=login_id,
                                password=login_pw)
        print("Connection Established")
        save_config(login_db, login_host, login_port, login_id, login_pw)
        e.page.clean()
        from staff_login import run_staff_login
        run_staff_login(e.page)
    except Exception as err:
        print(f"Connection Failed:\n{err}")
        e.page.open(dlg_connect_error)
        e.page.update()
# -- DB Connect GUI (Setup Screen) --
def run_db_connect(page: flet.Page):
    global db, host, port, username, password
    # -- Frame --
    page.title = "DB Connect" # 창 타이틀
    page.window.width = 400 # 창 가로
    page.window.height = 310 # 창 세로
    # -- Linux Window Force Size --
    page.window.min_width = page.window.width
    page.window.min_height = page.window.height
    # -- Exit --
    page.window.prevent_close = True  # X X 이벤트 옵션 추가
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
    page.window.resizable = False # 창 크기 변환 금지
    page.window.maximizable = False # 창 최대화 버튼 금지
    page.window.center() # 모니터 정중앙 출력
    # -- Label --
    db_name = flet.Text(value="Database")
    db_host = flet.Text(value="Host")
    db_port = flet.Text(value="Port")
    db_username = flet.Text(value="Username")
    db_password = flet.Text(value="Password")
    # -- Entry --
    db = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10)
    host = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=40)
    port = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=6)
    username = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10)
    password = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=20)
    # text_align=flet.TextAlign.RIGHT : 입력문자 우측에서 좌측 출력 (기본 좌측에서 우측 출력)
    # content_padding : 입력칸 테두리와 글자 사이의 간격 (들여쓰기, 위아래)
    # max_length : 최대 문자값
    # https://docs.flet.dev/controls/textfield/#flet.TextField.strut_style
    # -- Button --
    connect = flet.Button("Connect", on_click=db_connect_event, width=230, style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=5)))
    # -- Layout --
    page.vertical_alignment = flet.MainAxisAlignment.CENTER # 세로 중앙
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER # 가로 중앙
    page.add(
        flet.Row([
            flet.Column(
                [
                    flet.Container(height=1) # 보이지 않는 박스를 추가하여 간격 조절
                    , flet.Row([db_name, db])
                    , flet.Row([db_host, host])
                    , flet.Row([db_port, port])
                    , flet.Row([db_username, username])
                    , flet.Row([db_password, password])
                    , flet.Row([connect])
                ], horizontal_alignment=flet.CrossAxisAlignment.END, alignment=flet.MainAxisAlignment.CENTER
            ),
        ], alignment=flet.MainAxisAlignment.CENTER,)
    )
    # -- Option --
    password.password = True # 패스워드 *** 표시 = 사용
    password.can_reveal_password = True # 가려진 패스워드 표시 토글 버튼 = 사용
    # -- Update --
    page.update() # 모듈의 작성된 코드를 적용
# -- Run --
flet.app(target=auto_login_start) # 모듈 실행을 정의