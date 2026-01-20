# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import psycopg2
import tkinter
from tkinter import messagebox
from staff_login import staff_login_gui
from window import center_window
from window import set_focus_force
import os # ls %appdata%\sakila\db / mkdir %appdata%\sakila\db
import configparser # ini Editor
import base64
# ---------------------------------------------------------
# Save Config Module
# ---------------------------------------------------------
def save_config(login_db, login_host, login_port, login_id, login_pw):
    appdata = os.getenv("APPDATA") # %appdata% 경로 변환
    config_dir = os.path.join(appdata, "sakila", "db") # 변환된 경로 -> "sakila" -> "db"
    config_file = os.path.join(config_dir, "config.ini") # config_dir -> "config.ini"
    os.makedirs(config_dir, exist_ok=True) # 폴더 생성 | exist_ok=True > 폴더 존재 시 Cancel
    config = configparser.ConfigParser() # ini Editor 호출
    # -- Password Base64 Encode --
    pw_bytes = login_pw.encode('utf-8') # Encode utf-8
    base64_bytes = base64.b64encode(pw_bytes) # base64.b64encode Encode
    encrypted_pw = base64_bytes.decode('utf-8') # Encode utf-8 Decode
    # --
    config["DB Connect"] = {"dbname": login_db, # 분류 생성
                            "host": login_host, # "key" : value
                            "port": login_port,
                            "user": login_id,
                            "password": encrypted_pw
                            }
    with open(config_file, "w") as configfile: # Export ini
        config.write(configfile)
        print(f"{config_file} Save")
    # https://docs.python.org/ko/3/library/configparser.html
# ---------------------------------------------------------
# Load Config Module
# ---------------------------------------------------------
def load_config():
    appdata = os.getenv("APPDATA")  # %appdata% 경로 변환
    config_dir = os.path.join(appdata, "sakila", "db")  # 변환된 경로 -> "sakila" -> "db"
    config_file = os.path.join(config_dir, "config.ini")  # config_dir -> "config.ini"
    config = configparser.ConfigParser()
    if config.read(config_file): # Read ini
        print(f"Load root : {config_file}")
        db_db.delete(0, tkinter.END)
        db_db.insert(0, config['DB Connect']['dbname'])
        db_host.delete(0, tkinter.END)
        db_host.insert(0, config['DB Connect']['host'])
        db_port.delete(0, tkinter.END)
        db_port.insert(0, config['DB Connect']['port'])
        db_id.delete(0, tkinter.END)
        db_id.insert(0, config['DB Connect']['user'])
        try:
            # -- Password Base64 Decode --
            encrypted_pw = config['DB Connect']['password'] # Encode Text Call
            pw_bytes = base64.b64decode(encrypted_pw) # base64.b64decode Decode
            decrypted_pw = pw_bytes.decode('utf-8') # utf-8 Decode
            # --
            db_pw.delete(0, tkinter.END)
            db_pw.insert(0, decrypted_pw) # Decode utf-8 Password
        except Exception as e:
            print(f"Error : {e}")
            messagebox.showinfo("DB Connect", f"The saved account information does not match.")
            db_db.delete(0, tkinter.END)
            db_host.delete(0, tkinter.END)
            db_port.delete(0, tkinter.END)
            db_id.delete(0, tkinter.END)
            db_pw.delete(0, tkinter.END)
            db.after(200, set_focus_force, db, db_db)
# ---------------------------------------------------------
# Database Connect Module
# ---------------------------------------------------------
count = 3
def db_connect(event=None):
    global count
    login_db = db_db.get()
    login_host = db_host.get()
    login_port = db_port.get()
    login_id = db_id.get()
    login_pw = db_pw.get()
    print(f"ID : {login_id} | PW : {login_pw}")
    print("DB Connected ...")
    count = count - 1
    try:
        conn = psycopg2.connect(dbname=login_db,
                                host=login_host, # Default : localhost
                                port=login_port, # Default : 5432
                                user=login_id,
                                password=login_pw)
        print("Connection Established")
        save_config(login_db, login_host, login_port, login_id, login_pw) # 연결 성공 시 저장
        db.destroy()
        staff_login_gui()
    except Exception as e:
        print(f"Not Connected | Chance(3) : {count}\nError : {e}")
        messagebox.showinfo("DB Connect", f"Not Connected\nChance(3) : {count}")
        if count == 0:
            messagebox.showinfo("DB Connect", "Please Contact the Administrator\nPhone : 010-1234-5678")
            print("Not Connected Time Out")
            db.destroy()
# ---------------------------------------------------------
# DB Connect GUI
# ---------------------------------------------------------
if __name__ == "__main__":
    db = tkinter.Tk()
    db.title("DB Connect")
    center_window(db, 260, 220)

# DB Name
tkinter.Label(db, text="DB Name").grid(row=0, column=0, pady=5, padx=5, sticky="e")
db_db = tkinter.Entry(db)
db_db.grid(row=0, column=1, pady=10, padx=5)
db.grid_columnconfigure(0, weight=1)

# DB Host
tkinter.Label(db, text="DB Host").grid(row=1, column=0, pady=5, padx=5, sticky="e")
db_host = tkinter.Entry(db)
db_host.grid(row=1, column=1, pady=10, padx=5)
db.grid_columnconfigure(1, weight=1)

# DB Port
tkinter.Label(db, text="DB Port").grid(row=2, column=0, pady=5, padx=5, sticky="e")
db_port = tkinter.Entry(db)
db_port.grid(row=2, column=1, pady=10, padx=5)
db.grid_columnconfigure(2, weight=1)

# DB Username
tkinter.Label(db, text="DB Username").grid(row=3, column=0, pady=5, padx=5, sticky="e")
db_id = tkinter.Entry(db)
db_id.grid(row=3, column=1, padx=10, pady=5)
db.grid_columnconfigure(3, weight=1)

# DB Password
tkinter.Label(db, text="DB Password").grid(row=4, column=0, pady=5, padx=5, sticky="e")
db_pw = tkinter.Entry(db, show="*")
db_pw.grid(row=4, column=1, padx=10, pady=5)
db_pw.bind("<Return>", db_connect)
db.grid_columnconfigure(4, weight=1)

# DB Connect Button
db_login_but = tkinter.Button(db, text="DB Connect", command=db_connect)
db_login_but.grid(row=5, column=0, padx=10, pady=3, columnspan=2, sticky="ew")
db_login_but.bind("<Return>", db_connect)

load_config()

db_db.focus_set() # DB Name Focus

db.mainloop()