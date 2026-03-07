import flet as ft


def main(page: ft.Page):
    page.title = "Custom Sidebar with Index"
    page.bgcolor = ft.Colors.BLUE_GREY_50

    # 1. [오른쪽 화면] 내용이 바뀔 공간 (변수명: basic_content)
    # 내부에 Text가 있어야 .content.value나 .color를 바꿀 수 있습니다.
    basic_content = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.PURPLE,  # 초기값 (index 0 기준)
        content=ft.Text("메뉴", size=50, weight="bold", color=ft.Colors.ON_SURFACE)
    )

    # 2. [로직] 인덱스에 따라 화면 바꾸기
    # e: 이벤트 객체 (클릭 정보), index: 우리가 직접 넘겨줄 번호
    def on_nav_change(index):
        print(f"선택된 인덱스: {index}")  # 디버깅용

        if index == 0:
            basic_content.content.value = "메뉴"
            basic_content.content.color = ft.Colors.ON_SURFACE
            basic_content.bgcolor = ft.Colors.PURPLE
        elif index == 1:
            basic_content.content.value = "조회"
            basic_content.content.color = ft.Colors.ON_SURFACE
            basic_content.bgcolor = ft.Colors.BLUE
        elif index == 2:
            basic_content.content.value = "변경"
            basic_content.content.color = ft.Colors.ON_SURFACE
            basic_content.bgcolor = ft.Colors.BROWN_500
        elif index == 3:
            basic_content.content.value = "삭제"
            basic_content.content.color = ft.Colors.ON_SURFACE
            basic_content.bgcolor = ft.Colors.YELLOW_200
        elif index == 4:
            basic_content.content.value = "추가"
            basic_content.content.color = ft.Colors.ON_SURFACE
            basic_content.bgcolor = ft.Colors.LIGHT_BLUE_100
        elif index == 5:
            basic_content.content.value = "통계"
            basic_content.content.color = ft.Colors.ON_SURFACE
            basic_content.bgcolor = ft.Colors.DEEP_ORANGE_200
        elif index == 6:
            basic_content.content.value = "관리"
            basic_content.content.color = ft.Colors.ON_SURFACE
            basic_content.bgcolor = ft.Colors.CYAN_400

        basic_content.update()

    # 3. [왼쪽 사이드바] 버튼마다 번호표 붙이기 (lambda 사용)
    sidebar = ft.Container(
        width=250,
        bgcolor=ft.Colors.WHITE,
        padding=10,
        content=ft.Column(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DASHBOARD),
                    title=ft.Text("메뉴 (0)"),
                    # [핵심] lambda e: on_nav_change(0) -> 0번을 들고 함수로 가라!
                    on_click=lambda e: on_nav_change(0)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SEARCH),
                    title=ft.Text("조회 (1)"),
                    on_click=lambda e: on_nav_change(1)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CHANGE_CIRCLE),
                    title=ft.Text("변경 (2)"),
                    on_click=lambda e: on_nav_change(2)
                ),

                # 아코디언 메뉴 예시
                ft.ExpansionTile(
                    leading=ft.Icon(ft.Icons.FOLDER),
                    title=ft.Text("더보기"),
                    controls=[
                        ft.ListTile(
                            title=ft.Text("삭제 (3)"),
                            content_padding=ft.padding.only(left=40),
                            on_click=lambda e: on_nav_change(3)
                        ),
                        ft.ListTile(
                            title=ft.Text("추가 (4)"),
                            content_padding=ft.padding.only(left=40),
                            on_click=lambda e: on_nav_change(4)
                        ),
                    ]
                ),

                ft.Divider(),

                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PIE_CHART),
                    title=ft.Text("통계 (5)"),
                    on_click=lambda e: on_nav_change(5)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SETTINGS),
                    title=ft.Text("관리 (6)"),
                    on_click=lambda e: on_nav_change(6)
                ),
            ]
        )
    )

    page.add(
        ft.Row(
            [sidebar, ft.VerticalDivider(width=1), basic_content],
            expand=True
        )
    )


ft.app(target=main)