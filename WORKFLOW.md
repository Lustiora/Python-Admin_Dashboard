## [README](/README.md)

* **2026-02-20**
  1. 함수형 프로그래밍에서 객체지향 프로그래밍 전환 (Def >> Class)
     * src\db_connect.py >> class_src\db_connect.py **완료**

* **2026-02-19**
  1. menu search rental 페이징 버튼 추가
  2. page 선택 영역 드래그 기능 추가
  3. flet 0.28.3 라이브러리 위젯 List 추출 및 Docs 제작

* **2026-02-13**
  1. Database Update (Actor, Category, ... Table)
     * **Film Table**:
       * Column special_features Delete → 미사용
       * Column fulltext Not Update → Update, Insert: **Auto Update**
     * **Actor Table**:
       * TMDB Movie Credits Crawling
     * **Category Table**:
       * TMDB Movie Genres Crawling
       * film_actor, film_category Table Connect
  2. Database Update에 따른 View Query Update 진행중

* **2026-02-12**
  1. search rental menu filter 추가 실패
     * Dropdown menu 를 사용하여 연동 시 Container Button과의 충돌 발생 (e.control.valve)
  2. Database Update (Film Table)
     * TMDB API Crawling. Film Table Column 최대한도로 강화
      ```bash
      title = 'Greenland 2: Migration'
      , description = 'Having found the safety of the ...'
      , release_year = '2026'
      , language_id = '1'
      , rental_duration = '7'
      , rental_rate = '0.99'
      , length = '98'
      , replacement_cost = '21.99'
      , rating = 'PG-13'
      , last_update = '2026-02-12'
      , special_features = '{}'::_text
      , fulltext = $$Adventure Thriller Science Fiction $$
      , poster_path = '/z2tqCJLsw6uEJ8nJV8BsQXGa3dr.jpg'
      ```
  3. menu search rental query 수정
    * Customer Name Search → 'Returned' 항목 누락

* **2026-02-11**
  1. test Hot Reload Fix
     * 윈도우 지연 실행 문제 해결
  2. search view table or query clean
     * view table : not_return_customer , rental_data
     * query : menu search rental (7)
  3. Database Update (Film Table)
     * TMDB API 추출 Update (Title, Description, Release_year, Last_update)
     * **+ Poster_path (Poster Image Link)**

* **2026-02-10**

  1. View Table rental_full_status 보완
     * 고객 가입 매장과 이용 매장이 동일하지 않을 수 있음을 확인하여 컬럼 추가
     * item_store_id, customer_store_id
     * 총결제액을 p.amount 컬럼값을 사용하는게 아닌 연체료를 연체일수에 맞춰 계산하여 기본 대여료에 추가하는 방식으로 수정 
  2. return_payment_query create
     * 연체 중인지 아닌지 상태를 파악하여 반납과 동시에 결제

