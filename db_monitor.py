from tkinter import messagebox
import sys, os, subprocess

def connect_test(conn, status, main, target_file):
    try:
        print("Test Connected 5s")
        with conn.cursor() as cursor:
            cursor.execute("select 1")
        print("DB Connect Test : Connected")
        status.config(text="Connected", fg="green")  # .config를 사용하여 Label 값 교체 / status 값을 외부로 반출
    except Exception as e:
        status.config(text="Disconnected", fg="red")
        print(f"Error: {e}")
        if messagebox.askokcancel("Error", "Disconnected\nProgram Restart?"):
            main.destroy()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            target_file = os.path.join(current_dir, "db_connect.py")
            my_env = os.environ.copy()
            if "PYTHONPATH" in my_env:
                my_env["PYTHONPATH"] = current_dir + os.pathsep + my_env["PYTHONPATH"]
            else:
                my_env["PYTHONPATH"] = current_dir
            print("Restarting Process...")
            if sys.platform == 'win32':  # Windows OS의 경우 재시작 방식
                # [Windows] subprocess.Popen 사용 (새 창 띄우고 나는 종료)
                # os.system은 블로킹(대기) 현상이 있어 재시작에 부적합합니다.
                if getattr(sys, 'frozen', False):  # exe 패키지 구동시 실행 조건
                    print("Restarting Executable...")
                    subprocess.Popen([sys.executable], cwd=current_dir)
                else:
                    from db_connect import run_db_connect
                    os.system("python db_connect.py")
                sys.exit()
            else:  # 그외 OS(Linux)의 경우 재시작 방식
                os.environ.update(my_env)
                if getattr(sys, 'frozen', False):  # exe 패키지 구동시 실행 조건
                    print("Restarting Executable...")
                    application_path = sys.executable
                    os.execv(application_path, [application_path])
                else:
                    os.execv(sys.executable, [sys.executable, target_file])
                    # 현재 프로세스를 죽이고, 그 자리에서 새 파이썬을 실행 / 인자: (실행파일 경로, [실행파일경로, 스크립트파일])
        return  # 재시작 로직 진입 시 함수 종료  # 종료
    if main.winfo_exists():  # 창이 켜져 있을 때만 예약
        main.after(5000, lambda: connect_test(conn, status, main, target_file))