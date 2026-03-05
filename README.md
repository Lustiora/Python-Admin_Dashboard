# 📀 Sakila Store Management System

**Python Flet**과 **PostgreSQL**을 활용하여 구축한 **DVD 대여점 관리 시스템**(**Store Management System**)입니다.<br>
Sakila 샘플 데이터베이스를 기반으로 회원 관리, 재고 관리, 대여 및 반납 프로세스를 GUI로 구현중 입니다.

## 🛠 Tech Stack (Assets)

| Category          | Technology                              |
|:------------------|:----------------------------------------|
| **Language**      | Python 3.14                             |
| **GUI Framework** | Flet 0.28.3                             |
| **Database**      | PostgreSQL (Sakila Sample DB)           |
| **OS Support**    | Windows 11, Arch Linux (Cross-platform) |

---

## System Logic & Architecture (v2.1)

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
  
  * **Query:** `Customer ID (Barcode)` 또는 `Name` (First/Last) 복합 검색.
  * **Output:** 고객 기본 정보, 미반납 연체 상태(Normal/Overdue).
  * ~~**Flow:** 검색 결과 없음(Not Found) 시 **[신규 고객 등록]** 프로세스로 자동 전환.~~

* **B. Inventory Check (재고 확인)**
  
  * **Query:** `Inventory ID (Barcode)` 또는 `Title` 복합 검색.
  * **Output:**
    * **Film Data:** 영화 제목, 보유 상점, 최근 대여일자, 대여료 정보.
    * **Rental Status:** 현재 대여 중(`Checked Out`)인지 대여 가능(`In Stock`)인지 판별.
  * **Logic:** `rental` 테이블의 `return_date`가 `NULL`인 기록 존재 여부로 상태 판단.

* **C. Rental Search (대여 상태)**

  * **Output:**
    * **Total Rentals:** 대여중인 재고
    * **Overdue:** 연체중인 재고
    * **Due Today:** 금일 반납예정인 재고
    * **Rental Data:** Rental ID, Customer Name, Film Title, Rental Date, Due Date, Status, Action(?) 

---

## 📊 Business Logic (Rental & Return)

### 1. Transaction & Payment

* **1 Rental = 1 Payment**
  * **1:1 Mapping:** 하나의 대여(Rental)는 반드시 하나의 결제(Payment) 레코드와 매핑됩니다. 여러 DVD를 동시에 대여해도 내부적으로는 개별 트랜잭션으로 처리됩니다.
  * **Update Policy:** 연체료 발생 시 별도의 결제 레코드를 생성(`INSERT`)하지 않고, **기존 결제 레코드의 금액(`amount`)을 갱신(`UPDATE`)** 하여 최종 정산합니다.
  * **Pre-payment:** 기본 대여료는 대여 시점에 선불로 처리되며, 반납 시 추가 요금이 합산됩니다.

### 2. Overdue & Late Fee Policy

* **합리적인 연체료 상한선(Cap) 적용**
  * 연체료는 무한정 부과되지 않으며, 고객 이탈 방지를 위해 **DVD 교체 비용(Replacement Cost)** 을 초과할 수 없습니다.

| 구분            | 계산 로직                          | 비고                                 |
|---------------|--------------------------------|------------------------------------|
| **연체 기준**     | `(반납일 - 대여일) - 대여기간`           | 시간 단위 절사, **일(Day)** 단위 계산         |
| **연체 요율**     | **$1.00 / Day**                | 1일 연체 시 $1 추가                      |
| **상한선 (Cap)** | **MAX Fee ≤ Replacement Cost** | 연체료가 DVD 가격보다 비싸면 **DVD 가격까지만** 청구 |

**Formula:** `Final Fee = Base Rate + MIN( Overdue Days * $1.0, Replacement Cost )`

### 3. Status Definition

| Status       | Condition                                  | Description                |
|--------------|--------------------------------------------|----------------------------|
| **Rented**   | `return_date IS NULL`                      | 대여 중 (정상)                  |
| **Overdue**  | `return_date IS NULL` AND `Now > Due Date` | 연체 중 (반납 필요)               |
| **Returned** | `return_date IS NOT NULL`                  | 반납 완료 (정산 종료)              |
| **Lost**     | `Overdue > Threshold`                      | *분실 처리 (장기 연체 시 대체 비용 청구)* |

---

## 📅 Roadmap & Improvements

**Export Data:** 조회된 목록을 엑셀/CSV로 내보내기 기능.

**Console Log UI:** 시스템 동작 상태(Log) 출력 기능.

**Favorites:** 자주 사용하는 메뉴 타일을 빠르게 선택할 수 있는 기능.

---

## 📜 [Development Log (Workflow)](/WORKFLOW.md)

---

## 🗄️ Archived Specifications (Legacy)

<details>
<summary>📂 Basic Logic 2.0 (Detailed Spec)</summary>

### 1. Login Logic