* **2026-02-09**

  1. **Database Server** Synology Docker Connect
  2. Logic Test View Table rental_full_status Create 
     * customer_id, payment_id, rental_id, base_rental_rate, rental_date, 
     * payment_date, return_date, rental_limit_days, **days_rented**, **days_overdue**, 
     * **est_late_fee**, overdue_paid_date, total_amount, store_id
     * [**`Custom Sakila Database`**](https://github.com/Lustiora/Convert_Sakila)
  3. 기존 Query 재설계 필요성 확인 
     * 대여중 (55:54), 연체중(16:15), 금일 반납예정(3:4)

* **2026-02-06**

  1. **Search Rental:** Query Case문 오류 수정
  2. **Search Rental:** `Search Rental error : ListView Control must be added to the page first` Fix
     * rental_search_total_query Module 초기 실행 시 발생하는 Error `if rental_data.page:`를 추가하여 초기 Update 방지
  3. **Search Rental:** Font Color 중복 사용 부분 Class Add
  4. **Search Rental:** View Table: now() → CURRENT_DATE , return_due_today_query 수정 `due_day::date = today`
  5. **Search Payment:** Query 설계 중
  6. **Search Payment:** 화면 구성 중
  7. Test Main Window: 실행 속도 Fix

* **2026-02-05**

  1. Test Main Window: Conn Connect
  2. **Search Rental:** Query 설계 완료
  3. **Search Rental:** 화면 구성 완료 (Basic: Total Rentals View)
  4. **Search Rental:** Filter Button Delete

* **2026-02-04**

  1. **Search Rental:** 대여상태 조회 화면 설계 중
  2. `test_main_window.py`, `test_nav_tile.py` Update
  3. **Search Rental:** 구성 모듈 분리
  4. Hot Reload.bat / .sh Create

* **2026-02-03**

  1. Datatable → Row,Column,Expand 방식으로 전환 (flet 0.28.3 : page.on_resize 명령어 부재)
  2. Popup Autofocus 추가
  3. **Search Customer:** 검색 화면 재설계 (ID or Name (First or Last Name))
  4. **Search Inventory:** View Table 재생성 및 쿼리 재설정 / 재설계 (ID or Film Title)
  5. search query 분리
  6. input event 이후 포커스 연결 : input_inventory.focus()
  7. Search Modules (Core Features), C. Rental Search 추가 (Film Search 제거)

* **2026-02-02**

  1. Customer ID Query Update 및 IF문으로 출력물에 따른 색상 변동 기능 추가

* **2026-01-31**

  1. query_current_status module query 단축 및 스토어 정보를 연결하여 해당 점포에만 존재하는 재고를 출력
  2. Improved variable and function names
   
     <details><summary>Improvement History</summary>
   
     | Old                            | New                          | 비고 (역할)                        |
     | ------------------------------ | ---------------------------- | ------------------------------ |
     | **`menu.py`**                  | --                           | --                             |
     | `c_home`                       | **`view_home`**              | 메인 홈 화면 반환                     |
     | `c_status`                     | **`view_system_dashboard`**  | 시스템 상태 대시보드 반환                 |
     | `c_statistic`                  | **`view_analytics`**         | 통계/분석 화면 반환                    |
     | `c_manager`                    | **`view_admin_manager`**     | 관리자 설정 화면 반환                   |
     | **`menu_search.py`**           | --                           | --                             |
     | `search_customer`              | **`view_search_customer`**   | 고객 조회 전체 화면 구성                 |
     | `search_inventory`             | **`view_search_inventory`**  | 재고 조회 전체 화면 구성                 |
     | `search_film`                  | **`view_search_film`**       | 영화 조회 전체 화면 구성                 |
     | **`menu_search_inventory.py`** | --                           | --                             |
     | `search_inventory_data`        | **`build_inventory_ui`**     | UI 컴포넌트 생성 및 반환                |
     | `stock_id_module`              | **`query_basic_info`**       | DB: 기본 정보 조회 로직                |
     | `stock_rental_module`          | **`query_rental_history`**   | DB: 대여 이력 조회 로직                |
     | `stock_title_module`           | **`query_current_status`**   | DB: 현재 상태(대여중/반납) 조회           |
     | `iv_bu`                        | **`on_click_search`**        | 이벤트: 검색 버튼 클릭 핸들러              |
     | `inventory_id`                 | **`input_inventory_id`**     | UI: 재고 ID 입력창 (TextField)      |
     | `search`                       | **`btn_search`**             | UI: 검색 버튼 (Button)             |
     | `stock_id_data`                | **`table_basic_info`**       | UI: 기본 정보 표 (DataTable)        |
     | `stock_id`                     | **`ui_basic_info`**          | UI: 기본 정보 컨테이너 (Container/Row) |
     | `stock_rental_data`            | **`table_rental_history`**   | UI: 대여 이력 표 (DataTable)        |
     | `stock_rental`                 | **`ui_rental_history`**      | UI: 대여 이력 컨테이너                 |
     | `stock_title_data`             | **`table_current_status`**   | UI: 현재 상태 표 (DataTable)        |
     | `stock_title`                  | **`ui_current_status`**      | UI: 현재 상태 컨테이너                 |
     | **`menu_search_film.py`**      | --                           | --                             |
     | `search_film_title`            | **`build_film_ui`**          | UI 컴포넌트 생성 및 반환                |
     | `sfq_title`                    | **`handle_search`**          | 이벤트: 검색 로직 핸들러                 |
     | `film_title_text`              | **`input_film_title`**       | UI: 영화 제목 입력창                  |
     | `film_title_data`              | **`table_film_list`**        | UI: 영화 목록 표                    |
     | `film_title`                   | **`ui_film_list`**           | UI: 영화 목록 컨테이너                 |
     | **`menu_search_customer.py`**  | --                           | --                             |
     | `search_customer_id`           | **`build_customer_id_ui`**   | ID 검색 UI 생성                    |
     | `customer_id_module`           | **`query_customer_by_id`**   | DB: ID로 고객 조회                  |
     | `search_customer_name`         | **`build_customer_name_ui`** | 이름 검색 UI 생성                    |
     | `customer_name_module`         | **`query_customer_by_name`** | DB: 이름으로 고객 조회                 |
     | **`menu_add.py`**              |                              |                                |
     | `add_customer`                 | **`view_add_customer`**      | 신규 등록 화면 반환                    |
     | `add_inventory`                | **`view_add_inventory`**     | (이하 동일 규칙 적용)                  |
     | `add_film`                     | **`view_add_film`**          |                                |
     | **`menu_edit.py`**             | --                           | --                             |
     | `edit_customer`                | **`view_edit_customer`**     | 정보 수정 화면 반환                    |
     | `edit_inventory`               | **`view_edit_inventory`**    |                                |
     | **`menu_delete.py`**           | --                           | --                             |
     | `delete_customer`              | **`view_delete_customer`**   | 정보 삭제 화면 반환                    |
     | `delete_inventory`             | **`view_delete_inventory`**  |                                |
   
     </details>

* **2026-01-30**

  1. **Search Customer:** `Name` 검색 시 상세 상태(All Status) 출력으로 로직 고도화.
  2. **Logic Update:** Basic Logic 2.1 사양서 현행화 작업.

* **2026-01-29**

  1. **Search Customer:** 모듈 분할 (ID, Name)
  2. 예외 처리 강화: `try-except` 구문 및 Error 구분 문구 추가
  3. **Search Inventory:** 모듈 작성 (ID/Title 검색, 동일 Title 그룹화, 대여 상태 확인)
  4. **Search Film:** 모듈 작성
  5. 전체 변수명 수정 및 통일

* **2026-01-28**

  1. Tile Menu 생성 (홈, 조회, 관리, 접속 상태)
  2. Main Home UI 작성
  3. **System Dashboard:** 작성 (접속 정보 표시)
  4. **Search Customer:** 로직 작성

* **2026-01-27**

  1. DB Connect ~ Main Window 연결 프로세스 최적화
  2. DB Monitor와 Main Window 연결
  3. Windows OS Resize Error 해결을 위해 `page.window.max_` 속성 제거
  4. Auto Login 시작 시 `Connecting to Database` 텍스트 출력 추가
  5. UX 개선: `db_connect`, `staff_login` 입력창 `autofocus=True` 적용
  6. Status Bar 연동 상태 색상 강조 (Visual Indicator)
  7. Status Bar 전체 구조 생성 완료
  8. Linux 호환성: `time.sleep(0.1)` Loading Time Force 추가 (옵션 적용 전 시작 방지)
  9. Auto Login 모듈 실행 시 최소 1초 대기 옵션 추가
  10. Linux 종료 이벤트 루프 방지: `page.window.prevent_close = False` 옵션 추가

* **2026-01-26**

  1. **Framework Migration:** CustomTkinter → **Flet (0.28.3)** (Web/App 호환성 및 GUI 이슈 해결)
  2. DB Connect > Main Window 연결 성공
  3. Linux Flet 호환성 옵션 추가 (Window Size 강제 설정)
     ```bash
     page.window.min_width = page.window.width
     page.window.min_height = page.window.height
     page.window.max_width = page.window.min_width
     page.window.max_height = page.window.min_height
     ```
  4. Exit Popup 추가 (`page.window.prevent_close = True` 이벤트 처리)
    * Linux: `e.page.window.destroy()`

* **2026-01-23**

  1. Menubar Module 분리 (Sub Frame: search, change, delete, add)
  2. Window Module (`start_move`, `on_drag`) 로직 이전
  3. Menubar Status_Frame에 로그인 직원 정보 표시 (staff_login > main_window)
  4. 테마 적용을 위한 Theme 클래스 생성
  5. GUI 라이브러리 변경 (Tkinter > CustomTkinter)

* **2026-01-22**

  1. Status Bar 구현 (DB 접속 상태 5초 주기 체크)
  2. Linux 호환 설정: DB Disconnect 시 Restart 로직 디버깅
  3. PyInstaller 패키지 컴파일 테스트
        ```bash
        pyinstaller -F -w -n Sakila_Basic_Logic_2_3 db_connect.py
        # Linux 실행 성공 / Windows 별도 패키지 컴파일 필요 (Cross-Compile 미지원)
        ```
  4. OS별 재시작(Restart) 로직 분기 처리 및 디버깅
  5. `config.ini` 파일 유무에 따른 접속 로직 변경 (파일 존재 시 즉시 접속 시도)
  6. Windows EXE Compile Restart Error 디버깅 (파일 자체 재실행 방식으로 전환)
     * *원인: Windows EXE 실행 시 임시 폴더 생성 방식과 재시작 로직 간의 경로 충돌*
  7. Windows Sandbox Test 완료 (**Clear**)

* **2026-01-21**

  1. Main Window Menubar 생성
  2. Sub Window Frame 구현 진행
  3. Status Bar 구현 진행 (DB 접속 체크)
  4. DB Connect 5s Test 및 Disconnect Link Logic 추가
  5. Linux/Windows 경로 호환성 설정 추가
        ```bash
        import sys
        if sys.platform == "win32": appdata = os.getenv("APPDATA")
        else: appdata = os.path.expanduser("~/.config")
        ```
  6. Window Array Middle 정렬 디버깅

* **2026-01-20**

  1. DB Connect 디버깅
  2. DB Connect GUI > Staff Login GUI 연결
  3. Main Window 생성

* **2026-01-19**

  1. **Basic Logic 2.0 설계**
  2. DB Connect GUI 및 INI File 생성 로직 구현

* **2026-01-16 (GUI Prototype)**

  1. DVD 목록 검색 기능 및 결제 버튼 추가
  2. 키보드 입력 최적화
  3. 결제 기능 구현 (연체료 + 대여료 합산 결제)
  4. 전역 변수 데이터 수거 기능 추가
  5. PyInstaller EXE 생성 및 테스트 (**성공**)
  6. 구조 변경을 통한 동작 흐름 최적화 (`GUI_test2.py`)

* **2026-01-15 (GUI Prototype)**

  1. 로그인 화면 구현 및 DB 연결
  2. 고객 검색 화면 구현 및 미반납 로그 출력
  3. PyInstaller EXE 생성 및 테스트
  4. 방화벽 포트 개방 (5432) 및 PostgreSQL `pg_hba.conf` 설정 (IPv4 local connections 허용)

* **2026-01-14 (CLI Prototype)**

  1. 미반납 이력, 연체 목록, 연체료 출력 및 계산 로직 구현 (`rental`, `film`)
  2. 코드 모듈화 진행 (스파게티 코드 개선)
  3. 사용자 확인 구간 종료 커맨드 추가
  4. 장바구니 기능 추가 (종료 시 목록 및 대여료 계산)
  5. 데이터 오염 방지를 위해 DB 직접 저장 방식 취소

  * **2026-01-13 (CLI Prototype)**

  1. **Basic Logic 1.0 설계**
  2. 사용자 확인 및 미반납 이력 조회 (`customer`)
  3. 영화 존재 여부 및 대여 기간에 따른 대여료 출력 (`inventory`, `film`)