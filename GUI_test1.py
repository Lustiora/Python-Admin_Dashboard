import tkinter # Python 기본 GUI Package
from tkinter import messagebox # 팝업창 GUI Package
import psycopg2  # postgresql Connect Package
from tkinter import scrolledtext # Log Window Print Package
from datetime import datetime, timedelta # Date Module
######################################
# Login 모듈 (from tkinter import messagebox)
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
######################################
# Window (Main) 모듈 (tkinter)
def run_main(conn):
    main = tkinter.Tk()
    main.title("Sakila DB")
    center_window(main, 700, 400)
    ######################################
    # 입력값 검사 모듈
    def check_digit(incoming): # incoming: 사용자가 입력을 마친 후의 '결과값' (%P)
        if incoming.isdigit() or incoming == "": # 숫자이거나, 다 지워서 빈칸("")이면 -> 허용(True)
            return True
        else:
            return False
    validation = main.register(check_digit)
    ######################################
    # DB 조회 모듈
    def search_db(event=None):
        customer = customer_date.get() # .get().strip() > 입력받은 customer_date를 가져오고 앞뒤 공백 제거 > 앞뒤 공백 제거 부분은 검사 모듈과 겹치기에 삭제
        print(f"Customer ID Check ... {customer}")
        cursor = conn.cursor()
        log_area.configure(state="normal")
        try:
            cursor.execute("select c.customer_id , c.first_name||' '||c.last_name as Name, c.email from customer c where c.customer_id = %s", (customer,))  # DB에 질의 전송 , customer_id 존재여부
            customer_data = cursor.fetchone()  # 결과 데이터 가져오기 cursor.fetchone()
            log_area.delete(1.0, tkinter.END) # 로그창 초기화
            if customer_data:  # 쿼리값 존재시
                log_area.insert(tkinter.END, f"ID : {customer_data[0]} | Name : {customer_data[1]} | Email : {customer_data[2]}\n")
                process_return(conn,customer)
            else:  # 쿼리값 미존재시
                print(f"Customer Not Found {customer}")
                log_area.insert(tkinter.END, "Customer Not Found\n")
        except Exception as e:  # 에러 체크
            print(f"Error: {e}")
            conn.rollback()  # 에러 발생시 롤백
            print("---Rolled Back---")
        log_area.configure(state="disabled")
        ######################################
    def process_return(conn, customer):  # 반납 정의
        cursor = conn.cursor()
        cursor.execute("select * from rental where customer_id = %s and return_date is null",
                       (customer,))  # 조회된 customer_id의 return_date 여부 조회
        rental_data = cursor.fetchone()
        log_area.configure(state="normal")
        if rental_data:  # return_date is null
            today = datetime.now().date()
            print("-" * 50)
            print("Please Return DVD")
            log_area.insert(tkinter.END,"---------------------------------------------------------------------------------------------\n"
                                        "Please Return DVD\n")
            cursor.execute("""
                           select r.customer_id,
                                  f.title,
                                  r.rental_date,
                                  f.rental_rate
                           from rental r
                                    inner join inventory i
                                               on r.inventory_id = i.inventory_id
                                    inner join film f
                                               on i.film_id = f.film_id
                           where customer_id = %s
                             and r.return_date is null
                           """, (customer,))
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
                    f"Charge : {all_charge:.2f}")  # 소수점 2번째 자리까지만 출력 :.2f
                log_area.insert(tkinter.END,f"Title : {barcode[1]} | Rental Date : {(today - return_date).days} days | Charge : {all_charge:.2f}\n")
            print(f"\nTotal Charge : {total_charge:.2f}")
            log_area.insert(tkinter.END, f"\nTotal Charge : {total_charge:.2f}")
            print("-" * 50)
            log_area.configure(state="disabled")
    ######################################
    ### 화면 구성
    ## Customer Search
    search_frame = tkinter.LabelFrame(main, text="Customer Search")
    search_frame.pack(fill="x", padx=5, pady=5) # pack(fill="x") > width = 최대치
    tkinter.Label(search_frame, text="Customer ID :").pack(side="left", padx=5, pady=5) # grid 대신 pack 사용 / side="left" > 읽는 순서대로 좌측 정렬
    customer_date = tkinter.Entry(search_frame, validate="key", validatecommand=(validation, '%P'))
    # validate="key" > 입력값 상시확인 / validatecommand=(validation, '%P') > check_digit 모듈을 통과하는 입력값(%p)만 허용
    customer_date.pack(side="left", padx=5, pady=5)
    customer_date.bind("<Return>", search_db)
    tkinter.Button(search_frame, text="Search", command=search_db).pack(side="left", padx=5, pady=5)
    ######################################
    ## Log Area
    log_frame = tkinter.LabelFrame(main, text="Customer Details")
    log_frame.pack(fill="both", expand=True, padx=5, pady=5) # fill="both", expand=True > 잔여 공간 전부 할당
    log_area = scrolledtext.ScrolledText(log_frame, height=10, state="disabled") # Log 출력 공간
    log_area.pack(fill="both", expand=True, padx=5, pady=5)
    ######################################
    # DB 조회 종료창 모듈
    def on_closing():
        if messagebox.askokcancel("Quit", "Exit?"):
            conn.close()  # DB 연결 끊기 (유령 연결 방지)
            main.destroy()
    # 메인 윈도우의 닫기 프로토콜에 연결
    main.protocol("WM_DELETE_WINDOW", on_closing)
    ######################################
    main.mainloop()
