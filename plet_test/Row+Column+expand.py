import flet as ft
from window import Ratios

# DataTable 대체 -> Row + Column + expand

def main(page: ft.Page):
    page.title = "Auto-Resize Table Test (No Events)"
    page.padding = 20

    # 1. 컬럼 비율 설정 (합계: 1+1+2+3+3+2+1 = 13등분)
    # 이 숫자만 바꾸면 컬럼 너비 비율이 변합니다.

    # 2. 헤더 만들기 (고정된 회색 바)
    header_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Store", weight="bold", expand=Ratios.store, text_align="center"),
                ft.Text("ID", weight="bold", expand=Ratios.id, text_align="center"),
                ft.Text("Name", weight="bold", expand=Ratios.name, text_align="center"),
                ft.Text("Email", weight="bold", expand=Ratios.email, text_align="center"),
                ft.Text("Address", weight="bold", expand=Ratios.address, text_align="center"),
                ft.Text("Date", weight="bold", expand=Ratios.create_date, text_align="center"),
                ft.Text("Status", weight="bold", expand=Ratios.status, text_align="center"),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10  # 컬럼 사이 간격
        ),
        bgcolor=ft.Colors.GREY_300,
        padding=10,
        border_radius=5,
    )

    # 3. 데이터 리스트 (스크롤 가능한 영역)
    # 가짜 데이터 20개 생성
    data_controls = []
    for i in range(20):
        # 홀수/짝수 행 배경색 다르게 (가독성)
        bg_color = ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100

        row = ft.Container(
            content=ft.Row(
                controls=[
                    # expand=... 설정을 헤더와 똑같이 맞춥니다.
                    ft.Text(f"ST-{i % 2 + 1}", expand=Ratios.store, text_align="center"),
                    ft.Text(f"{1000 + i}", expand=Ratios.id, text_align="center"),
                    ft.Text(f"User Name {i}", expand=Ratios.name, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(f"user{i}@example.com", expand=Ratios.email, no_wrap=True,
                            overflow=ft.TextOverflow.ELLIPSIS),
                    # 아주 긴 주소 테스트
                    ft.Text(f"South Korea Seoul Gangnam-gu Teheran-ro 123, Building No.{i} (Very Long Address Test)",
                            expand=Ratios.address, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text("2023-10-25", expand=Ratios.create_date, text_align="center"),

                    # 상태값에 따른 색상/뱃지 처리
                    ft.Container(
                        content=ft.Text("Active" if i % 3 != 0 else "Overdue",
                                        color=ft.Colors.WHITE, size=12, weight="bold"),
                        bgcolor=ft.Colors.GREEN if i % 3 != 0 else ft.Colors.RED,
                        padding=5, border_radius=5, alignment=ft.alignment.center,
                        expand=Ratios.status
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            ),
            bgcolor=bg_color,
            padding=10,
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_200))
        )
        data_controls.append(row)

    # 데이터를 담을 스크롤 뷰
    data_list_view = ft.ListView(
        controls=data_controls,
        expand=True,  # 화면의 남은 높이를 다 씁니다.
        spacing=0
    )

    # 4. 화면 추가 (Header + List)
    # Column 자체도 expand=True가 되어야 꽉 찹니다.
    layout = ft.Column(
        controls=[
            ft.Text("Resize Window Test (Flex Layout)", size=20, weight="bold"),
            header_row,  # 고정 헤더
            data_list_view  # 남은 공간 다 차지하는 리스트
        ],
        expand=True  # 전체 레이아웃 확장
    )

    page.add(layout)


ft.app(target=main)