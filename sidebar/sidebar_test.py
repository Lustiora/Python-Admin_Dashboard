import flet as ft


def main(page: ft.Page):
    page.title = "NavigationRail Test"

    # 1. [오른쪽 화면] 내용이 바뀔 공간 (Container)
    # 처음에는 0번 인덱스(First)에 해당하는 내용을 보여줍니다.
    content_area = ft.Container(
        content=ft.Text("First Page Content", size=30),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.AMBER_100,  # 구분을 위해 배경색 지정
        expand=True  # 남은 공간을 꽉 채움
    )

    # 2. [이벤트 핸들러] 메뉴 변경 시 실행될 함수
    def on_nav_change(e):
        index = e.control.selected_index
        print(f"Selected destination: {index}")  # 터미널 로그 출력

        # 인덱스에 따라 오른쪽 화면 내용 변경
        if index == 0:
            content_area.content.value = "First Page Content"
            content_area.bgcolor = ft.Colors.AMBER_100
        elif index == 1:
            content_area.content.value = "Second Page Content"
            content_area.bgcolor = ft.Colors.BLUE_100
        elif index == 2:
            content_area.content.value = "Settings Page Content"
            content_area.bgcolor = ft.Colors.GREEN_100

        content_area.update()  # 화면 갱신

    # 3. [왼쪽 메뉴] NavigationRail 구성
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        # leading: 상단에 고정된 버튼 (보통 추가/작성 버튼으로 씀)
        leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE_BORDER,
                selected_icon=ft.Icons.FAVORITE,
                label="First",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
        ],
        on_change=on_nav_change,  # 함수 연결
    )

    # 4. [레이아웃 조립] Row( [메뉴] | 구분선 | [내용] )
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content_area,  # 여기가 내용이 바뀌는 부분
            ],
            expand=True,  # Row 자체가 화면을 꽉 채우도록 설정
        )
    )


ft.app(target=main)