######################################
# Window 자동 중앙 정렬 모듈 (미정렬 시 좌측 상단) (tkinter)
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth() # 현재 모니터의 해상도(크기)를 가져옴
    screen_height = window.winfo_screenheight()
    x_pos = (screen_width // 2) - (width // 2) # 정중앙 좌표 계산 \ (//)는 정수 나누기
    y_pos = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}") # 위치 적용 (가로x세로+X좌표+Y좌표)
    window.resizable(False, False) # Window Size 변동 금지 (가로, 세로)
# 적용 > center_window([tkinter Window],[width],[height])
######################################
# 변수명 지정 없이 tkinter.Tk()로 작성하면 해당하는 속성이 포함된 창 3개가 출력
# tkinter.Tk().title("DVD")
# tkinter.Tk().geometry("500x500")
# tkinter.Tk().mainloop()
######################################
# tkinter Package 에서는 불가능한 방식 -> return self 없음 -> 한줄에 하나의 속성만 사용가능
# tkinter.Tk().title("PU").geometry("500x500").mainloop()
######################################
# Window (Login)
login = tkinter.Tk() # 표사되는 Window(tkinter.Tk())에 변수명을 지정하여 변수명을 기준으로 속성을 추가
login.title("Sakila Login")
center_window(login, 260, 100)
######################################
# Login 화면 구성 grid
tkinter.Label(login, text="Username").grid(row=0, column=0, padx=5, pady=5, sticky="e")
user_id = tkinter.Entry(login) # Entry -> 입력칸 | 입력된 값을 사용하기 위해 변수명 지정 필요
user_id.grid(row=0, column=1, padx=10, pady=5)
login.grid_columnconfigure(0, weight=1) # ([열],[배당 비율])
tkinter.Label(login, text="Password").grid(row=1, column=0, padx=5, pady=5, sticky="e")
user_pw = tkinter.Entry(login, show="*") # show="*" > 유출 방지 : 입력값 * 대체 출력
user_pw.grid(row=1, column=1, padx=10, pady=5)
user_pw.bind("<Return>", user_login) # Enter key 입력으로 Login 모듈 동작 ("[입력키]", [모듈])
login.grid_columnconfigure(1, weight=1)
tkinter.Button(login, text="Login", command=user_login).grid(row=2, column=0, columnspan=2, padx=10, pady=3, sticky="ew") # command=[클릭시 동작내용] | sticky="e" > 우측 정렬
# row=[행], column=[열]) > 0행 0열 = 좌측 상단 / 행과 열이 겹치는 경우 덮어씌워짐
# padx=[좌측우측외부여백], pady=[상단하단외부여백], ipa~=[내부여백]
# 상세 정리 : https://puliseul.tistory.com/81
######################################
login.mainloop() # root(Window)를 지속적으로 반복 실행 (종료방지)
######################################