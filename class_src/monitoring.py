import flet
import threading, time
from class_popup import Popup

def connect_test(conn, status, page: flet.Page):
    popup = Popup(page=page)
    def restart_main(e):
        page.window.prevent_close = False
        popup.show_error_close(True)
        time.sleep(0.1)
        page.clean()
        page.update()
        from db_connect_ui import login_start
        login_start(page)

    try:
        with conn.cursor() as cursor:
            cursor.execute("select 1")
        status.content.value = "Connected "
        status.content.color = flet.Colors.PRIMARY
        status.bgcolor = flet.Colors.PRIMARY_CONTAINER
        status.update()
        timer = threading.Timer(2.0, connect_test, args=[conn, status, page])
        timer.daemon = True  # 프로그램 꺼지면 타이머도 같이 꺼지게 설정
        timer.start()
    except Exception as err:
        status.content.value = "Disconnected "
        status.content.color = flet.Colors.ERROR
        status.bgcolor = flet.Colors.ERROR_CONTAINER
        status.update()
        print(f"Error: {err}")
        popup.show_error_open(
            message="Disconnected\nProgram Restart?",
            actions=[
                flet.TextButton("OK", on_click=restart_main),
                flet.TextButton("Cancel", on_click=popup.show_error_close)
            ],
        )