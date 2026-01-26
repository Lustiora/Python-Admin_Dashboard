# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import sys, os, configparser, base64, hashlib
import psycopg2
import customtkinter
from tkinter import messagebox
from window import (center_window,
                    center_window_delayed,
                    set_focus_force,
                    Colors)
# ---------------------------------------------------------
# Variable
# ---------------------------------------------------------
count = 3
current_login_data = None
username = None
password = None
login = None
user_data = []
# ---------------------------------------------------------
# Staff Login GUI
# ---------------------------------------------------------
def staff_login_gui():
    global login
    global username
    global password
    login = customtkinter.CTk() # 표사되는 Window(customtkinter.CTk)에 변수명을 지정하여 변수명을 기준으로 속성을 추가
    login.withdraw() # Window 생성 다음에 숨겨야 글리치 현상 방지가능
    login.title("Staff Login")
    login.configure(fg_color=Colors.background)
    center_window(login, 260, 140, resizable=False)

    customtkinter.CTkLabel(login, text="Username", fg_color=Colors.background, text_color=Colors.text).grid(row=1, column=0, padx=5, pady=6, sticky="e")
    username = customtkinter.CTkEntry(login) # Entry -> 입력칸 | 입력된 값을 사용하기 위해 변수명 지정 필요
    username.grid(row=1, column=1, padx=10, pady=6)
    customtkinter.CTkLabel(login, text="Password", fg_color=Colors.background, text_color=Colors.text).grid(row=2, column=0, padx=5, pady=6, sticky="e")
    password = customtkinter.CTkEntry(login, show="*") # show="*" > 유출 방지 : 입력값 * 대체 출력
    password.grid(row=2, column=1, padx=10, pady=6)
    password.bind("<Return>", check_login_process) # Enter key 입력으로 Login 모듈 동작 ("[입력키]", [모듈])
    login_but = customtkinter.CTkButton(login, text="Login", command=check_login_process,
                                        fg_color=Colors.action, text_color="white",
                                        hover_color=Colors.primary, height=30)
    login_but.grid(row=3, column=0, columnspan=2, padx=10, pady=3, sticky="ew") # command=[클릭시 동작내용] | sticky="e" > 우측 정렬
    login_but.bind("<Return>", check_login_process)
    login.grid_columnconfigure(0, weight=1) # ([열],[배당 비율])
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)
    login.grid_rowconfigure(4, weight=1)

    # login.deiconify() # Window OS 동작 이상 시 주석 해제
    login.after(10, lambda: center_window_delayed(login, 260, 140))
    login.after(200, set_focus_force, login, username) # set_focus_force(login, user_id)
    login.mainloop() # root(Window)를 지속적으로 반복 실행 (종료방지)
# ---------------------------------------------------------
# Check Login Process Module
# ---------------------------------------------------------
def check_login_process(event = None):
    global current_login_data
    global count
    global login
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
            cursor.execute(""" 
               select s.username, s.password, a.address , s.active
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
                login.destroy()
                from main_window import staff_user_id
                staff_user_id(user_data[0], user_data[2])
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