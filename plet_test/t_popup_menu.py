import flet as ft


def main(page: ft.Page):
    page.title = "팝업 메뉴 예제"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 1. 메뉴를 눌렀을 때 실행될 함수
    def handle_menu_click(e):
        # e.control.text: 눌린 메뉴의 이름("수정", "삭제" 등)을 가져옴
        print(f"선택한 메뉴: {e.control.text}")

        page.snack_bar = ft.SnackBar(ft.Text(f"'{e.control.text}'를 클릭했습니다!"))
        page.snack_bar.open = True
        page.update()

    # 2. 팝업 메뉴 버튼 만들기
    menu_btn = ft.PopupMenuButton(
        icon=ft.Icons.MORE_VERT,  # 점 3개 아이콘 (가장 많이 씀)
        tooltip="더보기 메뉴",
        items=[
            # 메뉴 항목 1: 아이콘 + 텍스트
            ft.PopupMenuItem(
                text="수정하기",
                icon=ft.Icons.EDIT,
                on_click=handle_menu_click
            ),
            # 메뉴 항목 2: 위험한 작업 (삭제)
            ft.PopupMenuItem(
                text="삭제하기",
                icon=ft.Icons.DELETE_OUTLINE,
                on_click=handle_menu_click
            ),
            # [구분선] 그냥 빈 PopupMenuItem()을 넣으면 선이 생깁니다.
            ft.PopupMenuItem(),

            # 메뉴 항목 3: 체크박스 스타일 (checked=True 하면 체크됨)
            ft.PopupMenuItem(
                text="고급 설정",
                icon=ft.Icons.SETTINGS,
                on_click=handle_menu_click
            ),
        ]
    )

    page.add(
        ft.Text("아이콘을 눌러보세요 👇"),
        menu_btn
    )


ft.app(target=main)