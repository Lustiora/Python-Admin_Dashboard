import psycopg2 # postgresql Connect Module
from datetime import datetime, timedelta # Date Module

conn = None # conn의 기본값 선언
count = 3 # count의 기본값 선언

while count > 0: # count값이 0이 보다 클때까지 반복
    print("please enter your username :")
    username = input() or "lus"# ID 입력란
    print("please enter your password :")
    user_password = input() or "tiger"# PW 입력란
    count = count - 1 # 입력마다 count 감소 -1
    try:
        # 연결 함수가 성공해서 반환값을 주면, conn은 더 이상 None이 아님
        conn = psycopg2.connect(dbname='DVD Rental',
                                host='localhost',
                                port='5432',
                                user=username, # 입력된 ID가 작성되는곳
                                password=user_password) # 입력된 PW가 작성되는곳
        print("connection established") # 연결 성공시 출력
        break # 연결 성공시 while 탈출
    except: # 실패시
        print("Not Connect") # 실패시 출력
if count == 0 and conn is None: # Count값 0 , conn값 None 시
    print("ID / PW Error") # 출력

cursor = conn.cursor()
scan = 1

while scan > 0:
    print("Scan, customer ID :")
    customer = input().strip() # 입력란에 strip()를 추가하여 앞뒤 공백 제거하고 제출
    try:
        cursor.execute("select * from customer where customer_id = %s", (customer, )) # DB에 질의 전송 , customer_id 존재여부
        customer_data = cursor.fetchone() # 결과 데이터 가져오기 cursor.fetchone()
        if customer_data: # 쿼리값 존재시
            # print(f"customer ID : {customer}")
            cursor.execute("select * from rental where customer_id = %s and return_date is null", (customer,)) # 조회된 customer_id의 return_date 여부 조회
            rental_data = cursor.fetchone()
            if rental_data: # return_date is null
                today = datetime.now().date()
                print("Please Return DVD")
                cursor.execute("""select r.customer_id , f.title , r.rental_date , f.rental_rate 
                                  from rental r 
                                  inner join inventory i 
                                      on r.inventory_id = i.inventory_id 
                                  inner join film f 
                                      on i.film_id = f.film_id
                                  where customer_id = %s 
                                  and r.return_date is null""", (customer,))
                return_dvd = cursor.fetchall()
                total_rate = 0
                for dvdbarcode in return_dvd:
                    return_date = dvdbarcode[2].date()
                    all_rate = float((today - return_date).days * dvdbarcode[3]) * float(1.1)
                    total_rate += all_rate # 전체값 누적
                    print(
                        f"Customer Id : {dvdbarcode[0]} | "
                        f"Title : {dvdbarcode[1]} | "
                        f"Rental Date : {(today - return_date).days} days | "
                        f"Over Rate : {all_rate:.2f}") # 소수점 2번째 자리까지만 출력 :.2f
                print(f"Total Rate : {total_rate:.2f}")
                break
            else: # return_date is not null
                # print("Rental Please")
                # DVD를 스캔하여 자사의 상품인지 조회필요
                while scan > 0:
                    print("Please DVD Barcode")
                    dvdbarcode = input().strip()
                    try:
                        cursor.execute("""SELECT inventory.inventory_id, film.title, film.rental_rate
                                        FROM inventory
                                        INNER JOIN film ON inventory.film_id = film.film_id
                                        WHERE inventory.inventory_id = %s""", (dvdbarcode, ))
                        dvd_data = cursor.fetchone()
                        if dvd_data:
                            today = datetime.now().date() # 현재 날짜
                            print("Please Rental Date (1 , 3 , 7) :")
                            while scan > 0:
                                input_Date = input().strip()
                                if input_Date in ['1' , '3' , '7']: # 1 , 3 , 7 강제
                                    rental = int(input_Date) # 입력받은 값을 int로 변환
                                    break
                                else:
                                    print("Please Rental Date (1 , 3 , 7) :")
                            rental_days = timedelta(days=rental) # timedelta 함수를 사용하여 rental_days을 days로 지정
                            rental_rate = dvd_data[2] * rental
                            print(f"Barcode : {dvd_data[0]} | Title : {dvd_data[1]} | Rate : {dvd_data[2]}")  # Query Column 기반 위치에 따른 값 출력
                            print(f"Today : {today} Return Date : {today + rental_days} Rate : {rental_rate}") # today와 timedelta 변환된 rental_days 합산하여 Return Date 출력
                            break
                        else:
                            print("---존재하지않는 바코드---")
                    except Exception as e:  # 에러 체크
                        print(f"Error: {e}")
                        print("---------------")
                        conn.rollback()  # 에러 발생시 롤백
                        print("---Rolled Back---")
                break
        else: # 쿼리값 미존재시
            print(f"Not Customer ID {customer}")
    except Exception as e: # 에러 체크
        print(f"Error: {e}")
        print("---------------")
        conn.rollback() # 에러 발생시 롤백
        print("---Rolled Back---")
