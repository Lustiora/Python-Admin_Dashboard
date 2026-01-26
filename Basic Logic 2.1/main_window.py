# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import sys, os, configparser, base64
import psycopg2
import tkinter  # 메뉴바 구성을 위해 필요 (CTk에는 Menu 위젯이 없음)
import customtkinter
from tkinter import messagebox
from window import (center_window,
                    center_window_delayed,
                    start_move,
                    on_drag,
                    Colors)
from db_monitor import connect_test
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
current_login_data = None
current_status = None
check_status = []
staff_user = None
staff_store = None
# ---------------------------------------------------------
# Main Window Module
# ---------------------------------------------------------
def staff_user_id(user_id, store):
    global staff_user
    global staff_store
    staff_store = store
    staff_user = user_id
    return staff_user, staff_store

def run_main(conn, login_db, login_host, login_port):
    # -- Variable --
    global current_login_data
    global current_status
    global check_status
    global staff_user
    current_login_data = None
    current_status = None

    # -- Main --
    main = customtkinter.CTk()
    main.withdraw()
    main.title("Sakila")
    main.configure(fg_color=Colors.background)

    # 윈도우 크기 설정
    main_w, main_h = 1024, 768
    center_window(main, main_w, main_h, min_size=(1024, 768))

    # -- DB 유령 연결 방지 --
    def on_closing():
        if messagebox.askokcancel("Quit", "Exit?"):
            print("Sakila Exit")
            # conn.close()  # DB 연결 종료
            main.destroy()

    main.protocol("WM_DELETE_WINDOW", on_closing)

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
        status_frame = customtkinter.CTkFrame(main, width=300, height=300,
                                              fg_color=Colors.background,
                                              border_width=2,
                                              border_color=Colors.primary)
        status_frame.place(x=30, y=30)
        current_status = status_frame

        # -- Title Bar --
        title_bar = customtkinter.CTkFrame(current_status, fg_color=Colors.primary, height=30, corner_radius=0)
        title_bar.pack(fill="x", side="top")

        title_label = customtkinter.CTkLabel(title_bar, text="Connect Status",
                                             fg_color=Colors.primary, text_color=Colors.title_text,
                                             font=("Arial", 14, "bold"))  # CTk 폰트 크기 조정
        title_label.pack(side="left", padx=10)
        title_label.bind("<Button-1>", lambda e: current_status.lift)

        # -- Close --
        close_btn = customtkinter.CTkLabel(title_bar, text=" X ",
                                           fg_color=Colors.alert, text_color="white",
                                           width=30, height=30)
        close_btn.pack(side="right", padx=1)
        close_btn.bind("<Button-1>", close_status_frame)

        # -- Body --
        content_frame = customtkinter.CTkFrame(current_status, fg_color=Colors.background)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # 그리드 배치 (bg -> fg_color, fg -> text_color)
        labels = ["Database :", "Host :", "Port :", "Store :", "Login Staff :", "Connect Status :"]
        for i, text in enumerate(labels):
            customtkinter.CTkLabel(content_frame, text=text,
                                   fg_color=Colors.background, text_color=Colors.text).grid(row=i, column=0, pady=5, sticky="e")
        values = [login_db, login_host, login_port, staff_store, staff_user]
        for i, val in enumerate(values):
            customtkinter.CTkLabel(content_frame, text=val,
                                   fg_color=Colors.background, text_color=Colors.text).grid(row=i, column=1, pady=5, padx=10, sticky="w")
        check_status = customtkinter.CTkLabel(content_frame, text="Check_Status",
                                              text_color=Colors.text, fg_color=Colors.background)
        check_status.grid(row=5, column=1, pady=5, padx=10, sticky="w")

        def check_db(conn, check_status):
            try:
                with conn.cursor() as cursor:
                    cursor.execute("select 1")
                    # config -> configure
                    check_status.configure(text="Connected", text_color=Colors.success)
            except Exception as e:
                print(e)
                check_status.configure(text="Disconnected", text_color=Colors.alert)

            if status_frame.winfo_exists():
                status_frame.after(5000, lambda: check_db(conn, check_status))

        check_db(conn, check_status)

        # -- Click Event --
        content_frame.bind("<Button-1>", lambda e: current_status.lift())
        for widget in content_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: current_status.lift(), add="+")

        title_bar.bind("<Button-1>", lambda e: start_move(e, current_status))
        title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_status))
        title_label.bind("<Button-1>", lambda e: start_move(e, current_status))
        title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_status))

    # ---------------------------------------------------------
    # Main Window Menubar
    # ---------------------------------------------------------
    menu_theme = {
        "bg": Colors.point,  # 윈도우 OS에 따라 적용 안될 수 있음
        "fg": "white",
        "activebackground": Colors.action,
        "activeforeground": "white",
        "tearoff": 0
    }

    menubar = tkinter.Menu(main)

    # -- Menubar 1 (Menu) --
    menu1 = tkinter.Menu(menubar, **menu_theme)
    menu1.add_command(label="상태", command=status_frame)
    menu1.add_separator()
    menu1.add_command(label="종료", command=on_closing)
    menubar.add_cascade(label="메뉴", menu=menu1)

    # -- Menubar 2 (Search) --
    menu2 = tkinter.Menu(menubar, **menu_theme)
    menu2.add_command(label="고객", command=lambda: search_customer_frame(main))
    menu2.add_separator()
    menu2.add_command(label="재고", command=lambda: search_inventory_frame(main))
    menu2.add_separator()
    menu2.add_command(label="영화", command=lambda: search_film_frame(main))
    menu2.add_separator()
    menu2.add_command(label="대여", command=lambda: search_rental_frame(main))
    menu2.add_separator()
    menu2.add_command(label="결제", command=lambda: search_payment_frame(main))
    menubar.add_cascade(label="조회", menu=menu2)

    # -- Menubar 3 (Change) --
    menu3 = tkinter.Menu(menubar, **menu_theme)
    menu3.add_command(label="고객", command=lambda: change_customer_frame(main))
    menu3.add_separator()
    menu3.add_command(label="재고", command=lambda: change_inventory_frame(main))
    menu3.add_separator()
    menu3.add_command(label="영화", command=lambda: change_film_frame(main))
    menu3.add_separator()
    menu3.add_command(label="대여", command=lambda: change_rental_frame(main))
    menu3.add_separator()
    menu3.add_command(label="결제", command=lambda: change_payment_frame(main))
    menubar.add_cascade(label="변경", menu=menu3)

    # -- Menubar 4 (Delete) --
    menu4 = tkinter.Menu(menubar, **menu_theme)
    menu4.add_command(label="고객", command=lambda: delete_customer_frame(main))
    menu4.add_separator()
    menu4.add_command(label="재고", command=lambda: delete_inventory_frame(main))
    menu4.add_separator()
    menu4.add_command(label="영화", command=lambda: delete_film_frame(main))
    menu4.add_separator()
    menu4.add_command(label="대여", command=lambda: delete_rental_frame(main))
    menu4.add_separator()
    menu4.add_command(label="결제", command=lambda: delete_payment_frame(main))
    menubar.add_cascade(label="삭제", menu=menu4)

    # -- Menubar 5 (Add) --
    menu5 = tkinter.Menu(menubar, **menu_theme)
    menu5.add_command(label="고객", command=lambda: add_customer_frame(main))
    menu5.add_separator()
    menu5.add_command(label="재고", command=lambda: add_inventory_frame(main))
    menu5.add_separator()
    menu5.add_command(label="영화", command=lambda: add_film_frame(main))
    menu5.add_separator()
    menu5.add_command(label="배우", command=lambda: add_actor_frame(main))
    menu5.add_separator()
    menu5.add_command(label="장르", command=lambda: add_category_frame(main))
    menubar.add_cascade(label="추가", menu=menu5)

    # -- Menubar 6 (Manage) --
    menu6 = tkinter.Menu(menubar, **menu_theme)
    menu6.add_command(label="직원")
    menu6.add_separator()
    menu6.add_command(label="통계")
    menubar.add_cascade(label="관리", menu=menu6)

    # -- Menubar Apply --
    menubar.configure(bg=Colors.primary, fg="white")
    main.configure(menu=menubar)  # CTk 윈도우에 tkinter 메뉴 등록

    # ---------------------------------------------------------
    # Focus Force
    # ---------------------------------------------------------
    def main_focus_force():
        main.lift()
        main.attributes('-topmost', True)
        main.attributes('-topmost', False)
        main.focus_force()

    main.after(200, main_focus_force)
    # ---------------------------------------------------------
    # Status Bar
    # ---------------------------------------------------------
    status_frame = customtkinter.CTkFrame(main, height=30, corner_radius=0)  # 하단바는 각진게 좋음
    status_frame.pack(side="bottom", fill="x", padx=0, pady=0)
    status_frame.configure(fg_color=Colors.status_bar)

    status = customtkinter.CTkLabel(status_frame, text="Status",
                                    text_color=Colors.status_text,
                                    fg_color=Colors.status_bar)
    status.pack(side="right", padx=10)
    # ---------------------------------------------------------
    # Connect Test Module
    # ---------------------------------------------------------
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, "db_connect.py")

    connect_test(conn, status, main, target_file)
    # ---------------------------------------------------------
    main.after(10, lambda: center_window_delayed(main, main_w, main_h))
    main.mainloop()
# ---------------------------------------------------------
# Check Login Process Module
# ---------------------------------------------------------
def main_check_login_process(event=None):
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
                                    host=login_host,  # Default : localhost
                                    port=login_port,  # Default : 5432
                                    user=login_id,
                                    password=decrypted_pw)
            print("Sakila DB Connected")
            run_main(conn, login_db, login_host, login_port)
        except Exception as e:
            print(f"Sakila DB Not Connected : {e}")

if __name__ == "__main__":
    print("Please run 'db_connect.py' to start the application.")