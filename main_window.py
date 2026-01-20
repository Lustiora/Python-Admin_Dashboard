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
# ---------------------------------------------------------
# Main Window Module
# ---------------------------------------------------------
def run_main():
    main = tkinter.Tk()
    main.title("Sakila")
    center_window(main, 1024, 768, min_size=(1024,768))
    # ---------------------------------------------------------
    # Main Window GUI
    # ---------------------------------------------------------
    # tkinter.LabelFrame(main)
# ---------------------------------------------------------
# Check Login Process Module
# ---------------------------------------------------------
def main_check_login_process(event = None):
    global current_login_data
    global count
    # -- Load Config --
    appdata = os.getenv("APPDATA")
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
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
        print("DB Connected Main")
        run_main()