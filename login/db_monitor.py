from tkinter import messagebox
import sys
import os
import subprocess
from window import Colors

def connect_test(conn, status, main, target_file): # DB 연결 확인
    try:
        with conn.cursor() as cursor:
            cursor.execute("select 1")
        status.config(text="Connected", fg=Colors.success)
    except Exception as e:
        status.config(text="Disconnected", fg=Colors.alert)
        print(f"Error: {e}")
        if messagebox.askokcancel("Error", "Disconnected\nProgram Restart?"):
            main.destroy()
            if getattr(sys, 'frozen', False): # [Windows EXE]
                current_executable = sys.executable
                current_dir = os.path.dirname(current_executable)
            else: # [개발 환경]
                current_executable = sys.executable
                current_dir = os.path.dirname(os.path.abspath(__file__))
            print("Restarting Process...")
            if sys.platform == 'win32': # explorer.exe "실행파일경로" 명령 실행
                if getattr(sys, 'frozen', False):
                    print("Restarting via Windows Explorer...")
                    subprocess.Popen(['explorer', current_executable])
                else: # [Windows 개발 환경]
                    print("Restarting via os.system...")
                    os.chdir(current_dir)
                    os.system("python db_connect.py")
                sys.exit() # 파이썬 종료
            else: # [Linux / Mac]
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
        return
    if main.winfo_exists():
        main.after(5000, lambda: connect_test(conn, status, main, target_file))