import tkinter # Python 기본 GUI Package
from tkinter import messagebox # 팝업창 GUI Package
######################################
# Login 모듈
count = 3
def user_login():
    global count
    login_id = user_id.get()
    login_pw = user_pw.get()
    print(f"ID : {login_id} | PW : {login_pw}")
    print("DB Connected ...")
    count = count - 1
    if login_id == "lus" or login_pw == "tiger": # 일치조건 > DB 연동 예정
        print("Login Successful")
        messagebox.showinfo("Login", "Login Successful")
        login.destroy() # Window (Login) 종료
    else:
        print("Login Failed")
        messagebox.showinfo("Login", f"Login Failed\nChance(3) : {count}")
    if count == 0:
        messagebox.showinfo("Login", "Please Contact the Administrator")
        print("Not Connected")
        login.destroy()
######################################
# Window 자동 중앙 정렬 모듈 (미정렬 시 좌측 상단)
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth() # 현재 모니터의 해상도(크기)를 가져옴
    screen_height = window.winfo_screenheight()
    x_pos = (screen_width // 2) - (width // 2) # 정중앙 좌표 계산 \ (//)는 정수 나누기
    y_pos = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}") # 위치 적용 (가로x세로+X좌표+Y좌표)
# 적용 > center_window([tkinter Window],[width],[height])
######################################
# 변수명 지정 없이 tkinter.Tk()로 작성하면 해당하는 속성이 포함된 창 3개가 출력
# tkinter.Tk().title("DVD")
# tkinter.Tk().geometry("500x500")
# tkinter.Tk().mainloop()
######################################
# tkinter Package 에서는 불가능한 방식 -> return self 없음 -> 한줄에 하나의 속성만 사용가능
# tkinter.Tk().title("PU").geometry("500x500").mainloop()
######################################
# Window (Login)
login = tkinter.Tk() # 표사되는 Window(tkinter.Tk())에 변수명을 지정하여 변수명을 기준으로 속성을 추가
login.title("Sakila Login")
center_window(login, 260, 100)
######################################
# Login 화면 구성 grid
# row=[행], column=[열]) > 0행 0열 = 좌측 상단 / 행과 열이 겹치는 경우 덮어씌워짐
# padx=[좌측우측여백], pady=[상단하단여백]
tkinter.Label(login, text="ID :").grid(row=0, column=0, padx=10, pady=5)
user_id = tkinter.Entry(login) # Entry -> 입력칸 | 입력된 값을 사용하기 위해 변수명 지정 필요
user_id.grid(row=0, column=1)
tkinter.Label(login, text="PASSWORD :").grid(row=1, column=0, padx=10, pady=5)
user_pw = tkinter.Entry(login, show="*")
user_pw.grid(row=1, column=1) # show="*" > 유출 방지 : 입력값 * 대체 출력
tkinter.Button(login, text="Login", command=user_login, width=20).grid(row=2, column=1, sticky="e", pady=5) # command=[클릭시 동작내용] | sticky="e" > 우측 정렬
######################################
login.mainloop() # root(Window)를 지속적으로 반복 실행 (종료방지)
######################################