import flet
import sys, os, subprocess, threading

def connect_test(conn, status, page: flet.Page):  # DB 연결 확인
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, "db_connect.py")
    def open_pop(page):
        page.open(main_quit)
    def close_pop(e):
        page.close(main_quit)  # 팝업창 종료 명령어
    def close_main(e):
        page.window.destroy()
        page.window.close()
        if getattr(sys, 'frozen', False):  # [Windows EXE]
            current_executable = sys.executable
            current_dir = os.path.dirname(current_executable)
        else:  # [개발 환경]
            current_executable = sys.executable
            current_dir = os.path.dirname(os.path.abspath(__file__))
        print("Restarting Process...")
        if sys.platform == 'win32':  # explorer.exe "실행파일경로" 명령 실행
            if getattr(sys, 'frozen', False):
                print("Restarting via Windows Explorer...")
                subprocess.Popen(['explorer', current_executable])
            else:  # [Windows 개발 환경]
                print("Restarting via os.system...")
                os.chdir(current_dir)
                os.system("python db_connect.py")
            sys.exit()  # 파이썬 종료
        else:  # [Linux / Mac]
            my_env = os.environ.copy()
            if "PYTHONPATH" in my_env:
                my_env["PYTHONPATH"] = current_dir + os.pathsep + my_env["PYTHONPATH"]
            else:
                my_env["PYTHONPATH"] = current_dir
            os.environ.update(my_env)
            if getattr(sys, 'frozen', False):
                os.execv(sys.executable, [sys.executable])
            else:
                os.execv(sys.executable, [sys.executable, target_file])
    main_quit = flet.AlertDialog(
        title=flet.Text("Connect Error"),
        content=flet.Text("Disconnected\nProgram Restart?"),
        actions=[flet.TextButton("OK", on_click=close_main),
                 flet.TextButton("Cancel", on_click=close_pop)
                 ], actions_alignment=flet.MainAxisAlignment.END)
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
        open_pop(page)
    status.update()