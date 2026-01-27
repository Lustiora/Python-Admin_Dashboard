import flet as ft


def main(page: ft.Page):
    # 1. 메뉴바의 너비 모드 변경 함수
    def toggle_rail(e):
        # extended(글자보임) <-> compact(아이콘만) 토글
        rail.extended = not rail.extended
        rail.update()  # 변경사항 적용

    # 2. 사이드바 정의
    rail = ft.NavigationRail(
        extended=True,  # 처음엔 글자까지 다 보이게 시작
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.WIFI, label="Connect"),
            ft.NavigationRailDestination(icon=ft.Icons.TABLE_CHART, label="View"),
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Settings"),
        ],
        # [핵심] 메뉴 맨 위에 '토글 버튼' 추가
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=toggle_rail,
            tooltip="메뉴 접기/펼치기"
        ),
    )

    page.add(
        ft.Row(
            [rail, ft.VerticalDivider(width=1), ft.Text("본문 내용")],
            expand=True
        )
    )


ft.app(target=main)