1. **DB 연결정보를 확인**
   * 연결정보가 저장된 INI File 유무 확인
   * 화이트 리스트 확인: `postgresql.conf`, `pg_hba.conf`
   * **Process:**
     * 1-1. 해당 정보로 연결 시도
       * 일치: `DB Connect` 성공 → 2단계로 진입
       * 불일치: 에러 코드 출력 및 연결 정보 재입력 유도

2. **직원 ID를 확인 (Staff-Table)**
   * **Limit:** Login Count = 3
   * **Validation:** DB (Staff Table)의 `username`, `password`, `active=True` 확인
     * 일치: `DB Access` 성공
     * 불일치: Count 차감 및 재시도
       * Count 0 도달 시: _"Please Contact the Administrator"_ 출력 후 종료

### 2. Customer Check / Return / Rental / Calculation Logic

1. **회원 여부 확인 (Barcode) (Customer-Table)**
   * **1-1. 고객 ID 확인 (customer_id)**
     * 확인됨: `1 End`
     * 미확인: `1-2` 검색 화면으로 이동
     * 미회원: `1-3` 신규 등록
   * **1-2. 고객 정보 검색 화면**
     * Query: `first_name` or `last_name` or `email`
     * 결과 확인 시 `1-1`, 실패 시 `1-2` 유지
   * **1-3. 신규 고객 추가**
     * Auto-Increment ID 사용 (SERIAL/SEQUENCE)
     * 필수 정보: `store_id`, `first/last name`, `email`, `address_id` (Address 테이블 신규 생성 포함)

2. **재고 확인 (Barcode) (Inventory-Table)**
   * **2-1. 상품 Barcode 확인 (inventory_id)**
     * 확인됨: `2-2`
     * 미확인: `2-4` 검색 화면으로 이동
   * **2-2. 상품 상태 확인**
     * 대여중: Rental-Table에서 `return_date is null`인 기록 존재 → 반납 로직으로
     * 대여가능: `2-3` 정보 출력
   * **2-3. Film 정보 출력**
     * Film 테이블 Join (Category, Film_Category)
     * 출력: `title`, `rental_duration`, `rental_rate`, `rating`, `name`
   * **2-4. 재고 정보 검색 화면**
     * Query: `inventory_id` or `title (Fulltext)`
   * **2-5 ~ 2-7. 신규 재고/영화/배우 추가**
     * 기존 Film/Actor 존재 여부에 따라 분기 처리하여 신규 등록 수행.

3. **반납 (Rental-Table)**
   * **Process:**
     * `customer_id`와 `return_date is null` 조건으로 대여 기록 조회.
     * `(return_date - current_date)` 계산으로 연체 여부 판단.
   * **Calculation:**
     * 정상 반납: 추가 비용 없음.
     * 연체 시: `over_rate = (Delay Days) * (rental_rate / rental_duration) * 1.1`
     * 파손/분실 시: `+ replacement_cost`

4. **대여 (Rental-Table) & 결제**
   * **Rental Process:**
     * 고객(`1`)과 재고(`2`) 확인.
     * 장바구니(Rental_Cart) 담기 (최대 5개 제한).
     * 중복 대여 방지 ("이미 대여중인 DVD입니다" 출력).
   * **Payment & Transaction:**
     * `payment` 테이블: 전체 금액(Amount) 기록.
     * `rental` 테이블: 대여 기록 생성 (`return_date` = NULL).
     * **Rollback:** 과정 중 하나라도 실패 시 전체 취소.

</details>

<details>
<summary>📂 Basic Logic 1.0 (Deprecated)</summary>
    
1. Calculation Logic (Deprecated)
    > **연체료 및 대여료 산정 기준**
    >* **a. Rental Period (대여 기간):** `1 Day`, `3 Day`, `7 Day`
    >* **b. Rental Rate (대여료):** ~~Fixed: 1000, 2500, 5000~~
    >* **c. Overdue Base:** `Original Cost(C) * 1 Day`
    >* **d. Penalty Multiplier:** `1.1` (연체 시 1.1배 가산)
    
2. Workflow (Old)
   * **사용자 ID 확인:** 대여/연체 중인 DVD 존재 여부 확인.
   * **재고(Barcode) 확인:** 유효하지 않은 바코드일 경우 로그 기록 후 종료.
   * **대여/반납 화면 출력:**
      * **대여:** 대여 기간 선택 → 만료일 계산 → 대여 버튼 활성화.
      * **반납:** 연체 목록/기간 확인 → 연체료 계산 버튼 활성화.
   * **금액 표시 및 계산:** 대여료/연체료 합산 표시 및 결제.

3. Transition Note (Change Log)
   * **Sakila DB 재분석 결과:** 기존 예상보다 데이터 구조가 정교하여 새로운 로직(Logic 2.0)의 필요성 대두.
   * **주요 변경 사항:**
     * 관리자 확인 프로세스를 `Staff Table` 기반 로그인으로 대체.
     * `config.ini`를 통한 DB 연결 정보 관리 도입.
     * `Fulltext Search` 기능을 활용한 Title 검색창 추가.
     * GUI 프레임워크 변경: `Tkinter` → `Flet` (Cross-platform 지원).

</details>
