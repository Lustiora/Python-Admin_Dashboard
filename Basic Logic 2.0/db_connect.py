# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import sys, os, configparser, base64
import psycopg2
import tkinter
import customtkinter
from tkinter import messagebox
from window import (center_window,
                    center_window_delayed,
                    Colors)
# ---------------------------------------------------------
# Save Config Module
# ---------------------------------------------------------
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
        "dbname": login_db,
        "host": login_host,
        "port": login_port,
        "user": login_id,
        "password": encrypted_pw
    }
    with open(config_file, "w") as configfile:
        config.write(configfile)
        print(f"{config_file} Save")
# ---------------------------------------------------------
# Load Config Helper (GUI용)
# ---------------------------------------------------------
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
            db_pw.delete(0, tkinter.END)
            encrypted_pw = config['DB Connect']['password']
            pw_bytes = base64.b64decode(encrypted_pw)
            decrypted_pw = pw_bytes.decode('utf-8')
            db_pw.insert(0, decrypted_pw)

            db_db.delete(0, tkinter.END)
            db_host.delete(0, tkinter.END)
            db_port.delete(0, tkinter.END)
            db_id.delete(0, tkinter.END)

            db_db.insert(0, config['DB Connect']['dbname'])
            db_host.insert(0, config['DB Connect']['host'])
            db_port.insert(0, config['DB Connect']['port'])
            db_id.insert(0, config['DB Connect']['user'])
        except Exception as e:
            print(f"Error : {e}")
# ---------------------------------------------------------
# Auto Login Logic (Launcher)
# ---------------------------------------------------------
def auto_login_start():
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
        run_db_connect()
        return
    # 2. 설정 파일이 있으면 -> 연결 시도
    try:
        login_db = config['DB Connect']['dbname']
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

        from staff_login import staff_login_gui # 연결 성공 시 staff_login_gui로 바로 진입
        staff_login_gui()

    except Exception as e:
        print(f"Auto-Login Failed:\n{e}")
        messagebox.showerror("Connection Failed",f"{e}")
        # 연결 실패 시 -> 설정창(run_db_connect) 실행
        run_db_connect()
# ---------------------------------------------------------
# Database Connect Module (Button Event)
# ---------------------------------------------------------
db = []
db_db = []
db_host = []
db_port = []
db_id = []
db_pw = []
def db_connect_event(event=None):
    global db, db_db, db_host, db_port, db_id, db_pw
    login_db = db_db.get()
    login_host = db_host.get()
    login_port = db_port.get()
    login_id = db_id.get()
    login_pw = db_pw.get()
    print(f"Connecting to {login_host}...")
    try:
        conn = psycopg2.connect(dbname=login_db,
                                host=login_host,
                                port=login_port,
                                user=login_id,
                                password=login_pw)
        print("Connection Established")
        save_config(login_db, login_host, login_port, login_id, login_pw)
        db.destroy()
        from staff_login import staff_login_gui
        staff_login_gui()
    except Exception as e:
        print(f"Connection Failed:\n{e}")
        messagebox.showerror("Connection Failed",f"{e}")
# ---------------------------------------------------------
# DB Connect GUI (Setup Screen)
# ---------------------------------------------------------
def run_db_connect():
    global db, db_db, db_host, db_port, db_id, db_pw
    db = customtkinter.CTk()
    db.withdraw()
    db.title("DB Connect")
    db.configure(fg_color=Colors.background)

    # UI Components
    customtkinter.CTkLabel(db, text="DB Name", fg_color=Colors.background, text_color=Colors.text).grid(row=1, column=0, pady=5, padx=5, sticky="e")
    db_db = customtkinter.CTkEntry(db)
    db_db.grid(row=1, column=1, pady=5, padx=5)

    customtkinter.CTkLabel(db, text="DB Host", fg_color=Colors.background, text_color=Colors.text).grid(row=2, column=0, pady=5, padx=5, sticky="e")
    db_host = customtkinter.CTkEntry(db)
    db_host.grid(row=2, column=1, pady=5, padx=5)

    customtkinter.CTkLabel(db, text="DB Port", fg_color=Colors.background, text_color=Colors.text).grid(row=3, column=0, pady=5, padx=5, sticky="e")
    db_port = customtkinter.CTkEntry(db)
    db_port.grid(row=3, column=1, pady=5, padx=5)

    customtkinter.CTkLabel(db, text="DB Username", fg_color=Colors.background, text_color=Colors.text).grid(row=4, column=0, pady=5, padx=5, sticky="e")
    db_id = customtkinter.CTkEntry(db)
    db_id.grid(row=4, column=1, pady=5, padx=5)

    customtkinter.CTkLabel(db, text="DB Password", fg_color=Colors.background, text_color=Colors.text).grid(row=5, column=0, pady=5, padx=5, sticky="e")
    db_pw = customtkinter.CTkEntry(db, show="*")
    db_pw.grid(row=5, column=1, pady=5, padx=5)

    db_pw.bind("<Return>", db_connect_event)

    db_login_but = customtkinter.CTkButton(db, text="DB Connect", command=db_connect_event,
                                  fg_color=Colors.action, text_color="white",
                                  hover_color=Colors.primary)
    db_login_but.grid(row=6, column=0, pady=5, padx=10, columnspan=2, sticky="ew")
    db_login_but.bind("<Return>", db_connect_event)

    db.grid_columnconfigure(0, weight=1)
    db.grid_columnconfigure(1, weight=1)
    db.grid_rowconfigure(0, weight=1)
    db.grid_rowconfigure(7, weight=1)

    load_config_to_gui()  # 기존 저장된 값 불러오기

    db.after(10, lambda: center_window_delayed(db, 300, 240, resizable=False))
    db_db.focus_set()
    db.mainloop()
# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    # [중요] 직접 실행 시 자동 로그인 로직부터 시작
    auto_login_start()