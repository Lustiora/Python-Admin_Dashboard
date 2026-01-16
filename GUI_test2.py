# ---------------------------------------------------------
# 1. Import Package (맨 위)
# ---------------------------------------------------------
import tkinter # Python 기본 GUI Package
from tkinter import messagebox # 팝업창 GUI Package
import psycopg2  # postgresql Connect Package
from tkinter import scrolledtext # Log Window Print Package
from tkinter import simpledialog # Number 팝업창 Window Print Package
from datetime import datetime, timedelta # Date Module

# ---------------------------------------------------------
# 2. 전역 설정 및 Helper Module (도구들)
# ---------------------------------------------------------
def center_window(window, width, height): # Window 자동 중앙 정렬 모듈 (미정렬 시 좌측 상단) (tkinter)
    screen_width = window.winfo_screenwidth() # 현재 모니터의 해상도(크기)를 가져옴
    screen_height = window.winfo_screenheight()
    x_pos = (screen_width // 2) - (width // 2) # 정중앙 좌표 계산 \ (//)는 정수 나누기
    y_pos = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}") # 위치 적용 (가로x세로+X좌표+Y좌표)
    window.resizable(False, False) # Window Size 변동 금지 (가로, 세로)
# 적용 > center_window([tkinter Window],[width],[height])

