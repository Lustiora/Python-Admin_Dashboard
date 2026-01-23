import psycopg2 # postgresql Connect Module
from datetime import datetime, timedelta # Date Module

def connect_db(): # DB 접속 정의
    conn = None  # conn의 기본값 선언
    count = 3  # count의 기본값 선언
    while count > 0:  # count값이 0이 보다 클때까지 반복
        print("-" * 50)
        print("please enter your username :")
        username = input() or "lus"  # ID 입력란
        print("-" * 50)
        print("please enter your password :")
        user_password = input() or "tiger"  # PW 입력란
        count = count - 1  # 입력마다 count 감소 -1
        try:
            # 연결 함수가 성공해서 반환값을 주면, conn은 더 이상 None이 아님
            conn = psycopg2.connect(dbname='DVD Rental',
                                    host='localhost',
                                    port='5432',
                                    user=username,  # 입력된 ID가 작성되는곳
                                    password=user_password)  # 입력된 PW가 작성되는곳
            print("-" * 50)
            print("connection established")  # 연결 성공시 출력
            break  # 연결 성공시 while 탈출
        except:  # 실패시
            print("Not Connect")  # 실패시 출력
    if count == 0 and conn is None:  # Count값 0 , conn값 None 시
        print("ID / PW Error")  # 출력
    return conn

def check_customers(conn): # 고객 확인 정의
    cursor = conn.cursor()
    scan = 1
    while scan > 0:
        print("-" * 50)
        print("Scan customer ID or Quit > 'q'")
        customer = input().strip()  # 입력란에 strip()를 추가하여 앞뒤 공백 제거하고 제출
        if customer == 'q':  # 종료 커맨트 지정
            return None, None
        try:
            cursor.execute("select * from customer where customer_id = %s", (customer,))  # DB에 질의 전송 , customer_id 존재여부
            customer_data = cursor.fetchone()  # 결과 데이터 가져오기 cursor.fetchone()
            if customer_data:  # 쿼리값 존재시
                return customer, customer_data
            else:  # 쿼리값 미존재시
                print("-" * 50)
                print(f"Not Customer ID {customer}")
        except Exception as e:  # 에러 체크
            print(f"Error: {e}")
            conn.rollback()  # 에러 발생시 롤백
            print("---Rolled Back---")
    return None, None

def process_return(conn,customer): # 반납 정의
    cursor = conn.cursor()
    cursor.execute("select * from rental where customer_id = %s and return_date is null",(customer,))  # 조회된 customer_id의 return_date 여부 조회
    rental_data = cursor.fetchone()
    if rental_data:  # return_date is null
        today = datetime.now().date()
        print("-" * 50)
        print("Please Return DVD")
        cursor.execute("""
                       select 
                           r.customer_id, f.title, r.rental_date, f.rental_rate
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
        print(f"\nTotal Charge : {total_charge:.2f}")
        print("-" * 50)
        return True
    else:
        return False

def process_rental(conn): # 대여 정의
    cursor = conn.cursor()
    scan = 1
    rental_cart = []
    total_fee = 0
    while scan > 0:
        print("-" * 50)
        print("Please DVD Barcode or Quit > 'q'")
        barcode = input().strip()
        if barcode == 'q': break
        try:
            cursor.execute("""SELECT inventory.inventory_id, film.title, film.rental_rate
                              FROM inventory
                                       INNER JOIN film ON inventory.film_id = film.film_id
                              WHERE inventory.inventory_id = %s""", (barcode,))
            dvd_data = cursor.fetchone()
            if dvd_data:
                today = datetime.now().date()  # 현재 날짜
                print("-" * 50)
                print("Please Rental Date (1 , 3 , 7) :")
                while scan > 0:
                    input_date = input().strip()
                    if input_date in ['1', '3', '7']:  # 1 , 3 , 7 강제
                        rental = int(input_date)  # 입력받은 값을 int로 변환
                        break
                    else:
                        print("-" * 50)
                        print("Please Rental Date (1 , 3 , 7) :")
                rental_days = timedelta(days=rental)  # timedelta 함수를 사용하여 rental_days을 days로 지정
                rental_fee = dvd_data[2] * rental
                inventory_id = dvd_data[0]
                return_date = today + rental_days
                rental_date = today
                title = dvd_data[1]
                print("-" * 50)
                print(
                    f"Barcode : {inventory_id} | Title : {title} | Rental : {dvd_data[2]}") # Query Column 기반 위치에 따른 값 출력
                print(
                    f"\nToday : {rental_date} | Return Date : {return_date} | Rental : {rental_fee}") # today와 timedelta 변환된 rental_days 합산하여 Return Date 출력
                rental_cart.append((inventory_id, title, rental_date, rental_fee)) # 출력이 필요한 정보 포장
                total_fee += rental_fee # 대여료 합산
                # return inventory_id , rental_date , return_date
            else:
                print("Not DVD Barcode")
        except Exception as e:  # 에러 체크
            print(f"Error: {e}")
            print("-" * 50)
            conn.rollback()  # 에러 발생시 롤백
            print("---Rolled Back---")
    if rental_cart:
        print("-" * 50)
        print("<-- Title --> | <-- Rental -->")
        for item in rental_cart:
            print(f"Title : {item[1]} | Rental : {item[3]}")
        print(f"\nTotal Fee : {total_fee}")
        return rental_cart , total_fee
    return None , 0

conn = connect_db() # DB 접속

while True:
    customer, customer_data = check_customers(conn) # 고객정보 호출 (기본화면)
    if customer is None: # 받은 값 = None 종료
        break
    is_return = process_return(conn, customer) # 고객의 미반납 이력 확인
    if is_return:
        input("Return Fee Calculation : (Enter)") # 연체료 납입을 확인
    else:
        rental_cart , total_fee = process_rental(conn) # 대여 정보 출력
        if total_fee:
            input(f"Rental Fee Calculation : (Enter)") # 대여료 납입을 확인

conn.close() # DB 접속 종료