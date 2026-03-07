import flet as ft


def main(page: ft.Page):
    page.title = "NavigationRail Test"

    # -------------------------------------------------------------------------
    # 1. [서브 메뉴 정의] 우측에 보여줄 '추가 선택지'들을 미리 만들어둡니다.
    # -------------------------------------------------------------------------
    def get_settings_view():
        # 서브 메뉴 클릭 시 실행될 함수
        def on_sub_click(e):
            page.snack_bar = ft.SnackBar(ft.Text(f"'{e.control.title.value}'를 선택했습니다."))
            page.snack_bar.open = True
            page.update()

        # 리스트 타일(메뉴 한 줄)들을 담은 컬럼 반환
        return ft.Column(
            controls=[
                ft.Text("환경 설정", size=30, weight="bold"),
                ft.Divider(),  # 구분선

                # [선택지 1]
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text("프로필 관리"),
                    subtitle=ft.Text("이름, 이메일 변경"),
                    on_click=on_sub_click
                ),
                # [선택지 2]
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.NOTIFICATIONS),
                    title=ft.Text("알림 설정"),
                    trailing=ft.Switch(value=True),  # 우측에 스위치 달기
                ),
                # [선택지 3]
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOCK),
                    title=ft.Text("보안 및 개인정보"),
                    on_click=on_sub_click
                ),
            ],
            spacing=10
        )

    # -------------------------------------------------------------------------
    # 2. [화면 영역 정의] (오른쪽 본문)
    # -------------------------------------------------------------------------
    content_area = ft.Container(
        # 초기값
        content=ft.Text("First Page Content", size=30),
        alignment=ft.alignment.center,  # 초기엔 가운데 정렬
        bgcolor=ft.Colors.AMBER_100,
        padding=20,  # 리스트가 벽에 붙지 않게 여백 추가
        expand=True
    )

    # -------------------------------------------------------------------------
    # 3. [로직 처리] 메뉴 클릭 핸들러
    # -------------------------------------------------------------------------
    def on_nav_change(e):
        index = e.control.selected_index
        print(f"Selected destination: {index}")

        # ★ 여기가 핵심입니다! ★
        # content_area.content에 무엇을 넣느냐에 따라 화면이 바뀝니다.

        if index == 0:
            # 0번: 그냥 텍스트 보여주기
            content_area.content = ft.Text("First Page Content", size=30)
            content_area.bgcolor = ft.Colors.AMBER_100
            content_area.alignment = ft.alignment.center  # 텍스트니까 가운데 정렬

        elif index == 1:
            # 1번: 다른 텍스트
            content_area.content = ft.Text("Second Page Content", size=30)
            content_area.bgcolor = ft.Colors.BLUE_100
            content_area.alignment = ft.alignment.center

        elif index == 2:
            # 2번(Settings): ★ 아까 만든 '메뉴 리스트(Column)'를 통째로 넣음 ★
            content_area.content = get_settings_view()
            content_area.bgcolor = ft.Colors.WHITE  # 배경을 흰색으로 깔끔하게
            content_area.alignment = ft.alignment.top_left  # 리스트는 위에서부터 나와야 하니까 정렬 변경

        content_area.update()

    # -------------------------------------------------------------------------
    # 4. [메뉴바 정의] NavigationRail
    # -------------------------------------------------------------------------
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,  # 메뉴 펼치기
        min_width=100,
        min_extended_width=200,
        leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE, label="First"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BOOKMARK_BORDER, selected_icon=ft.Icons.BOOKMARK, label="Second"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Settings"
            ),
        ],
        on_change=on_nav_change,
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )


ft.app(target=main)