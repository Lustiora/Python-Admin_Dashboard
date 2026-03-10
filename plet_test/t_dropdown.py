import flet as ft
import time


def main(page: ft.Page):
    # 🚨 [중요] Ref를 사용하면 "진짜 화면에 있는 놈"의 멱살을 잡을 수 있다냥!
    dd1_ref = ft.Ref[ft.Dropdown]()
    dd2_ref = ft.Ref[ft.Dropdown]()

    def on_change_dd1(e):
        print(f"1번 변경됨! 현재 2번 값: {dd2_ref.current.value}")

        # 1. 값을 완전히 비운다냥
        # dd2_ref.current.value = None

        # 2. 🚨 [필살기] Key를 바꿔서 Flet이 "어? 이거 새 드롭다운이네?" 하고
        # 이전 기억(잔상)을 싹 지우게 만든다냥!
        dd2_ref.current.key = str(time.time())

        # 3. 1번 선택에 따라 2번 옵션도 갈아끼워준다냥
        if dd1_ref.current.value == "A":
            dd2_ref.current.options = [ft.dropdown.Option("A-1"), ft.dropdown.Option("A-2")]
        else:
            dd2_ref.current.options = [ft.dropdown.Option("B-1"), ft.dropdown.Option("B-2")]

        # 4. 페이지 전체를 새로고침한다냥
        page.update()
        print("2번 초기화 완료냥! 🐾")

    # UI 구성
    page.add(
        ft.Text("드롭다운 완전 초기화 테스트 (Ref 방식)", size=20, weight="bold"),

        ft.Dropdown(
            ref=dd1_ref,  # 참조 연결
            label="1번 메뉴 (여기 선택하면 2번 리셋)",
            options=[ft.dropdown.Option("A"), ft.dropdown.Option("B")],
            on_change=on_change_dd1,
            width=300,
        ),

        ft.Dropdown(
            ref=dd2_ref,  # 참조 연결
            label="2번 메뉴",
            hint_text="1번을 먼저 골라라냥",
            options=[],
            width=300,
        )
    )


ft.app(target=main)