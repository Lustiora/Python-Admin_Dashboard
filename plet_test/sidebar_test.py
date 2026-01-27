import flet as ft


def main(page: ft.Page):
    page.title = "Nested Sidebar Example"
    page.bgcolor = ft.Colors.BLUE_GREY_50  # 전체 배경색

    # 1. [오른쪽 화면] 내용이 표시될 공간
    content_area = ft.Container(
        expand=True,
        bgcolor=ft.Colors.WHITE,
        padding=20,
        alignment=ft.alignment.center,
        content=ft.Text("메뉴를 선택해주세요", size=20)
    )

    # 2. [로직] 메뉴 클릭 시 실행될 함수
    def on_menu_click(e):
        # 클릭한 버튼의 텍스트를 가져와서 화면에 표시
        menu_name = e.control.title.value
        content_area.content = ft.Text(f"'{menu_name}' 화면입니다.", size=30, weight="bold")
        content_area.update()

    # 3. [왼쪽 사이드바] 커스텀 메뉴 구성
    sidebar = ft.Container(
        width=250,  # 사이드바 너비
        bgcolor=ft.Colors.WHITE,
        padding=10,
        content=ft.Column(
            controls=[
                # (1) 프로필 영역 (사진처럼)
                ft.ListTile(
                    leading=ft.CircleAvatar(
                        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"),
                    title=ft.Text("Andrew Smith", weight="bold"),
                    subtitle=ft.Text("Product Manager"),
                ),
                ft.Divider(),

                # (2) 일반 메뉴 (Dashboard)
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DASHBOARD_OUTLINED),
                    title=ft.Text("Dashboard"),
                    on_click=on_menu_click,
                    selected=True,  # 처음 선택된 느낌
                ),

                # (3) ★ 핵심기능: 확장 가능한 메뉴 (Audience) ★
                ft.ExpansionTile(
                    leading=ft.Icon(ft.Icons.PEOPLE_OUTLINE),
                    title=ft.Text("Audience"),
                    controls=[
                        # 하위 메뉴들 (들여쓰기 줘서 안쪽인거 티내기)
                        ft.ListTile(
                            title=ft.Text("Overview", size=14),
                            content_padding=ft.padding.only(left=50),  # 들여쓰기
                            on_click=on_menu_click,
                            height=40,  # 하위 메뉴는 조금 얇게
                        ),
                        ft.ListTile(
                            title=ft.Text("Demographics", size=14),
                            content_padding=ft.padding.only(left=50),
                            on_click=on_menu_click,
                            height=40,
                        ),
                    ]
                ),

                # (4) ★ 핵심기능: 사진 속 Income 메뉴 ★
                ft.ExpansionTile(
                    leading=ft.Icon(ft.Icons.BAR_CHART),
                    title=ft.Text("Income"),
                    # 처음부터 펼쳐져 있게 하려면 아래 주석 해제
                    # initially_expanded=True,
                    controls=[
                        ft.ListTile(
                            title=ft.Text("Earnings", size=14),
                            content_padding=ft.padding.only(left=50),
                            on_click=on_menu_click,
                            height=40,
                        ),
                        ft.ListTile(
                            title=ft.Text("Refunds", size=14),
                            content_padding=ft.padding.only(left=50),
                            on_click=on_menu_click,
                            height=40,
                        ),
                        ft.ListTile(
                            title=ft.Text("Declines", size=14),
                            content_padding=ft.padding.only(left=50),
                            on_click=on_menu_click,
                            height=40,
                        ),
                        ft.ListTile(
                            title=ft.Text("Payouts", size=14),
                            content_padding=ft.padding.only(left=50),
                            on_click=on_menu_click,
                            height=40,
                        ),
                    ]
                ),

                # (5) 하단 Settings 영역
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SETTINGS_OUTLINED),
                    title=ft.Text("Settings"),
                    on_click=on_menu_click,
                ),
            ],
            scroll=ft.ScrollMode.AUTO  # 메뉴가 길어지면 스크롤 가능하게
        )
    )

    # 4. [레이아웃] 사이드바 | 구분선 | 내용
    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )


ft.app(target=main)