# ---------------------------------------------------------
# 3. Main Window Module (핵심 기능)
# ---------------------------------------------------------
def run_main(conn):
    # [3-1] 메인 윈도우 초기 설정
    global current_customer_id # 전역 변수로 지정하여 입력 여부 확인
    current_customer_id = None # 변수값 지정
    main = tkinter.Tk()
    main.title("Sakila Manager")
    center_window(main, 700, 400)

    # [3-2] 입력값 검사 모듈 (Validation)
    def check_digit(incoming): # incoming: 사용자가 입력을 마친 후의 '결과값' (%P)
        if incoming.isdigit() or incoming == "": # 숫자이거나, 다 지워서 빈칸("")이면 -> 허용(True)
            return True
        else:
            return False
    validation = main.register(check_digit) # Entry 위젯의 validatecommand에 파이썬 함수를 연결하기 위해 Tcl 명령어로 등록

    # [3-3] 기능 함수들 (Logic)
    def search_db(event=None): # 고객 조회 모듈
        global current_customer_id
        global rental_cart
        global total_fee
        global total_charge
        rental_cart = []
        total_fee = 0
        total_charge = 0
        current_customer_id = None
        customer = customer_date.get() # .get().strip() > 입력받은 customer_date를 가져오고 앞뒤 공백 제거 > 앞뒤 공백 제거 부분은 검사 모듈과 겹치기에 삭제
        print(f"Customer ID Check ... {customer}")
        cursor = conn.cursor()
        log_area.configure(state="normal")
        try:
            cursor.execute("""  select c.customer_id , c.first_name||' '||c.last_name as Name, c.email 
                                from customer c
                                where c.customer_id = %s  """, (customer,))  # DB에 질의 전송 , customer_id 존재여부
            customer_data = cursor.fetchone()  # 결과 데이터 가져오기 cursor.fetchone()
            log_area.delete(1.0, tkinter.END) # 로그창 초기화
            if customer_data:  # 쿼리값 존재시
                log_area.insert(tkinter.END, "-" * 93 + f"\nID : {customer_data[0]} | Name : {customer_data[1]} | Email : {customer_data[2]}\n")
                process_return(conn,customer)
                current_customer_id = customer_data[0]
            else:  # 쿼리값 미존재시
                current_customer_id = None
                print(f"Customer Not Found {customer}")
                log_area.insert(tkinter.END, "Customer Not Found\n")
        except Exception as e:  # 에러 체크
            log_area.insert(tkinter.END, f"Customer Not Found {customer}\n")
            current_customer_id = None
            print(f"Error: {e}")
            conn.rollback()  # 에러 발생시 롤백
            print("---Rolled Back---")
        log_area.configure(state="disabled")

    def process_return(conn, customer):  # 반납 정의 모듈
        global total_charge
        cursor = conn.cursor()
        cursor.execute("select * from rental where customer_id = %s and return_date is null",(customer,))  # 조회된 customer_id의 return_date 여부 조회
        rental_data = cursor.fetchone()
        log_area.configure(state="normal")
        if rental_data:  # return_date is null
            today = datetime.now().date()
            print("-" * 93)
            print("Please Return DVD")
            log_area.insert(tkinter.END,"-" * 93 + "\nPlease Return DVD\n")
            cursor.execute(""" select r.customer_id, f.title, r.rental_date, f.rental_rate
                               from rental r 
                                    inner join inventory i on r.inventory_id = i.inventory_id
                                    inner join film f on i.film_id = f.film_id
                               where customer_id = %s
                                 and r.return_date is null """, (customer,))
            return_dvd = cursor.fetchall()
            total_charge = 0
            for barcode in return_dvd:
                return_date = barcode[2].date()
                all_charge = float((today - return_date).days * barcode[3]) * float(1.1)
                total_charge += all_charge  # 전체값 누적
                print(
                    f"Customer Id : {barcode[0]} | "
                    f"Title : {barcode[1]} | "
                    f"Rental Date : {(today - return_date).days} days | "
                    f"Charge : ${all_charge:.2f}")  # 소수점 2번째 자리까지만 출력 :.2f
                log_area.insert(tkinter.END,f"Title : {barcode[1]} | Rental Date : {(today - return_date).days} days | Charge : ${all_charge:.2f}\n")
            print(f"\nTotal Charge : ${total_charge:.2f}")
            log_area.insert(tkinter.END, f"\nTotal Charge : ${total_charge:.2f}\n")
            print("-" * 93)
            log_area.configure(state="disabled")
        else:
            print("-" * 93)
            print("Please DVD Barcode")
            log_area.insert(tkinter.END, "-" * 93 + "\nNo overdue items.\n")
            log_area.insert(tkinter.END, "-" * 93 + "\nPlease DVD Barcode.\n")
            log_area.configure(state="normal")

    def process_rental(event = None):  # 대여 정의 모듈
        global current_customer_id
        global rental_cart
        global total_fee
        global total_charge
        cursor = conn.cursor()
        barcode = dvd_barcode.get()
        rental = []
        log_area.configure(state="normal")
        if current_customer_id is None:
            print("Please Input Customer ID")
            log_area.insert(tkinter.END, "-" * 93 + "Please Input Customer ID\n")
            log_area.configure(state="disabled")
            customer_date.focus_set()
            dvd_barcode.delete(0, tkinter.END)  # dvd_barcode 입력값 삭제
            return
        if not barcode:
            print("-" * 93)
            print("Please Input Barcode")
            log_area.insert(tkinter.END, "-" * 93 +"Please Input Barcode\n")
            log_area.see(tkinter.END)
            dvd_barcode.focus_set()
            dvd_barcode.delete(0, tkinter.END)  # dvd_barcode 입력값 삭제
            return
        try:
            cursor.execute("""SELECT inventory.inventory_id, film.title, film.rental_rate
                              FROM inventory
                                       INNER JOIN film ON inventory.film_id = film.film_id
                              WHERE inventory.inventory_id = %s""", (barcode,))
            dvd_data = cursor.fetchone()
            today = datetime.now().date()  # 현재 날짜
            print("-" * 50)
            print("Please Rental Date (1 , 3 , 7) :")
            # input_date = input().strip()
            input_date = simpledialog.askinteger(title="Rental Date", parent=main, minvalue=1, maxvalue=7, prompt="Rental Date (1 , 3 , 7)")
            if input_date in [1 , 3 , 7]:  # 1 , 3 , 7 강제
                rental = input_date  # 입력받은 값을 int로 변환
            else:
                print("-" * 50)
                print("Please Rental Date (1 , 3 , 7) :")
                messagebox.showwarning("Warning", "Only 1, 3, 7 days allowed")
                dvd_barcode.focus_set()
            rental_days = timedelta(days=rental)  # timedelta 함수를 사용하여 rental_days을 days로 지정
            rental_fee = dvd_data[2] * rental
            inventory_id = dvd_data[0]
            return_date = today + rental_days
            rental_date = today
            title = dvd_data[1]
            total_fee += rental_fee  # 대여료 합산
            print("-" * 93)
            print(f"Barcode : {inventory_id} | Title : {title} | Rental : {dvd_data[2]}")  # Query Column 기반 위치에 따른 값 출력
            log_area.insert(tkinter.END, "-" * 93 + f"\nBarcode : {inventory_id} | Title : {title} | Rental : ${dvd_data[2]} x {rental}days | Total Fee : ${rental_fee}\n")
            log_area.see(tkinter.END)
            print(f"\nToday : {rental_date} | Return Date : {return_date} | Rental : ${rental_fee}")  # today와 timedelta 변환된 rental_days 합산하여 Return Date 출력
            rental_cart.append((inventory_id, title, rental_date, rental_fee))  # 출력이 필요한 정보 포장
            dvd_barcode.delete(0, tkinter.END)  # dvd_barcode 입력값 삭제
            dvd_barcode.focus_set()
        except Exception as e:  # 에러 체크
            log_area.insert(tkinter.END, "-" * 93 + "Not DVD Barcode\n")
            log_area.see(tkinter.END)
            dvd_barcode.delete(0, tkinter.END)  # dvd_barcode 입력값 삭제
            dvd_barcode.focus_set()
            print(f"Error: {e}")
            print("-" * 93)
            conn.rollback()  # 에러 발생시 롤백
            print("---Rolled Back---")
        log_area.configure(state="disabled")
        return None, 0

    def fee_calculation(event = None): # 정산 모듈
        global current_customer_id
        global total_fee
        global rental_cart
        global total_charge
        grand_total = float(total_fee) + float(total_charge)
        log_area.configure(state="normal")
        if rental_cart:
            print("-" * 93)
            print("<-- Title --> | <-- Rental -->")
            for item in rental_cart:
                print(f"Title : {item[1]} | Rental : {item[3]}")
                log_area.insert(tkinter.END, "-" * 93 + f"Title : {item[1]} | Rental : ${item[3]}\n")
                log_area.see(tkinter.END)
            print(f"\nTotal Fee : {total_fee}")
            log_area.insert(tkinter.END, "-" * 93 + f"\n\nTotal Fee : ${total_fee}\n\n" + "-" * 93)
            log_area.see(tkinter.END)
        if total_charge > 0:
            print("-" * 93)
            print(f"\nGrand Total : {grand_total}\n")
            log_area.insert(tkinter.END,f"\n\nGrand Fee : ${grand_total:.2f}\n\n" + "-" * 93)
            log_area.see(tkinter.END)
        print("-" * 93)
        print("Is the bill paid?")
        messagebox.showinfo("Calculation", "Is the bill paid?")
        print("-" * 93)
        print("Settlement Completed")
        log_area.delete(1.0, tkinter.END)  # 로그창 초기화

        # -- 결제 완료 및 저장 정보 초기화 --
        log_area.insert(tkinter.END,"Settlement Completed\n")
        log_area.configure(state="disabled")
        current_customer_id = None
        total_fee = 0
        total_charge = 0
        rental_cart = []

    # [3-4] 화면 GUI 구성 (Layout)

    # -- Customer Search Frame --
    search_frame = tkinter.LabelFrame(main, text="Customer Search")
    search_frame.pack(fill="x", padx=5, pady=5) # pack(fill="x") > width = 최대치
    tkinter.Label(search_frame, text="Customer ID :").pack(side="left", padx=5, pady=5) # grid 대신 pack 사용 / side="left" > 읽는 순서대로 좌측 정렬
    customer_date = tkinter.Entry(search_frame, validate="key", validatecommand=(validation, '%P')) # validate="key" > 입력값 상시확인 / validatecommand=(validation, '%P') > check_digit 모듈을 통과하는 입력값(%p)만 허용
    customer_date.pack(side="left", padx=5, pady=5)
    customer_date.bind("<Return>", search_db)
    tkinter.Button(search_frame, text="Search", command=search_db, takefocus=0).pack(side="left", padx=5, pady=5) # takefocus=0 > Tap Key 선택 제외

    # -- DVD Search Frame --
    tkinter.Button(search_frame, text="Search", command=process_rental, takefocus=0).pack(side="right", padx=5, pady=5)
    dvd_barcode = tkinter.Entry(search_frame, validate="key", validatecommand=(validation, '%P')) # validate="key" > 입력값 상시확인 / validatecommand=(validation, '%P') > check_digit 모듈을 통과하는 입력값(%p)만 허용
    dvd_barcode.pack(side="right", padx=5, pady=5)
    dvd_barcode.bind("<Return>", process_rental)
    tkinter.Label(search_frame, text="DVD Barcode :").pack(side="right", padx=5, pady=5) # grid 대신 pack 사용 / side="left" > 읽는 순서대로 좌측 정렬

    # -- Log Frame --
    log_frame = tkinter.LabelFrame(main, text="Customer Details")
    log_frame.pack(fill="both", expand=True, padx=5, pady=5) # fill="both", expand=True > 잔여 공간 전부 할당
    log_area = scrolledtext.ScrolledText(log_frame, height=10, state="disabled") # Log 출력 공간
    log_area.pack(fill="both", expand=True, padx=5, pady=5)

    # -- Calculation Frame --
    calculation = tkinter.LabelFrame(main)
    calculation.pack(fill="x", padx=5, pady=5)
    calculation_key = tkinter.Button(calculation, text="Calculation", width=500, command=fee_calculation)
    calculation_key.pack(padx=5, pady=5)
    calculation_key.bind("<Return>", fee_calculation)

    # [3-5] 초기 포커스 및 실행
    def on_closing(): # DB 유령 연결 방지 모듈
        if messagebox.askokcancel("Quit", "Exit?"):
            conn.close()  # DB 연결 끊기 (유령 연결 방지)
            main.destroy()
    main.protocol("WM_DELETE_WINDOW", on_closing)  # 메인 윈도우의 닫기 프로토콜에 연결

    def set_focus_force(): # 포커스 강제 조정
        main.lift()  # 창을 화면 맨 앞으로
        main.attributes('-topmost', True)  # 잠시동안 창을 최상위로 고정
        main.attributes('-topmost', False)  # 고정 해제 (안 그러면 다른 창이 안 덮임)
        customer_date.focus_force()  # 입력창 강제 포커스
    main.after(200, set_focus_force) # 0.2초(200ms) 뒤에 실행 (화면이 다 그려질 시간 확보)
    main.mainloop()

