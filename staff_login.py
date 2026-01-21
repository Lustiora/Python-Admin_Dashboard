# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import psycopg2
import tkinter
from tkinter import messagebox
from window import center_window
from window import set_focus_force
import os
import configparser
import hashlib # 해시값 Encoding
import base64
# ---------------------------------------------------------
# Variable
# ---------------------------------------------------------
count = 3
current_login_data = None
username = None
password = None
login = None
# ---------------------------------------------------------
# Staff Login GUI
# ---------------------------------------------------------
def staff_login_gui():
    global login
    global username
    global password
    login = tkinter.Tk() # 표사되는 Window(tkinter.Tk())에 변수명을 지정하여 변수명을 기준으로 속성을 추가
    login.title("Staff Login")
    center_window(login, 260, 100, resizable=False)

    tkinter.Label(login, text="Username").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    username = tkinter.Entry(login) # Entry -> 입력칸 | 입력된 값을 사용하기 위해 변수명 지정 필요
    username.grid(row=0, column=1, padx=10, pady=5)
    login.grid_columnconfigure(0, weight=1) # ([열],[배당 비율])
    tkinter.Label(login, text="Password").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    password = tkinter.Entry(login, show="*") # show="*" > 유출 방지 : 입력값 * 대체 출력
    password.grid(row=1, column=1, padx=10, pady=5)
    password.bind("<Return>", check_login_process) # Enter key 입력으로 Login 모듈 동작 ("[입력키]", [모듈])
    login.grid_columnconfigure(1, weight=1)
    login_but = tkinter.Button(login, text="Login", command=check_login_process)
    login_but.grid(row=2, column=0, columnspan=2, padx=10, pady=3, sticky="ew") # command=[클릭시 동작내용] | sticky="e" > 우측 정렬
    login_but.bind("<Return>", check_login_process)

    login.after(200, set_focus_force, login, username) # set_focus_force(login, user_id)
    login.mainloop() # root(Window)를 지속적으로 반복 실행 (종료방지)
# ---------------------------------------------------------
# Check Login Process Module
# ---------------------------------------------------------
def check_login_process(event = None):
    global current_login_data
    global count
    global login
    # -- Load Config --
    appdata = os.getenv("APPDATA")
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
    print(f"\nConfig Load : {config_file}")
    config = configparser.ConfigParser()
    current_login_data = None
    if config.read(config_file):
        # -- DB Connect --
        login_db = config['DB Connect']['dbname']
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
        input_id = username.get()
        raw_pw = password.get()
        input_pw = hashlib.sha1(raw_pw.encode('utf-8')).hexdigest()
            # 1. 문자열을 바이트(byte)로 인코딩 (.encode('utf-8'))
            # 2. sha1 알고리즘 적용
            # 3. 16진수 문자열로 변환 (.hexdigest())
        try:
            cursor.execute(""" select s.username, s.password, s.active
                               from staff s
                               where s.username = %s
                                 and s.password = %s
                                 and s.active is true""", (input_id, input_pw,))
            user_data = cursor.fetchone()
            print("User Login ...")
            if user_data:  # 쿼리값 존재시
                print(f"ID : {user_data[0]} | PW : {user_data[1]}")
                login.destroy()
                from main_window import main_check_login_process
                main_check_login_process()
            else:  # 쿼리값 미존재시
                if count <= 0:
                    print(f"Login Failed")
                    messagebox.showerror("Staff Login", "Please Contact the Administrator\nPhone : 010-1234-5678")
                    login.destroy()
                else:
                    print(f"Login Failed | Count (3) : {count}")
                    messagebox.showerror("Staff Login", f"Connect Failed\nChance (3) : {count}")
        except Exception as e:
            print(f"error : {e}")
            if count == 0:
                print(f"Login Failed")
                messagebox.showinfo("Staff Login", "Please Contact the Administrator\nPhone : 010-1234-5678")
                login.destroy()