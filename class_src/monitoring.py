import flet
import threading, time
from class_popup import Popup

def connect_test(conn, server_status, server_time, connect_status, page: flet.Page):
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
            cursor.execute("select to_char(clock_timestamp(), 'YYYY-MM-DD HH24:MI:SS')")
            server_time.value = cursor.fetchone()[0]
        conn.commit()
        server_status.value = "Connected"
        # connect_status.content.color = flet.Colors.PRIMARY
        # connect_status.bgcolor = flet.Colors.PRIMARY_CONTAINER
        connect_status.update()
        # print(f"Server Time : {server_time}")
        timer = threading.Timer(1.0, connect_test, args=[conn, server_status, server_time, connect_status, page])
        timer.daemon = True  # 프로그램 꺼지면 타이머도 같이 꺼지게 설정
        timer.start()
    except Exception as err:
        conn.rollback()
        server_status.value = "Disconnected"
        # connect_status.content.color = flet.Colors.ERROR
        # connect_status.bgcolor = flet.Colors.ERROR_CONTAINER
        connect_status.update()
        print(f"Error: {err}")
        popup.show_error_open(
            message="Disconnected\nProgram Restart?",
            actions=[
                flet.TextButton("OK", on_click=restart_main),
                flet.TextButton("Cancel", on_click=popup.show_error_close)
            ],
        )