# ---------------------------------------------------------
# 4. Login Window Module (진입점)
# ---------------------------------------------------------
count = 3
def user_login(event=None): # event=None을 추가하여 event값 입력 받음을 선언
    global count
    login_id = user_id.get()
    login_pw = user_pw.get()
    print(f"ID : {login_id} | PW : {login_pw}")
    print("DB Connected ...")
    count = count - 1
    try:
        # 연결 함수가 성공해서 반환값을 주면, conn은 더 이상 None이 아님
        conn = psycopg2.connect(dbname='DVD Rental',
                                host='192.168.0.44', # Kosmo Computer IP
                                port='5432',
                                user=login_id,  # 입력된 ID가 작성되는곳
                                password=login_pw)  # 입력된 PW가 작성되는곳
        print("Connection Established")  # 연결 성공시 출력
        login.destroy()
        run_main(conn)
    except:  # 실패시
        print(f"Login Failed | Chance(3) : {count}")
        messagebox.showinfo("Login", f"Login Failed\nChance(3) : {count}")
        if count == 0:
            messagebox.showinfo("Login", "Please Contact the Administrator")
            print("Not Connected")
            login.destroy()

# ---------------------------------------------------------
# 5. 실행부 (Application Start)
# ---------------------------------------------------------
# -- Login (Window) --
if __name__ == "__main__": # 해당 py를 import하여 사용 시 Login (Window) 출력 방지
    login = tkinter.Tk() # 표사되는 Window(tkinter.Tk())에 변수명을 지정하여 변수명을 기준으로 속성을 추가
    login.title("Sakila Login")
    center_window(login, 260, 100)

