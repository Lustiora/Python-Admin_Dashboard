# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import psycopg2
import sys
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
current_status = None
current_search_customer = None
current_search_inventory = None
current_search_film = None
current_search_rental = None
current_search_payment = None
status = []
# ---------------------------------------------------------
# Main Window Module
# ---------------------------------------------------------
def run_main(conn, login_db, login_host, login_port):
    # -- Variable --
    global current_login_data
    global current_status
    global current_search_customer
    global current_search_inventory
    global current_search_film
    global current_search_rental
    global current_search_payment
    global status
    current_login_data = None
    current_status = None
    current_search_customer = None
    current_search_inventory = None
    current_search_film = None
    current_search_rental = None
    current_search_payment = None
    # -- Main --
    main = tkinter.Tk()
    main.title("Sakila")
    center_window(main, 1024, 768, min_size=(1024,768))# -- DB 유령 연결 방지 --
    def on_closing():
        if messagebox.askokcancel("Quit", "Exit?"):
            print("Sakila Exit")
            # conn.close()  # DB 연결 종료
            main.destroy()
    main.protocol("WM_DELETE_WINDOW", on_closing)  # 메인 윈도우의 닫기 프로토콜에 연결
    # ---------------------------------------------------------
    # Sub Frame
    # ---------------------------------------------------------
    def start_move(event, window):
        # event.x_root는 모니터 전체 기준 마우스 위치입니다. (절대 좌표)
        # 윈도우의 현재 위치와 마우스 위치의 차이(Offset)를 저장합니다.
        window.start_x = event.x_root - window.winfo_x()
        window.start_y = event.y_root - window.winfo_y()

        window.lift() # 선택시 상단 출력

    def on_drag(event, window): # 마우스가 움직인 절대 좌표에서, 아까 저장한 차이만큼 뺍니다.
        x = event.x_root - window.start_x
        y = event.y_root - window.start_y

        # --- 가두리(Clamping) 로직 ---
        parent = window.master
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        window_w = window.winfo_width()
        window_h = window.winfo_height()

        if x < 0: x = 0
        if y < 0: y = 0
        if x + window_w > parent_w: x = parent_w - window_w
        if y + window_h > parent_h: y = parent_h - window_h

        window.place(x=x, y=y)
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
        def check_db(conn, status):
            try:
                with conn.cursor() as cursor:
                    cursor.execute("select 1")
                    status = "Connected"
                    print("DB Connect Check : Connected")
                    return status
            except Exception as e:
                print(e)
                status = "Disconnected"
                return status

        if check_db(conn, status) == "Connected":
            status_color = "green"
        else:
            status_color = "red"
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
        tkinter.Label(content_frame, text=check_db(conn, status), fg=status_color, bg="white").grid(row=3, column=1, pady=5, sticky="w")
        # -- Click Event --
        content_frame.bind("<Button-1>", lambda e: current_status.lift())
        for widget in content_frame.winfo_children(): # 클릭 시 상단 표시, 하위 계층 전파
            widget.bind("<Button-1>", lambda e: current_status.lift(), add="+")
        title_bar.bind("<Button-1>", lambda e:start_move(e, current_status))
        title_bar.bind("<B1-Motion>", lambda e:on_drag(e, current_status))
        title_label.bind("<Button-1>", lambda e:start_move(e,current_status))
        title_label.bind("<B1-Motion>", lambda e:on_drag(e, current_status))
    # ---------------------------------------------------------
    # Sub Frame (Search_Customer)
    # ---------------------------------------------------------
    def close_search_customer_frame(event=None):
        global current_search_customer
        current_search_customer.destroy()
        current_search_customer = None

    def search_customer_frame():
        global current_search_customer
        if current_search_customer is not None:
            current_search_customer.lift()
            return
        # -- Frame --
        search_customer_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
        search_customer_frame.place(x=30, y=30)
        current_search_customer = search_customer_frame
        # -- Title Bar --
        title_bar = tkinter.Frame(current_search_customer, bg="#2c3e50", height=30)
        title_bar.pack(fill="x", side="top")
        title_label = tkinter.Label(title_bar, text="Customer", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
        title_label.pack(side="left", padx=5)
        # -- Close --
        close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", close_search_customer_frame)
        # -- Body --
        content_frame = tkinter.Frame(current_search_customer, bg="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
        tkinter.Entry(content_frame).pack(pady=5)
        tkinter.Button(content_frame, text="검색").pack(pady=5)
        # -- Click Event --
        content_frame.bind("<Button-1>", lambda e: current_search_customer.lift())
        for widget in content_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: current_search_customer.lift(), add="+")
        title_bar.bind("<Button-1>", lambda e:start_move(e, current_search_customer))
        title_bar.bind("<B1-Motion>", lambda e:on_drag(e, current_search_customer))
        title_label.bind("<Button-1>", lambda e:start_move(e, current_search_customer))
        title_label.bind("<B1-Motion>", lambda e:on_drag(e, current_search_customer))
    # ---------------------------------------------------------
    # Sub Frame (Search_Inventory)
    # ---------------------------------------------------------
    def close_search_inventory_frame(event=None):
        global current_search_inventory
        current_search_inventory.destroy()
        current_search_inventory = None

    def search_inventory_frame():
        global current_search_inventory
        if current_search_inventory is not None:
            current_search_inventory.lift()
            return
        # -- Frame --
        search_inventory_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
        search_inventory_frame.place(x=30, y=30)
        current_search_inventory = search_inventory_frame
        # -- Title Bar --
        title_bar = tkinter.Frame(current_search_inventory, bg="#2c3e50", height=30)
        title_bar.pack(fill="x", side="top")
        title_label = tkinter.Label(title_bar, text="Inventory", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
        title_label.pack(side="left", padx=5)
        title_label.bind("<Button-1>", current_search_inventory.lift)
        # -- Close --
        close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", close_search_inventory_frame)
        # -- Body --
        content_frame = tkinter.Frame(current_search_inventory, bg="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
        tkinter.Entry(content_frame).pack(pady=5)
        tkinter.Button(content_frame, text="검색").pack(pady=5)
        # -- Click Event --
        content_frame.bind("<Button-1>", lambda e: current_search_inventory.lift())
        for widget in content_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: current_search_inventory.lift(), add="+")
        title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_inventory))
        title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_inventory))
        title_label.bind("<Button-1>", lambda e: start_move(e, current_search_inventory))
        title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_inventory))
    # ---------------------------------------------------------
    # Sub Frame (Search_Film)
    # ---------------------------------------------------------
    def close_search_film_frame(event=None):
        global current_search_film
        current_search_film.destroy()
        current_search_film = None

    def search_film_frame():
        global current_search_film
        if current_search_film is not None:
            current_search_film.lift()
            return
        # -- Frame --
        search_film_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
        search_film_frame.place(x=30, y=30)
        current_search_film = search_film_frame
        # -- Title Bar --
        title_bar = tkinter.Frame(current_search_film, bg="#2c3e50", height=30)
        title_bar.pack(fill="x", side="top")
        title_label = tkinter.Label(title_bar, text="Film", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
        title_label.pack(side="left", padx=5)
        title_label.bind("<Button-1>", current_search_film.lift)
        # -- Close --
        close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", close_search_film_frame)
        # -- Body --
        content_frame = tkinter.Frame(current_search_film, bg="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
        tkinter.Entry(content_frame).pack(pady=5)
        tkinter.Button(content_frame, text="검색").pack(pady=5)
        # -- Click Event --
        content_frame.bind("<Button-1>", lambda e: current_search_film.lift())
        for widget in content_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: current_search_film.lift(), add="+")
        title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_film))
        title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_film))
        title_label.bind("<Button-1>", lambda e: start_move(e, current_search_film))
        title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_film))
    # ---------------------------------------------------------
    # Sub Frame (Search_Rental)
    # ---------------------------------------------------------
    def close_search_rental_frame(event=None):
        global current_search_rental
        current_search_rental.destroy()
        current_search_rental = None

    def search_rental_frame():
        global current_search_rental
        if current_search_rental is not None:
            current_search_rental.lift()
            return
        # -- Frame --
        search_rental_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
        search_rental_frame.place(x=30, y=30)
        current_search_rental = search_rental_frame
        # -- Title Bar --
        title_bar = tkinter.Frame(current_search_rental, bg="#2c3e50", height=30)
        title_bar.pack(fill="x", side="top")
        title_label = tkinter.Label(title_bar, text="Rental", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
        title_label.pack(side="left", padx=5)
        title_label.bind("<Button-1>", current_search_rental.lift)
        # -- Close --
        close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", close_search_rental_frame)
        # -- Body --
        content_frame = tkinter.Frame(current_search_rental, bg="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
        tkinter.Entry(content_frame).pack(pady=5)
        tkinter.Button(content_frame, text="검색").pack(pady=5)
        # -- Click Event --
        content_frame.bind("<Button-1>", lambda e: current_search_rental.lift())
        for widget in content_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: current_search_rental.lift(), add="+")
        title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_rental))
        title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_rental))
        title_label.bind("<Button-1>", lambda e: start_move(e, current_search_rental))
        title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_rental))
    # ---------------------------------------------------------
    # Sub Frame (Search_Payment)
    # ---------------------------------------------------------
    def close_search_payment_frame(event=None):
        global current_search_payment
        current_search_payment.destroy()
        current_search_payment = None

    def search_payment_frame():
        global current_search_payment
        if current_search_payment is not None:
            current_search_payment.lift()
            return
        # -- Frame --
        search_payment_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
        search_payment_frame.place(x=30, y=30)
        current_search_payment = search_payment_frame
        # -- Title Bar --
        title_bar = tkinter.Frame(current_search_payment, bg="#2c3e50", height=30)
        title_bar.pack(fill="x", side="top")
        title_label = tkinter.Label(title_bar, text="Payment", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
        title_label.pack(side="left", padx=5)
        title_label.bind("<Button-1>", current_search_payment.lift)
        # -- Close --
        close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", close_search_payment_frame)
        # -- Body --
        content_frame = tkinter.Frame(current_search_payment, bg="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
        tkinter.Entry(content_frame).pack(pady=5)
        tkinter.Button(content_frame, text="검색").pack(pady=5)
        # -- Click Event --
        content_frame.bind("<Button-1>", lambda e: current_search_payment.lift())
        for widget in content_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: current_search_payment.lift(), add="+")
        title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_payment))
        title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_payment))
        title_label.bind("<Button-1>", lambda e: start_move(e, current_search_payment))
        title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_payment))
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
    menu2.add_command(label="고객")
    menu2.add_separator()
    menu2.add_command(label="재고", command=search_inventory_frame)
    menu2.add_separator()
    menu2.add_command(label="영화", command=search_film_frame)
    menu2.add_separator()
    menu2.add_command(label="대여", command=search_rental_frame)
    menu2.add_separator()
    menu2.add_command(label="결제", command=search_payment_frame)
    menubar.add_cascade(label="조회", menu=menu2)
    # -- Menubar 3 --
    menu3 = tkinter.Menu(menubar, tearoff=0)
    menu3.add_command(label="고객")
    menu3.add_separator()
    menu3.add_command(label="재고")
    menu3.add_separator()
    menu3.add_command(label="영화")
    menu3.add_separator()
    menu3.add_command(label="대여")
    menu3.add_separator()
    menu3.add_command(label="결제")
    menubar.add_cascade(label="변경", menu=menu3)
    # -- Menubar 4 --
    menu4 = tkinter.Menu(menubar, tearoff=0)
    menu4.add_command(label="고객")
    menu4.add_separator()
    menu4.add_command(label="재고")
    menu4.add_separator()
    menu4.add_command(label="영화")
    menu4.add_separator()
    menu4.add_command(label="대여")
    menu4.add_separator()
    menu4.add_command(label="결제")
    menubar.add_cascade(label="삭제", menu=menu4)
    # -- Menubar 5 --
    menu5 = tkinter.Menu(menubar, tearoff=0)
    menu5.add_command(label="고객")
    menu5.add_separator()
    menu5.add_command(label="재고")
    menu5.add_separator()
    menu5.add_command(label="영화")
    menu5.add_separator()
    menu5.add_command(label="배우")
    menu5.add_separator()
    menu5.add_command(label="장르")
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
    def connect_test(conn):
        try:
            print("Test Connected 5s")
            with conn.cursor() as cursor:
                cursor.execute("select 1")
            print("DB Connect Test : Connected")
        except Exception as e:
            print(f"Error: {e}")
            if messagebox.askokcancel("Error", "Disconnected\nRestart?"):
                main.destroy()
                from db_connect import run_db_connect
                os.system("python db_connect.py")
                print("Restart DB Connect")
                return  # 재시작했으면 더 이상 예약하지 않고 종료
        if main.winfo_exists():  # 창이 켜져 있을 때만 예약
            main.after(5000, lambda: connect_test(conn))
    # ---------------------------------------------------------
    connect_test(conn)
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