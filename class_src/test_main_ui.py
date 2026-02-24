# Log Print
import logging, warnings

from click import style

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
from class_popup import Popup
from navigation_tile import navigation

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
        login_db = config['DB Connect']['db']
        login_host = config['DB Connect']['host']
        login_port = config['DB Connect']['port']
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
    page.clean()
    page.title = "Sakila"
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

    # -- Statusbar --
    server_status = flet.Text(value="Server Status", text_align=flet.TextAlign.RIGHT)
    server_time = flet.Text(value="Server Time", text_align=flet.TextAlign.LEFT)
    connect_status =flet.Container(
        content=flet.Row([server_time, server_status], alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        height=24,
        alignment=flet.alignment.center_left,
        padding=flet.padding.only(left=10, right=10),
        border_radius=5,
        border=flet.border.all(color=flet.Colors.BLACK)
    )

    # -- Main Area --
    ex_tile, basic_content = navigation(
        page, conn, login_db, login_host, login_port, staff_user, staff_store_address, staff_store_id
    )

    # -- Page --
    page.add(
        flet.Row([
            flet.Column([ex_tile
                ],scroll=flet.ScrollMode.AUTO, alignment=flet.MainAxisAlignment.START),
            flet.VerticalDivider(width=1),
            flet.Column([basic_content, connect_status],expand=True),
                ], expand=True, vertical_alignment=flet.CrossAxisAlignment.START
        )
    )
    connect_test(conn, server_status, server_time, connect_status, page)

    # -- Update --
    page.update()

# -- Run Test --
if __name__ == "__main__":
    import webbrowser
    if os.getenv("FLET_NO_BROWSER"):
        webbrowser.open = lambda *args, **kwargs: None
    flet.app(target=run_main, assets_dir="assets", view=flet.WEB_BROWSER, port=34636) # test