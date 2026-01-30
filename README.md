# 📀 Sakila Store Management System

**Python Flet**과 **PostgreSQL**을 활용하여 구축한 **DVD 대여점 관리 시스템**(**Store Management System**)입니다.<br>
Sakila 샘플 데이터베이스를 기반으로 회원 관리, 재고 관리, 대여 및 반납 프로세스를 GUI로 구현했습니다.

## 🛠 Tech Stack (Assets)

| Category | Technology                              |
| :--- |:----------------------------------------|
| **Language** | Python 3.14                             |
| **GUI Framework** | Flet 0.28.3                             |
| **Database** | PostgreSQL (Sakila Sample DB)           |
| **OS Support** | Windows 11, Arch Linux (Cross-platform) |

---

## 🧠 System Logic & Architecture (v2.1)

### 1. System Startup & Authentication
시스템 시작 시 데이터베이스 연결 무결성을 점검하고 보안 로그인을 수행합니다.

* **Database Connection (Auto-Config):**
    * `config.ini` 파일 유무를 확인하여 저장된 정보로 자동 연결을 시도합니다.
    * **White List Check:** [PostgreSQL Server White List](https://github.com/Lustiora/Python-Sakila/wiki/PostgresSQL-Server-White-List) 설정을 준수합니다.
    * **Exception Handling:**
        * 자동 연결 실패 시 `Auto-Login Failed` 팝업 출력 후, 수동 입력 창(Setup Window)으로 전환됩니다.
* **Staff Login (Access Control):**
    * `staff` 테이블의 계정 정보(username, password)와 활성 상태(`active=True`)를 대조합니다.
    * **Security Lock:** 3회 로그인 실패 시 시스템이 잠기며 관리자 문의 메시지를 출력합니다.

### 2. Main Interface & Dashboard
사용자 편의성을 고려한 타일 메뉴와 실시간 상태 모니터링을 제공합니다.

* **Layout Structure:**
    * **Left Navigation:** 주요 모듈(검색, 등록, 관리)로의 빠른 접근.
    * **Tile Menu:** 직관적인 아이콘 형태의 메인 대시보드.
    * **Status Bar:** 하단에 DB 연결 상태(Connected/Disconnected)를 실시간으로 표시.

### 3. Search Modules (Core Features)
각 업무 목적에 최적화된 검색 로직을 수행합니다.

* **A. Customer Search (고객 관리)**
    * **Query:** `Customer ID` 또는 `Name` (First/Last) 복합 검색.
    * **Output:** 고객 기본 정보, 계정 활성 상태(Active/Inactive), 미반납 연체 이력 표시.
    * **Flow:** 검색 결과 없음(Not Found) 시 **[신규 고객 등록]** 프로세스로 자동 전환.

* **B. Inventory Check (재고 확인)**
    * **Query:** `Inventory ID` (Barcode) 스캔.
    * **Output:**
        * **Film Data:** 영화 제목, 등급, 대여료 정보.
        * **Rental Status:** 현재 대여 중(`Checked Out`)인지 대여 가능(`In Stock`)인지 판별.
    * **Logic:** `rental` 테이블의 `return_date`가 `NULL`인 기록 존재 여부로 상태 판단.

* **C. Film Search (영화 정보)**
    * **Query:** `Title` 기반 검색 (Full-text Search 지원).
    * **Output:** 영화 제목, 줄거리(Description), 출연 배우(Actor) 정보 매핑 출력.

---

## 📊 Business Logic (Rental & Return)

### Transaction Flow
* **Rental (대여):**
    * **Validation:** 고객의 연체 이력 유무 및 해당 재고의 `In Stock` 상태를 검증합니다.
    * **Cart System:** 장바구니 기능을 통해 복수의 미디어를 일괄 처리합니다.
* **Return (반납):**
    * **Overdue Check:** 반납 예정일(`Due Date`)과 현재 날짜를 비교하여 연체 여부를 판단합니다.
    * **Update:** `rental` 테이블의 `return_date`를 갱신하고, 연체료 발생 시 `payment` 테이블에 기록합니다.

---

## 🚀 Installation & Run (Hot Reload)

개발 환경에서의 실행 방법입니다. `db_connect` 모듈은 Hot Reload를 지원하지 않습니다.

**Environment:**
* Path: `~/Python-Sakila`
* Python Interpreter: `.venv/Scripts/python.exe`

**Run Command:**
```bash
# flet run -r [Target File]
flet run -r ./main_window.py
```

---

## 📅 Roadmap & Improvements

* [ ] **Export Data:** 조회된 목록을 엑셀/CSV로 내보내기 기능.
* [ ] **CRUD Integration:** 조회 목록에서 선택하여 즉시 수정/삭제 화면으로 연결.
* [ ] **Console Log UI:** 시스템 동작 상태(Log)를 출력하는 터미널 윈도우 추가.
* [ ] **Theme System:** 다크 모드/라이트 모드 테마 변경 기능.
* [ ] **Auto-Reconnect:** 서버 연결 끊김 시 백그라운드 재연결 시도 로직.

---

## 📜 Development Log (Workflow)

**Latest Update: 2026-01-30**

1. **Search Customer:** `Name` 검색 시 상세 상태(All Status) 출력으로 로직 고도화.
2. **Logic Update:** Basic Logic 2.1 사양서 현행화 작업 진행 중.

<details><summary>📂 Past Development Log (Click to Expand)</summary>
* **2026-01-29**
  1. Search Customer 모듈 분할 (ID, Name)
  2. 예외 처리 강화: `try-except` 구문 및 Error 구분 문구 추가
  3. Search Inventory 모듈 작성 (ID/Title 검색, 동일 Title 그룹화, 대여 상태 확인)
  4. Search Film 모듈 작성
  5. 전체 변수명 수정 및 통일

* **2026-01-28**
  1. Tile Menu 생성 (홈, 조회, 관리, 접속 상태)
  2. Main Home UI 작성
  3. System Dashboard 작성 (접속 정보 표시)
  4. Search Customer 로직 작성

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
  <p>
      <img width="707" height="437" alt="스크린샷 2026-01-20 170017" src="[https://github.com/user-attachments/assets/c2ea61f9-b06a-44d9-9592-cf3a0bfa5a8e](https://github.com/user-attachments/assets/c2ea61f9-b06a-44d9-9592-cf3a0bfa5a8e)" />
  </p>

* **2026-01-15 (GUI Prototype)**
  1. 로그인 화면 구현 및 DB 연결
  2. 고객 검색 화면 구현 및 미반납 로그 출력
  3. PyInstaller EXE 생성 및 테스트
  4. 방화벽 포트 개방 (5432) 및 PostgreSQL `pg_hba.conf` 설정 (IPv4 local connections 허용)
  <p>
      <img width="271" height="141" alt="스크린샷 2026-01-20 165959" src="[https://github.com/user-attachments/assets/2b732a9f-7eb9-4e53-b514-540f517ac469](https://github.com/user-attachments/assets/2b732a9f-7eb9-4e53-b514-540f517ac469)" />
  </p>

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

</details>

---

## 🗄️ Archived Specifications (Legacy)

과거 개발 단계에서 작성되었으나, **Logic 2.1** 도입으로 인해 현재는 폐기되거나 변경된 로직 사양서입니다. 개발 히스토리 보존을 위해 남겨둡니다.

<details>
<summary>📂 Basic Logic 2.0 (Detailed Spec)</summary>

### 1. Login Logic

1. [x] **DB 연결정보를 확인**
    - 연결정보가 저장된 INI File 유무 확인
    - 화이트 리스트 확인: `postgresql.conf`, `pg_hba.conf`
    - **Process:**
        - 1-1. 해당 정보로 연결 시도
            - 일치: `DB Connect` 성공 → 2단계로 진입
            - 불일치: 에러 코드 출력 및 연결 정보 재입력 유도

2. [x] **직원 ID를 확인 (Staff-Table)**
    - **Limit:** Login Count = 3
    - **Validation:** DB (Staff Table)의 `username`, `password`, `active=True` 확인
        - 일치: `DB Access` 성공
        - 불일치: Count 차감 및 재시도
            - Count 0 도달 시: _"Please Contact the Administrator"_ 출력 후 종료

### 2. Customer Check / Return / Rental / Calculation Logic

1. [ ] **회원 여부 확인 (Barcode) (Customer-Table)**
    - **1-1. 고객 ID 확인 (customer_id)**
        - 확인됨: `1 End`
        - 미확인: `1-2` 검색 화면으로 이동
        - 미회원: `1-3` 신규 등록
    - **1-2. 고객 정보 검색 화면**
        - Query: `first_name` or `last_name` or `email`
        - 결과 확인 시 `1-1`, 실패 시 `1-2` 유지
    - **1-3. 신규 고객 추가**
        - Auto-Increment ID 사용 (SERIAL/SEQUENCE)
        - 필수 정보: `store_id`, `first/last name`, `email`, `address_id` (Address 테이블 신규 생성 포함)

2. [ ] **재고 확인 (Barcode) (Inventory-Table)**
    - **2-1. 상품 Barcode 확인 (inventory_id)**
        - 확인됨: `2-2`
        - 미확인: `2-4` 검색 화면으로 이동
    - **2-2. 상품 상태 확인**
        - 대여중: Rental-Table에서 `return_date is null`인 기록 존재 → 반납 로직으로
        - 대여가능: `2-3` 정보 출력
    - **2-3. Film 정보 출력**
        - Film 테이블 Join (Category, Film_Category)
        - 출력: `title`, `rental_duration`, `rental_rate`, `rating`, `name`
    - **2-4. 재고 정보 검색 화면**
        - Query: `inventory_id` or `title (Fulltext)`
    - **2-5 ~ 2-7. 신규 재고/영화/배우 추가**
        - 기존 Film/Actor 존재 여부에 따라 분기 처리하여 신규 등록 수행.

3. [ ] **반납 (Rental-Table)**
    - **Process:**
        - `customer_id`와 `return_date is null` 조건으로 대여 기록 조회.
        - `(return_date - current_date)` 계산으로 연체 여부 판단.
    - **Calculation:**
        - 정상 반납: 추가 비용 없음.
        - 연체 시: `over_rate = (Delay Days) * (rental_rate / rental_duration) * 1.1`
        - 파손/분실 시: `+ replacement_cost`

4. [ ] **대여 (Rental-Table) & 결제**
    - **Rental Process:**
        - 고객(`1`)과 재고(`2`) 확인.
        - 장바구니(Rental_Cart) 담기 (최대 5개 제한).
        - 중복 대여 방지 ("이미 대여중인 DVD입니다" 출력).
    - **Payment & Transaction:**
        - `payment` 테이블: 전체 금액(Amount) 기록.
        - `rental` 테이블: 대여 기록 생성 (`return_date` = NULL).
        - **Rollback:** 과정 중 하나라도 실패 시 전체 취소.

</details>

<details>
<summary>📂 Basic Logic 1.0 (Deprecated)</summary>

### 1. Calculation Logic (Deprecated)
> 초기 기획 단계의 연체료 및 대여료 산정 기준 (현재 폐기됨)

* **a. Rental Period (대여 기간):** `1 Day`, `3 Day`, `7 Day`
* **b. Rental Rate (대여료):** ~~Fixed: 1000, 2500, 5000~~
* **c. Overdue Base:** `Original Cost(C) * 1 Day`
* **d. Penalty Multiplier:** `1.1` (연체 시 1.1배 가산)

### 2. Workflow (Old)
1.  **사용자 ID 확인:** 대여/연체 중인 DVD 존재 여부 확인.
2.  **재고(Barcode) 확인:** 유효하지 않은 바코드일 경우 로그 기록 후 종료.
3.  **대여/반납 화면 출력:**
    * **대여:** 대여 기간 선택 → 만료일 계산 → 대여 버튼 활성화.
    * **반납:** 연체 목록/기간 확인 → 연체료 계산 버튼 활성화.
4.  **금액 표시 및 계산:** 대여료/연체료 합산 표시 및 결제.

### 3. Transition Note (Change Log)
* **Sakila DB 재분석 결과:** 기존 예상보다 데이터 구조가 정교하여 새로운 로직(Logic 2.0)의 필요성 대두.
* **주요 변경 사항:**
    * 관리자 확인 프로세스를 `Staff Table` 기반 로그인으로 대체.
    * `config.ini`를 통한 DB 연결 정보 관리 도입.
    * `Fulltext Search` 기능을 활용한 Title 검색창 추가.
    * GUI 프레임워크 변경: `Tkinter` → `Flet` (Cross-platform 지원).
    * DB 날짜 데이터(`2006년`) 최신화를 위한 `Interval` 쿼리 로직 구상.

</details>