from screeninfo import get_monitors
def center_window(window, width, height, resizable=None, min_size=None):
    # 1. 창 정보 업데이트
    window.update_idletasks()

    target_monitor = None
    monitors = get_monitors()

    # 2. '주 모니터(Primary)'를 찾아서 고정 타겟으로 설정
    for m in monitors:
        if m.is_primary:
            target_monitor = m
            break

    # 만약 주 모니터 감지에 실패했다면(Linux 드라이버 특성 등), 무조건 첫 번째 모니터 사용
    if target_monitor is None and len(monitors) > 0:
        target_monitor = monitors[0]

    # 3. 좌표 계산 (선택된 모니터의 중앙)
    if target_monitor:
        x_pos = target_monitor.x + (target_monitor.width // 2) - (width // 2)
        y_pos = target_monitor.y + (target_monitor.height // 2) - (height // 2)
    else:
        # 정말 만약에 모니터 정보를 아예 못 가져왔을 경우 (안전장치)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_pos = (screen_width // 2) - (width // 2)
        y_pos = (screen_height // 2) - (height // 2)

    # 4. 적용
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    # 옵션 설정 (기존과 동일)
    if resizable is not None:
        if isinstance(resizable, bool):
            window.resizable(resizable, resizable)
        else:
            window.resizable(resizable[0], resizable[1])

    if min_size is not None:
        window.minsize(min_size[0], min_size[1])

def center_window_delayed(window, width, height):
    # 기존 center_window 로직 실행 (screeninfo 사용하는 버전)
    center_window(window, width, height, resizable=None)

    # 위치를 잡은 뒤에 창을 보여줌 (deiconify)
    window.deiconify()

def set_focus_force(main, entry):  # 포커스 강제 조정
    main.lift()  # 창을 화면 맨 앞으로
    main.attributes('-topmost', True)  # 잠시동안 창을 최상위로 고정
    main.attributes('-topmost', False)  # 고정 해제 (안 그러면 다른 창이 안 덮임)
    entry.focus_force()  # [entry]입력창 강제 포커스

# from Window import set_focus_force
# login.after(200, set_focus_force, login, user_id) # set_focus_force(login, user_id)

# ---------------------------------------------------------
# Sub Frame
# ---------------------------------------------------------
def start_move(event, window):
    # event.x_root는 모니터 전체 기준 마우스 위치입니다. (절대 좌표)
    # 윈도우의 현재 위치와 마우스 위치의 차이(Offset)를 저장합니다.
    window.start_x = event.x_root - window.winfo_x()
    window.start_y = event.y_root - window.winfo_y()

    window.lift() # 선택시 상단 출력

def on_drag(event, window): # 마우스가 움직인 절대 좌표에서, 아까 저장한 차이만큼 뺍니다.
    x = event.x_root - window.start_x
    y = event.y_root - window.start_y

    # --- 가두리(Clamping) 로직 ---
    parent = window.master
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height() - 30 # Status Bar Height 30
    window_w = window.winfo_width()
    window_h = window.winfo_height()

    if x < 0: x = 0
    if y < 0: y = 0
    if x + window_w > parent_w: x = parent_w - window_w
    if y + window_h > parent_h: y = parent_h - window_h

    window.place(x=x, y=y)


# -- Color Palette --
class Corporate_Blue:
    # Corporate Blue
    primary = "#243b55"  # 타이틀 바 (어두운 네이비)
    title_text = "#ffffff"  # 타이틀 텍스트 (흰색)
    point = "#141e30"  # 강조
    action = "#00b4db"  # 버튼/검색
    alert = "#ff6b6b"  # 경고/닫기
    background = "#f8f9fa"  # 배경색 (밝은 회색)
    success = "#27ae60"  # 성공 메시지
    text = "#2c3e50"  # 일반 글자색 (어두운 회색)
    status_bar = "#dfe6e9"
    status_text = "#2d3436"

class Dark_Pro:
    # Theme: Dark Pro (VS Code Style)
    primary = "#1e1e1e"  # 아주 어두운 회색
    title_text = "#ffffff"  # 타이틀 텍스트 (흰색)
    point = "#252526"  # 서브 배경
    action = "#007acc"  # 선명한 파랑
    alert = "#f44336"  # 밝은 빨강
    background = "#2d2d2d"  # 짙은 회색
    success = "#4ec9b0"  # 민트색
    text = "#d4d4d4"  # 일반 글자색 (밝은 회색)
    status_bar = "#333333"
    status_text = "#cccccc"

class Warm_Latte:
    # Theme: Warm Latte
    primary = "#6d4c41"  # 커피 브라운
    title_text = "#fff3e0"  # 타이틀 텍스트 (크림색 - 부드러운 느낌)
    point = "#5d4037"  # 진한 브라운
    action = "#d84315"  # 번트 오렌지
    alert = "#c62828"  # 진한 빨강
    background = "#efebe9"  # 연한 베이지
    success = "#2e7d32"  # 숲 녹색
    text = "#3e2723"  # 일반 글자색 (진한 고동색)
    status_bar = "#d7ccc8"
    status_text = "#4e342e"

class Forest_Calm:
    # Theme: Forest Calm
    primary = "#2e7d32"  # 포레스트 그린
    title_text = "#ffffff"  # 타이틀 텍스트 (흰색)
    point = "#1b5e20"  # 짙은 녹색
    action = "#00897b"  # 틸(Teal) 색상
    alert = "#e53935"  # 붉은색
    background = "#f1f8e9"  # 아주 연한 연두색
    success = "#43a047"  # 밝은 녹색
    text = "#1c2331"  # 일반 글자색 (진한 남색)
    status_bar = "#c8e6c9"
    status_text = "#1b5e20"

class Modern_Mono:
    # Theme: Modern Mono
    primary = "#263238"  # 블루 그레이
    title_text = "#ffffff"  # 타이틀 텍스트 (흰색)
    point = "#37474f"  # 옅은 블루 그레이
    action = "#6200ea"  # 강렬한 보라색
    alert = "#d50000"  # 선명한 빨강
    background = "#eceff1"  # 밝은 회색
    success = "#00c853"  # 비비드 그린
    text = "#212121"  # 일반 글자색 (검정)
    status_bar = "#cfd8dc"
    status_text = "#37474f"
    
Colors = Forest_Calm