# -- Login GUI --
tkinter.Label(login, text="Username").grid(row=0, column=0, padx=5, pady=5, sticky="e")
user_id = tkinter.Entry(login) # Entry -> 입력칸 | 입력된 값을 사용하기 위해 변수명 지정 필요
user_id.grid(row=0, column=1, padx=10, pady=5)
login.grid_columnconfigure(0, weight=1) # ([열],[배당 비율])
tkinter.Label(login, text="Password").grid(row=1, column=0, padx=5, pady=5, sticky="e")
user_pw = tkinter.Entry(login, show="*") # show="*" > 유출 방지 : 입력값 * 대체 출력
user_pw.grid(row=1, column=1, padx=10, pady=5)
user_pw.bind("<Return>", user_login) # Enter key 입력으로 Login 모듈 동작 ("[입력키]", [모듈])
login.grid_columnconfigure(1, weight=1)
login_but = (tkinter.Button(login, text="Login", command=user_login))
login_but.grid(row=2, column=0, columnspan=2, padx=10, pady=3, sticky="ew") # command=[클릭시 동작내용] | sticky="e" > 우측 정렬
login_but.bind("<Return>", user_login)
# row=[행], column=[열]) > 0행 0열 = 좌측 상단 / 행과 열이 겹치는 경우 덮어씌워짐 | padx=[좌측우측외부여백], pady=[상단하단외부여백], ipa~=[내부여백]
# 상세 정리 : https://puliseul.tistory.com/81

user_id.focus_set() # 실행 시 user_id 포커스 지정
login.mainloop() # root(Window)를 지속적으로 반복 실행 (종료방지)