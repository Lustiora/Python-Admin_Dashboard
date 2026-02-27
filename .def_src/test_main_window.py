# 로그 메시지 출력
import logging
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

# 경고 메시지 출력으로 인한 딜레이 방지
import warnings
warnings.filterwarnings("ignore")

# -- Import --
import flet, os, sys, configparser, base64, psycopg2
from test_nav_tile import nav
# -- Variable --
# -- Module --
def check_login_process(page: flet.Page):
    store_id = 1
    store_address = "test Address"
    staff_user = "Superuser"
    # -- Load Config --
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")  # %appdata% 경로 변환
    else:
        appdata = os.path.expanduser("~/.config")
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
    print(f"\nConfig Load : {config_file}")
    config = configparser.ConfigParser()
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
        # -- Frame --
        page.title = "Sakila"
        page.bgcolor = flet.Colors.BLUE_GREY_50
        page.vertical_alignment = flet.MainAxisAlignment.START
        page.update()
        # -- Statusbar --
        con_status = flet.Container(
            content=flet.Text(value="status "),
            alignment=flet.Alignment(1, 1),
            height=24,
            padding=2,
            border_radius=5,
            bgcolor=flet.Colors.OUTLINE
        )
        # -- Main Area --
        ex_tile, basic_content = nav(page, login_db, login_host, login_port, store_address, staff_user, store_id,
                                     conn)  # test
        # -- Page --
        page.add(
            flet.Row([
                flet.Column([ex_tile
                             ], scroll=flet.ScrollMode.AUTO, alignment=flet.MainAxisAlignment.START),
                flet.VerticalDivider(width=1),
                flet.Column([basic_content, con_status], expand=True),
            ], expand=True, vertical_alignment=flet.CrossAxisAlignment.START
            )
        )
        # connect_test(conn, con_status, page)
        # -- Update --
        page.update()
    else:
        return
# -- Run Test --
if __name__ == "__main__":
    import webbrowser
    if os.getenv("FLET_NO_BROWSER"):
        webbrowser.open = lambda *args, **kwargs: None
    flet.app(target=check_login_process, assets_dir="assets", view=flet.WEB_BROWSER, port=34636) # test