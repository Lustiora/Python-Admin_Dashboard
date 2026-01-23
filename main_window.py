# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import psycopg2
import sys
import os
import configparser
import hashlib # 해시값 Encoding
import base64
import tkinter
from tkinter import messagebox
from window import (center_window,
                    center_window_delayed,
                    start_move,
                    on_drag)
from login.db_monitor import connect_test
from sub_frame.sub_frame_search import (search_customer_frame,
                                        search_inventory_frame,
                                        search_film_frame,
                                        search_rental_frame,
                                        search_payment_frame)
from sub_frame.sub_frame_change import (change_customer_frame,
                                        change_inventory_frame,
                                        change_film_frame,
                                        change_rental_frame,
                                        change_payment_frame)
from sub_frame.sub_frame_delete import (delete_customer_frame,
                                        delete_inventory_frame,
                                        delete_film_frame,
                                        delete_rental_frame,
                                        delete_payment_frame)
from sub_frame.sub_frame_add import (add_customer_frame,
                                     add_inventory_frame,
                                     add_film_frame,
                                     add_actor_frame,
                                     add_category_frame)
# ---------------------------------------------------------
# Variable
# ---------------------------------------------------------
count = 3
current_login_data = None
current_status = None
check_status = []
# ---------------------------------------------------------
# Main Window Module
# ---------------------------------------------------------
def run_main(conn, login_db, login_host, login_port):
    # -- Variable --
    global current_login_data
    global current_status
    global check_status
    current_login_data = None
    current_status = None
    # -- Main --
    main = tkinter.Tk()
    main.withdraw()
    main.title("Sakila")
    center_window(main, 1024, 768, min_size=(1024,768))# -- DB 유령 연결 방지 --
    def on_closing():
        if messagebox.askokcancel("Quit", "Exit?"):
            print("Sakila Exit")
            # conn.close()  # DB 연결 종료
            main.destroy()
    main.protocol("WM_DELETE_WINDOW", on_closing)  # 메인 윈도우의 닫기 프로토콜에 연결
    # ---------------------------------------------------------
    # Sub Frame (Status)
    # ---------------------------------------------------------
    def close_status_frame(event=None):
        global current_status
        current_status.destroy()
        current_status = None

    def status_frame():
        global current_status
        if current_status is not None:
            current_status.lift()
            return
        # -- Frame --
        status_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
        status_frame.place(x=30, y=30)
        current_status = status_frame
        # -- Title Bar --
        title_bar = tkinter.Frame(current_status, bg="#2c3e50", height=30)
        title_bar.pack(fill="x", side="top")
        title_label = tkinter.Label(title_bar, text="Connect Status", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
        title_label.pack(side="left", padx=5)
        title_label.bind("<Button-1>", current_status.lift)
        # -- Close --
        close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", close_status_frame)
        # -- Body --
        content_frame = tkinter.Frame(current_status, bg="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tkinter.Label(content_frame, text="Database :", bg="white").grid(row=0, column=0, pady=5, sticky="e")
        tkinter.Label(content_frame, text="Host :", bg="white").grid(row=1, column=0, pady=5, sticky="e")
        tkinter.Label(content_frame, text="Port :", bg="white").grid(row=2, column=0, pady=5, sticky="e")
        tkinter.Label(content_frame, text="Connect Status :", bg="white").grid(row=3, column=0, pady=5, sticky="e")
        tkinter.Label(content_frame, text=login_db, bg="white").grid(row=0, column=1, pady=5, sticky="w")
        tkinter.Label(content_frame, text=login_host, bg="white").grid(row=1, column=1, pady=5, sticky="w")
        tkinter.Label(content_frame, text=login_port, bg="white").grid(row=2, column=1, pady=5, sticky="w")
        check_status = tkinter.Label(content_frame, text="Check_Status", fg="white", bg="white")
        check_status.grid(row=3, column=1, pady=5, sticky="w")
        def check_db(conn, check_status):
            try:
                with conn.cursor() as cursor:
                    cursor.execute("select 1")
                    print("DB Connect Check : Connected")
                    check_status.config(text="Connected", fg="green")
            except Exception as e:
                print(e)
                check_status.config(text = "Disconnected", fg="red")
            if status_frame.winfo_exists():  # 창이 켜져 있을 때만 예약
                status_frame.after(5000, lambda: check_db(conn, check_status))
        check_db(conn, check_status)
        # -- Click Event --
        content_frame.bind("<Button-1>", lambda e: current_status.lift())
        for widget in content_frame.winfo_children(): # 클릭 시 상단 표시, 하위 계층 전파
            widget.bind("<Button-1>", lambda e: current_status.lift(), add="+")
        title_bar.bind("<Button-1>", lambda e:start_move(e, current_status))
        title_bar.bind("<B1-Motion>", lambda e:on_drag(e, current_status))
        title_label.bind("<Button-1>", lambda e:start_move(e,current_status))
        title_label.bind("<B1-Motion>", lambda e:on_drag(e, current_status))
    # ---------------------------------------------------------
    # Main Window Menubar
    # ---------------------------------------------------------
    # -- Menubar Start --
    menubar = tkinter.Menu(main)
    # -- Menubar 1 --
    menu1 = tkinter.Menu(menubar, tearoff=0) # tearoff : 하위 메뉴 사용시 활성화
    menu1.add_command(label="상태")
    menu1.add_separator() # 구분선
    menu1.add_command(label="종료", command=on_closing)
    menubar.add_cascade(label="메뉴", menu=menu1)
    # -- Menubar 2 --
    menu2 = tkinter.Menu(menubar, tearoff=0)
    menu2.add_command(label="고객", command=lambda :search_customer_frame(main))
                                         # lambda : 실행 대기 필요시 사용 (즉시 실행 방지)
    menu2.add_separator()
    menu2.add_command(label="재고", command=lambda :search_inventory_frame(main))
    menu2.add_separator()
    menu2.add_command(label="영화", command=lambda :search_film_frame(main))
    menu2.add_separator()
    menu2.add_command(label="대여", command=lambda :search_rental_frame(main))
    menu2.add_separator()
    menu2.add_command(label="결제", command=lambda :search_payment_frame(main))
    menubar.add_cascade(label="조회", menu=menu2)
    # -- Menubar 3 --
    menu3 = tkinter.Menu(menubar, tearoff=0)
    menu3.add_command(label="고객", command=lambda :change_customer_frame(main))
    menu3.add_separator()
    menu3.add_command(label="재고", command=lambda :change_inventory_frame(main))
    menu3.add_separator()
    menu3.add_command(label="영화", command=lambda :change_film_frame(main))
    menu3.add_separator()
    menu3.add_command(label="대여", command=lambda :change_rental_frame(main))
    menu3.add_separator()
    menu3.add_command(label="결제", command=lambda :change_payment_frame(main))
    menubar.add_cascade(label="변경", menu=menu3)
    # -- Menubar 4 --
    menu4 = tkinter.Menu(menubar, tearoff=0)
    menu4.add_command(label="고객", command=lambda :delete_customer_frame(main))
    menu4.add_separator()
    menu4.add_command(label="재고", command=lambda :delete_inventory_frame(main))
    menu4.add_separator()
    menu4.add_command(label="영화", command=lambda :delete_film_frame(main))
    menu4.add_separator()
    menu4.add_command(label="대여", command=lambda :delete_rental_frame(main))
    menu4.add_separator()
    menu4.add_command(label="결제", command=lambda :delete_payment_frame(main))
    menubar.add_cascade(label="삭제", menu=menu4)
    # -- Menubar 5 --
    menu5 = tkinter.Menu(menubar, tearoff=0)
    menu5.add_command(label="고객", command=lambda :add_customer_frame(main))
    menu5.add_separator()
    menu5.add_command(label="재고", command=lambda :add_inventory_frame(main))
    menu5.add_separator()
    menu5.add_command(label="영화", command=lambda :add_film_frame(main))
    menu5.add_separator()
    menu5.add_command(label="배우", command=lambda :add_actor_frame(main))
    menu5.add_separator()
    menu5.add_command(label="장르", command=lambda :add_category_frame(main))
    menubar.add_cascade(label="추가", menu=menu5)
    # -- Menubar 6 --
    menu6 = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="통계", menu=menu6)
    # -- Menubar 7 --
    menu7 = tkinter.Menu(menubar, tearoff=0)
    menu7.add_command(label="직원")
    menubar.add_cascade(label="관리", menu=menu7)
    # -- Menubar End --
    main.config(menu=menubar)
    def main_focus_force():
        main.lift()
        main.attributes('-topmost', True)
        main.attributes('-topmost', False)
        main.focus_force() # 강제 포커스 (Entry or window 지정가능)
    main.after(200, main_focus_force)
    # ---------------------------------------------------------
    # Status Bar
    # ---------------------------------------------------------
    status_frame = tkinter.Frame(main)
    status_frame.pack(side="bottom", fill="x", padx=5, pady=5)
    status_frame.configure(bg="gainsboro")
    status = tkinter.Label(status_frame, text="Status", fg="white", bg="gainsboro") # 하단 모듈에서 status 값을 인자로 받아서 출력하기에 동일하게 명명해야 혼란방지
    status.pack(side="right")
    # ---------------------------------------------------------
    # Connect Test Module
    # ---------------------------------------------------------
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, "login/db_connect.py")
    connect_test(conn, status, main, target_file)
    # ---------------------------------------------------------
    # main.deiconify() # Window OS 동작 이상 시 주석 해제
    main.after(10, lambda: center_window_delayed(main, 1024, 768))
    main.mainloop()
# ---------------------------------------------------------
# Check Login Process Module
# ---------------------------------------------------------
def main_check_login_process(event = None):
    global current_login_data
    # -- Load Config --
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")  # %appdata% 경로 변환
    else:
        appdata = os.path.expanduser("~/.config")
    config_dir = os.path.join(appdata, "sakila", "db")
    config_file = os.path.join(config_dir, "config.ini")
    config = configparser.ConfigParser()
    current_login_data = None
    if config.read(config_file):
        try:
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
            print("Sakila DB Connected")
            run_main(conn, login_db, login_host, login_port)
        except Exception as e:
            print(f"Sakila DB Not Connected : {e}")

if __name__ == "__main__":
    print("Please run 'db_connect.py' to start the application.")