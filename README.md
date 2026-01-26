# Python-Sakila
> Sakila DB > Read POS (Point of Sales) Simulator

## Basic Logic 2.0

### 1. Login Logic

1. [x] **DB 연결정보를 확인**
    - 연결정보가 저장된 INI File 유무 확인
    - 화이트 리스트 [...\PostgreSQL\18\data\postgresql.conf, pg_hba.conf](https://github.com/Lustiora/Python-Sakila/wiki/PostgresSQL-Server-White-List)
        - ~DB Connect Count = **3**~
        - 1-1. 해당 정보로 연결시도
            - ~일치 print _DB Connect_ > `2`~
            - ~불일치 >> Count **-1** Print _Not Connected_~
                - ~Count == **0** Print _Please Contact the Administrator / Phone : 010-1234-5678_ _End_~
                - Count 제거 / 에러코드 출력으로도 충분
        <br>
        <img width="674" height="257" alt="스크린샷 2026-01-20 170736" src="https://github.com/user-attachments/assets/1e3ad08c-defb-48db-92ae-0b0bb70a7929" />

2. [x] **직원 ID를 확인 (Staff-Table)**
    - Login Count = **3**
    - DB (Staff Table)에 해당하는 로그인 정보(username, password, active == `True`) 확인
        - 일치 >> `DB Access`
        - 불일치 >> Count **-1** Print _Login Failed / Chance(Count)_
            - Count == **0** Print _Please Contact the Administrator / Phone : 010-1234-5678_ _End_
    <br>
    <img width="782" height="214" alt="스크린샷 2026-01-20 170512" src="https://github.com/user-attachments/assets/956b66f3-7f8f-4fae-9522-c4fc8bfb394e" />

### 2. Customer Check / Return / Rental / Calculation Logic

1. [ ] **회원 여부 확인 (Barcode) (Customer-Table)**
    - 1-1. 고객 ID를 확인 (customer_id)
        - 확인 `1 End`
        - 미확인 `1-2`
        - 미회원 `1-3`
    - 1-2. 고객 정보 검색 화면 출력
        - `first name` or `last name` or `email` Search Button
        - Columns `first name`, `last name`, `email`
            - 확인 `1-1`
            - 미확인 `1-2`
    - 1-3. 신규 고객 추가 (Customer-Table)
        - customer_id = Last customer_id +1 (DB -> SERIAL 혹은 SEQUENCE)
        - store_id = Connect Staff ID = store_id
        - first_name, last_name, email
        - address_id = Address-Table > Last address_id +1 (DB -> SERIAL 혹은 SEQUENCE) / New Rows

2. [ ] **재고 확인 (Barcode) (Inventory-Table)**
    - 2-1. 상품 Barcode 확인 (inventory_id, Connect Staff ID = store_id)
        - 확인 `2-2`
        - 미확인 `2-4`
    - 2-2. 상품 상태 확인
        - 대여중 inventory_id > Rental-Table > return_date is null
        - 대여가능 `2-3`
    - 2-3. 해당하는 Film 정보 출력 (film_id > Film-Table join Film_Category-Table join Category-Table > name) > `2 End`
        - Columns `film_id`, `title`, `rental_duration`, `rental_rate`, `rating`, `name`
    - 2-4. 재고 정보 검색 화면 출력 > `2-1`
        - Inventory-Table join Film-Table join Store-Table join Address-Table
        - `inventory_id` or `title(fulltext)` Search Button
        - Columns `inventory_id`, `title`, `story_id`, `city_id`, `address`, `phone`, `inventory (가용 / 전체)`
    - 2-5. 신규 재고 추가 (Inventory-Table)
        - inventory_id = Last inventory_id +1 (DB -> SERIAL 혹은 SEQUENCE)
        - film_id = 
            - 기존 Film이 있는경우 그대로 사용
            - 새로운 Film의 경우 `2-6`
    - 2-6. 신규 Film 추가 (Film-Table)
        - film_id = Last film_id +1 (DB -> SERIAL 혹은 SEQUENCE)
        - title = New title
        - description = New description
        - release_year = New release_year
        - language_id = Language-Table >= language_id
        - rental_duration = Default 3 or 
        - rental_rate = Default 4.99 or
        - length = New length
        - replacement_cost = Default 19.99 or
        - rating = G or PG or PG-13 or R or NC-17
        - category = Category-Table >= name
        - Film_Actor-Table
            - 존재하는 경우 해당하는 Actor 연결
            - 존재하지 않는 경우 `2-7`
    - 2-7. 신규 Actor 추가 (Actor-Table)
        - actor_id = Last actor_id +1 (DB -> SERIAL 혹은 SEQUENCE)
        - first_name , last_name

3. [ ] **반납 (Rental-Table)**
    - `1` = %s > customer_id = %s, return_date is null
        - Film List 출력 (film_id > Film-Table)
        - Columns `film_id`, `title`, `rental_rate`, `rental_date`, `return_date`, `replacement_cost`
            - ((`return_date` - 현재 날짜) <= 0) > 반납 > _End_
        - 연체
            - (`return_date` - 현재 날짜) > 0 // `over_rate` 추가 (+ 분실/손상 시 = + `replacement_cost`)
            - `over_rate` = (`return_date` - 현재 날짜) * (`rental_rate` / `rental_duration`) * 1.1
            - (반납 and `over_rate` + `5`) or (반납 + `4` + `over_rate` + `5`) > _End_

4. [ ] **대여 (Rental-Table) & 결제**
    - Rental-Table
        - `1` = %s // customer_id = %s (Customer-Table)
        - `2` > `5` or (Rental_Cart > `5`) else `2-2` Global Fee, Cart Reset, print _이미 대여중인 dvd입니다._
    - Payment-Table
        - payment_id = last payment_id +1 (DB -> SERIAL 혹은 SEQUENCE)
        - customer_id = `1`
        - staff_id = Connect Staff ID
        - rental_id = last rental_id +1 (DB -> SERIAL 혹은 SEQUENCE) (Rental-Table)
        - amount = 전체 결제 금액 (global fee) = (대여금액 (All `rental_rate`) + 연체금액 (All `over_rate`))
        - payment_date = 결제 일시
    - Rental-Table
        - rental_id = last rental_id +1 (DB -> SERIAL 혹은 SEQUENCE)
        - rental_date = 대여 일시
        - inventory_id = `2`
        - customer_id = `1`
        - return_date = `2`
        - staff_id = Connect Staff ID
    - 전체 과정 실패 시 `rollback`
    - _End_

### Window


1. [x] DB Connect Window `1`

    <img width="302" height="272" alt="스크린샷 2026-01-22 172642" src="https://github.com/user-attachments/assets/91d2e611-533d-43be-9b15-11bd2f6412e3" />

2. [x] Staff Login Window `2`

    -- Left `Tkinter` -- Middle `Custom Tkinter` & Dark Theme -- Right `Custom Tkinter` & Basic Theme --

    <img width="831" height="238" alt="Screenshot_20260124_142020" src="https://github.com/user-attachments/assets/98578567-67f3-49d1-b651-4901f262644b" />
    
3. [x] Main Window
    
    `Tkinter`
    <img width="1026" height="820" alt="스크린샷 2026-01-22 172434" src="https://github.com/user-attachments/assets/04d5c636-2aa7-487c-b883-01ac260df8c9" />
    
    `Custom Tkinter`
    <img width="1154" height="958" alt="Screenshot_20260124_145245" src="https://github.com/user-attachments/assets/3bdc3d49-7658-4f5d-a095-0d861697b2b0" />

    - Menubar
        - 메뉴
            - 상태 (DB 연결, 직원 정보)
            - 종료 _End_
        - 조회 & 변경 & 삭제
            - 고객 (Customer-Table)
            - 재고 (Inventory-Table)
            - 영화 (Film-Table) (C: fulltext)
            - 대여 (Rental-Table)
            - 결제 (Payment-Table)
        - 추가
            - 고객 (Customer-Table)
            - 재고 (Inventory-Table)
            - 영화 (Film-Table) (C: fulltext)
            - 배우 (Actor-Table)
            - 장르 (Category-Table)
        - 통계 (대여 / 반납 , 대여 Top 10 (영화, 장르, 등급 Count))
        - 관리
            - 직원 (Staff-Table)

### Old Basic Logic 1.0

<details>
<summary>...</summary>
<br>
<img width="271" height="141" alt="스크린샷 2026-01-20 165959" src="https://github.com/user-attachments/assets/2b732a9f-7eb9-4e53-b514-540f517ac469" />

<img width="707" height="437" alt="스크린샷 2026-01-20 170017" src="https://github.com/user-attachments/assets/c2ea61f9-b06a-44d9-9592-cf3a0bfa5a8e" />

1. **사용자 ID를 확인**
   - 1-1. 대여중/연체중인 DVD가 존재하는 경우 > **3-2**

2. **영화 DVD = inventory_id = 바코드 확인**
   - 확인되지 않는다면 날짜/시간, 확인되지 않는 DVD임을 로그로 기록 > **[종료]**

3. **대여 > 3-1 , 반납 > 3-2 을 확인하는 화면 출력**
   - **3-1. 대여의 경우**
     - 현재 날짜를 상단에 표시하고 중간 좌측에 대여 기간(a)을 선택사항으로 두고 우측에는 현재날짜 + 대여기간(a)을 합산한 만료일 출력
     - 하단에는 대여 버튼을 만들고 대여기간(a)이 선택되면 활성화/ 이전까지는 비활성화 > **3-1**
   - **3-2. 반납의 경우**
     - 현재 날짜를 상단에 표시하고 중간에 좌측에 연체 목록/만료 기간을 출력하고 우측에는 연체기간 표시(현재날짜-만료날짜)
     - 하단 좌측에 반납 버튼을 만들고 연체가 없는 경우 활성화 > 반납 후 **[종료]**
     - 하단 우측에는 연체가 있는 경우 연체 기간에 따른 연체료를 버튼으로 생성하여 활성화 > **3-2**

4. **[대여금액 및 연체료 표시]**
   - **4-1.** 대여기간(a)에 해당하는 대여금액(b)을 표시하고 하단에 전체 대여금액 표시,  복수의 DVD를 대여하는 경우 바코드를 확인 > **3-1**
   - **4-2.** 연체기간(C)에 해당하는 연체료(c x d)를 표시하고 하단에 전체 연체료 표시, 복수의 DVD를 연체한 경우 바코드를 확인 > **3-2**

5. **계산**

6. **[종료]**

<details>
<summary>Calculation Logic</summary>

> 대여료 및 연체료 산정 기준
* **a. Rental Period (대여 기간)**
  * Options: `1 Day`, `3 Day`, `7 Day`
* **b. Rental Rate (대여료)**
  * ~~Fixed: 1000, 2500, 5000~~ (Deprecated)
* **c. Overdue Base (연체료 산정 기준)**
  * Formula: `Original Cost(C) * 1 Day`
* **d. Penalty Multiplier (가산율)**
  * Factor: `1.1` (연체 시 1.1배 적용)

</details>

</details>

## Future Improvements

* Sakila DB를 재확인한 결과 상상이상으로 많은 데이터가 정리되어있음을 확인하여 **새로운 Logic의 필요성을 확인**
  * Old
    * 관리자확인 > 고객확인 > 대여이력확인 > 재고확인 > 결제
  * New
    * 대여 가능 기간, 그에 따른 대여 비용은 사전에 정의되어있음
    * 관리자확인을 대신하는 Staff Table
    * 특정 폴더에 로그와 psycopg2.connect 정보를 저장하는(이후 정보) ini 파일 생성
      * 실행시 특정 폴더에 정보 ini 파일이 없는 경우 로그인 Window 실행 전 psycopg2.connect 정보를 입력하는 Window 실행하고 저장 > (Host, User, ...)
      * 정보 ini 파일이 있는경우 바로 로그인 Window 실행 > (Staff Table)
    * 대여 정의 모듈에서 현재 대여 중인 dvd 의 경우 '이미 대여중인 dvd입니다.' 문구 출력 > 연체료, 대여료, 장바구니 초기화하여 결제 불가능하게 설정
    * Title Search Window 추가
      * Columns (Title , All Count , Rent Count , Rental available Count)
      * Search Window에 검색어 없이 검색하면 전체 목록이 출력
      * Title Name 일부를 검색하면 해당하는 목록이 출력
      * film table > fulltext column 사용
    * DB date 값 최신화 필요 (rental date 2006-02-14 / last return date 2005-09-02 |  + interval '19 year 11 month')
    * Log_area / tkinter GUI Change
      * [Flet](https://github.com/flet-dev/flet)
    * Rank Window > (현재 시간 기준 Week Rank, Month Rank, Year Rank) 추가
      * Columns (Rank , Title , Description (설명), Rating (관람등급), category(장르)(film > film_category > category Table)

## Workflow

* **2026-01-26**
  1. 기존 tkinter 구조에서 customtkinter로 변환하였으나 GUI 부분에서 아쉬운점이 많아 파기
  2. flet(0.28.3)을 사용하여 웹, 앱 호환성 해결을 위한 변환작업 진행중 (DB Connect > Main Window 연결 완료)
  <br>(0.80.3 >> Script End Monitor Brightness "0" Issue)
  <br>https://flet-controls-gallery.fly.dev/

<details>
<summary>Old Workflow</summary>

* **2026-01-23**
  1. Menubar Module 별도 py 분리 (Sub Frame search, change, delete, add)
  2. Window Module start_move, on_drag 이전
  3. Menubar Status_Frame Login Staff 표시 staff_login > main_window
  4. 차후 테마 적용을 위한 Theme 생성
  5. tkinter > customtkinter 변환

* **2026-01-22**
  1. Status Bar 구현 (DB 접속상태 5s 체크)
  2. Linux 호환 설정 DB Disconnect Restart Debug
  3. pyinstaller > Package Compile 
  ```bash
  pyinstaller -F -w -n Sakila_Basic_Logic_2_3 db_connect.py
  
  Linux 실행 성공
  Window 별도 Package Compile 필요 (pyinstaller Cross-Compile 지원하지 않음)
  ````
  4. Linux에서 재시작에 성공하고 Windows에서 실패하는 현상 debug (분기 추가)
  5. db_connect.py > config.ini 파일 유무에 따른 동작 로직 변경 (파일 존재시 바로 접속 시도)
  6. Windows EXE Compile Restart Error Debug > 파일 자체를 재실행 하는 방식으로 전환<br>
  ```bash
  # 원인
  Windows EXE 실행 시 임시폴더를 생성 후 해당 위치에 Compile된 EXE를 실행하는 방식이었으나
  Restart Logic 실행 시
  Windows는 프로그램이 종료되었다고 생각하여 임시폴더를 삭제하고 환경변수, 임시폴더위치는 상속되어
  실행되지 않고 에러 발생
  
  Linux Compile Test >> Clear
  ```
  7. Windows Sandbox Test >> **Clear** 

* **2026-01-21**
  1. Main Window Menubar Create
  2. Sub Window Frame 구현중
  3. Status Bar 구현중 (DB 접속상태 체크)
  4. DB Connect 5s Test, Disconnect > db_connect.py link Logic 추가
  5. Linux 호환 설정 추가 <br>
      ```bash
      import sys <br>
      if sys.platform == "win32": appdata = os.getenv("APPDATA") # Window의 경우<br>
      else: appdata = os.path.expanduser("~/.config") # Linux의 경우
      ```
  6. Window Array Middle Debug

* **2026-01-20**
  1. DB Connect Debug
  2. DB Connect GUI > Staff Login GUI Connect
  3. Main Window Create

* **2026-01-19**
  1. Basic Logic 2.0 설계
  2. DB Connect GUI, INI File Create

* **2026-01-16 (GUI)**
  1. DVD 목록 검색기능 + 결제 버튼 추가 / `GUI_test1.py`
  2. 키보드 입력 최적화 / `GUI_test1.py`
  3. 결제기능 구현 + 연체료와 대여료를 합산하여 결제도 가능 / `GUI_test1.py`
  4. 전역변수로 필요 데이터 수거 기능 추가 / `GUI_test1.py`
  5. exe file 생성 `pyinstaller` 및 테스트 / `GUI_test1 - 1.exe`
  6. **성공**
  7. 구조 변경을 통한 동작 흐름 최적화 / `GUI_test2.py`
    <img width="707" height="437" alt="스크린샷 2026-01-20 170017" src="https://github.com/user-attachments/assets/c2ea61f9-b06a-44d9-9592-cf3a0bfa5a8e" />

* **2026-01-15 (GUI)**
  1. 로그인 화면 구현 및 DB 연결 / `GUI_test1.py`
  2. 고객검색 화면 구현 및 미반납 로그 출력 / `GUI_test1.py`
  3. exe file 생성 `pyinstaller` 및 테스트 / `GUI_test1.exe`
  4. `방화벽 포트 개방 5432` 
  5. `QUERY Tool` > `SHOW hba_file;` > `IPv4 local connections 모든 IP 접속 허용`
  6. **성공**
    <img width="271" height="141" alt="스크린샷 2026-01-20 165959" src="https://github.com/user-attachments/assets/2b732a9f-7eb9-4e53-b514-540f517ac469" />

* **2026-01-14 (CLI)**
  1. 미반납 이력이 존재하는 경우 미반납 이력과 연체 목록, 전체 연체료 출력 , 계산 > rental , film / `CLI_test1.py`
  2. 스파게티 코드의 모듈화 / `CLI_test2.py`
  3. 사용자 확인 구간에서 종료 커맨드 추가 / `CLI_test2.py`
  4. 장바구니 기능 추가 및 종료 시 장바구니 목록, 전체 대여료 출력 , 계산 / `CLI_test2.py`
  5. 데이터 오염 방지를 위해 DB 직접 저장 **Cancel**

* **2026-01-13 (CLI)**
  1. Basic Logic 1.0 설계
  2. 존재하는 사용자인지 아닌지를 확인하며 미반납 이력을 확인 > customer / `CLI_test1.py`
  3. 존재하는 영화 여부 확인 및 대여기간을 지정하여 대여기간에 따른 대여료 출력 > inventory , film / `CLI_test1.py`

</details>
