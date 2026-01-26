import tkinter as tk


# =============================================================================
# [공용] 드래그 & 이동 함수 (모든 서브 윈도우가 이 함수를 씁니다)
# =============================================================================
def start_move(event, window):
    # 1. 클릭하는 순간 맨 앞으로 가져오기 (Lift)
    window.lift()

    # 2. 절대 좌표(모니터 기준)를 사용하여 오차 계산
    # (위젯 내부 좌표인 event.x 대신 event.x_root를 써야 Label을 잡아도 튀지 않습니다)
    window.start_x = event.x_root - window.winfo_x()
    window.start_y = event.y_root - window.winfo_y()


def on_drag(event, window):
    # 1. 이동할 위치 계산 (현재 마우스 절대 좌표 - 오차)
    x = event.x_root - window.start_x
    y = event.y_root - window.start_y

    # 2. 가두리(Clamping) 로직: 부모 창 밖으로 못 나가게 막음
    parent = window.master
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()
    window_w = window.winfo_width()
    window_h = window.winfo_height()

    if x < 0: x = 0
    if y < 0: y = 0
    if x + window_w > parent_w: x = parent_w - window_w
    if y + window_h > parent_h: y = parent_h - window_h

    # 3. 위치 적용
    window.place(x=x, y=y)


# =============================================================================
# [예시] 고객 조회 창 함수 (기능 적용 완료)
# =============================================================================
# 전역 변수 (중복 실행 방지용)
current_search_customer = None


def close_customer_frame(event=None):
    global current_search_customer
    if current_search_customer:
        current_search_customer.destroy()
    current_search_customer = None


def search_customer_frame(root):  # root나 main을 인자로 받거나 전역변수 사용
    global current_search_customer

    # 1. 중복 방지 (이미 있으면 맨 앞으로)
    if current_search_customer is not None:
        current_search_customer.lift()
        return

    # 2. 프레임 생성
    # -------------------------------------------------------------------------
    current_search_customer = tk.Frame(root, width=300, height=200, bg="white", relief="raised", bd=3)
    current_search_customer.place(x=50, y=50)
    # -------------------------------------------------------------------------

    # 3. 타이틀 바 (손잡이)
    title_bar = tk.Frame(current_search_customer, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")

    # 타이틀 글자
    title_label = tk.Label(title_bar, text="고객 조회", bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
    title_label.pack(side="left", padx=5)

    # 닫기 버튼
    close_btn = tk.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4, cursor="hand2")
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_customer_frame)

    # 4. 내용물 (Body)
    content_frame = tk.Frame(current_search_customer, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # 위젯 배치
    tk.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tk.Entry(content_frame).pack(pady=5)
    tk.Button(content_frame, text="검색").pack(pady=5)

    # =========================================================================
    # 5. 이벤트 바인딩 (여기가 핵심!)
    # =========================================================================

    # (A) 타이틀바 & 라벨 -> [드래그 이동] + [Lift]
    # lambda를 써서 'current_search_customer' 창 객체를 함수에 넘겨줍니다.
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_customer))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_customer))

    title_label.bind("<Button-1>", lambda e: start_move(e, current_search_customer))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_customer))

    # (B) 내용물(Body) -> [Lift]만 적용 (드래그 X)
    content_frame.bind("<Button-1>", lambda e: current_search_customer.lift())

    # (C) 내용물 안의 모든 자식 위젯들(버튼, 엔트리 등) -> [Lift]만 적용
    # 이 루프가 있어야 버튼이나 빈칸을 눌러도 창이 앞으로 튀어나옵니다.
    for child in content_frame.winfo_children():
        child.bind("<Button-1>", lambda e: current_search_customer.lift(), add="+")