import flet


def main(page: flet.Page):
    # 1. 메뉴들이 자유롭게 떠다닐 '투명한 레이어 (Stack)'를 하나 만든다냥.
    menu_layer = flet.Stack(expand=True)

    # ---------------------------------------------------------
    # 🛠️ 집사가 구상한 "메뉴를 생성해서 리턴하는 함수" 다냥!
    # ---------------------------------------------------------
    def create_context_menu(x, y, customer_name):
        # 메뉴 항목을 클릭했을 때 메뉴를 닫는 내부 함수
        def close_menu(e):
            menu_layer.controls.clear()  # 레이어 비우기
            menu_layer.update()

        # 🚨 여기서 PopupMenuButton 대신, 직접 디자인한 Container를 리턴한다냥!
        return flet.PopupMenuButton(
            items=[
                flet.PopupMenuItem(content=flet.Text("Customer Name")),
                flet.PopupMenuItem(content=flet.Divider()),
                flet.PopupMenuItem("Rentals Data", on_click=close_menu),
                flet.PopupMenuItem("Payments Data", on_click=close_menu),
            ],
        )

    # ---------------------------------------------------------
    # 🖱️ 우클릭을 감지하는 이벤트 핸들러
    # ---------------------------------------------------------
    def on_right_click(e: flet.ControlEvent):
        # 1. 기존에 열려있는 메뉴가 있다면 싹 지운다냥.
        menu_layer.controls.clear()

        # 2. 🚨 집사의 함수를 호출해서 '메뉴 위젯'을 리턴 받는다냥!
        new_menu = create_context_menu(e.global_x, e.global_y, "John Doe")

        # 3. 리턴 받은 위젯을 메뉴 레이어에 올리고 화면 갱신!
        menu_layer.controls.append(new_menu)
        menu_layer.update()

    # (테스트용) 우클릭을 감지할 영수증 리스트 바탕화면
    background = flet.GestureDetector(
        content=flet.Container(bgcolor=flet.Colors.BLUE_GREY_50, expand=True,
                               content=flet.Text("아무데나 우클릭 해보라냥!", size=30)),
        on_secondary_tap_down=on_right_click  # 우클릭 감지!
    )

    # 🚨 가장 중요한 화면 구조! 바탕화면 위에 메뉴 레이어를 겹친다냥!
    page.add(
        flet.Stack([
            background,  # 1층: 영수증 목록
            menu_layer  # 2층: 메뉴가 나타났다 사라지는 투명 레이어
        ], expand=True)
    )


flet.app(target=main)