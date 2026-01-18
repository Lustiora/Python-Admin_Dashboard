# Python-Sakila-Manager
> Sakila DB > Read POS (Point of Sales) Simulator

## Future Improvements

* Sakila DB를 재확인한 결과 상상이상으로 많은 데이터가 정리되어있음을 확인하여 **새로운 Logic의 필요성을 확인**
  * 현재
    * 관리자확인 > 고객확인 > 대여이력확인 > 재고확인 > 결제
    * 대여 가능 기간, 그에 따른 대여 비용은 사전에 정의되어있음
    *  관리자확인을 대신하는 Staff Table
  * 이후
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

## Basic Logic

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

## Workflow

* **2026-01-16 (GUI)**
  1. DVD 목록 검색기능 + 결제 버튼 추가 / `GUI_test1.py`
  2. 키보드 입력 최적화 / `GUI_test1.py`
  3. 결제기능 구현 + 연체료와 대여료를 합산하여 결제도 가능 / `GUI_test1.py`
  4. 전역변수로 필요 데이터 수거 기능 추가 / `GUI_test1.py`
  5. exe file 생성 `pyinstaller` 및 테스트 / `GUI_test1 - 1.exe`
  6. **성공**
  7. 구조 변경을 통한 동작 흐름 최적화 / `GUI_test2.py`

<details>
<summary>Old Workflow</summary>

* **2026-01-15 (GUI)**
  1. 로그인 화면 구현 및 DB 연결 / `GUI_test1.py`
  2. 고객검색 화면 구현 및 미반납 로그 출력 / `GUI_test1.py`
  3. exe file 생성 `pyinstaller` 및 테스트 / `GUI_test1.exe`
  4. `방화벽 포트 개방 5432` 
  5. `QUERY Tool` > `SHOW hba_file;` > `IPv4 local connections 모든 IP 접속 허용`
  6. **성공**

* **2026-01-14 (CLI)**
  1. 미반납 이력이 존재하는 경우 미반납 이력과 연체 목록, 전체 연체료 출력 , 계산 > rental , film / `CLI_test1.py`
  2. 스파게티 코드의 모듈화 / `CLI_test2.py`
  3. 사용자 확인 구간에서 종료 커맨드 추가 / `CLI_test2.py`
  4. 장바구니 기능 추가 및 종료 시 장바구니 목록, 전체 대여료 출력 , 계산 / `CLI_test2.py`
  5. 데이터 오염 방지를 위해 DB 직접 저장 **Cancel**

* **2026-01-13 (CLI)**
  1. 존재하는 사용자인지 아닌지를 확인하며 미반납 이력을 확인 > customer / `CLI_test1.py`
  2. 존재하는 영화 여부 확인 및 대여기간을 지정하여 대여기간에 따른 대여료 출력 > inventory , film / `CLI_test1.py`

</details>
