def center_window(window, width, height, resizable = None, min_size = None): # Window 자동 중앙 정렬 모듈 (미정렬 시 좌측 상단) (tkinter)
    screen_width = window.winfo_screenwidth() # 현재 모니터의 해상도(크기)를 가져옴
    screen_height = window.winfo_screenheight()
    x_pos = (screen_width // 2) - (width // 2) # 정중앙 좌표 계산 \ (//)는 정수 나누기
    y_pos = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}") # 위치 적용 (가로x세로+X좌표+Y좌표)
    if resizable is not None:
        if isinstance(resizable, bool): # 입력값이 True/False 하나라면 가로/세로 똑같이 적용
            window.resizable(resizable, resizable)
        else: # 입력값이 (True, False) 처럼 튜플/리스트라면 각각 적용
            window.resizable(resizable[0], resizable[1])
    if min_size is not None: # 최소 해상도 지정 (더 이상 작아지지 않음)
        # min_size=(너비, 높이) 튜플 형태로 입력받음
        window.minsize(min_size[0], min_size[1])
# 적용 > center_window([tkinter Window],[width],[height],[resizable = True, False],[min_size = 가로,세로])

def set_focus_force(main, entry):  # 포커스 강제 조정
    main.lift()  # 창을 화면 맨 앞으로
    main.attributes('-topmost', True)  # 잠시동안 창을 최상위로 고정
    main.attributes('-topmost', False)  # 고정 해제 (안 그러면 다른 창이 안 덮임)
    entry.focus_force()  # [entry]입력창 강제 포커스

# from Window import set_focus_force
# login.after(200, set_focus_force, login, user_id) # set_focus_force(login, user_id)