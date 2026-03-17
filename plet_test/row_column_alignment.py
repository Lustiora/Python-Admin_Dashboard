import flet as ft


def main(page: ft.Page):
    page.title = "용용씨의 정렬(Alignment) 테스트"
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30

    # 테스트용 박스 찍어내는 함수 (보기 편하게 색과 크기를 지정)
    def box(text, color, width=60, height=60):
        return ft.Container(
            content=ft.Text(text, color=ft.Colors.WHITE, weight="bold", size=20),
            bgcolor=color, width=width, height=height,
            alignment=ft.alignment.center, border_radius=8
        )

    # ==========================================
    # 1. Row (가로 배치) 테스트 영역
    # ==========================================
    row_test = ft.Container(
        bgcolor=ft.Colors.BLUE_50,
        height=150,  # 세로 공간을 넉넉히 줌 (세로 정렬 확인용)
        border=ft.border.all(2, ft.Colors.BLUE_200),
        content=ft.Row(
            # 🚨 가로(메인 축) 정렬: 박스들 사이의 간격을 동일하게 띄움
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,

            # 🚨 세로(교차 축) 정렬: 박스들을 상단(START)에 착! 붙임
            vertical_alignment=ft.CrossAxisAlignment.START,

            controls=[
                box("1", ft.Colors.BLUE_400, height=60),
                box("2", ft.Colors.BLUE_600, height=100),  # 얘만 키가 큼!
                box("3", ft.Colors.BLUE_800, height=60),
            ]
        )
    )

    # ==========================================
    # 2. Column (세로 배치) 테스트 영역
    # ==========================================
    col_test = ft.Container(
        bgcolor=ft.Colors.RED_50,
        width=300,  # 가로 공간을 넉넉히 줌 (가로 정렬 확인용)
        height=300,
        border=ft.border.all(2, ft.Colors.RED_200),
        content=ft.Column(
            # 🚨 세로(메인 축) 정렬: 박스들을 위아래 양끝과 가운데로 쫙 찢어놓음
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            # 🚨 가로(교차 축) 정렬: 박스들을 가운데(CENTER)로 모음
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[
                box("A", ft.Colors.RED_400, width=60),
                box("B", ft.Colors.RED_600, width=150),  # 얘만 뚱뚱함!
                box("C", ft.Colors.RED_800, width=60),
            ]
        )
    )

    # 화면에 추가
    page.add(
        ft.Text("🟦 1. Row (가로 배치) 규칙", size=20, weight="bold"),
        ft.Text("- 가로정렬(진행): MainAxis / 세로정렬(교차): CrossAxis"),
        row_test,

        ft.Divider(height=40),

        ft.Text("🟥 2. Column (세로 배치) 규칙", size=20, weight="bold"),
        ft.Text("- 세로정렬(진행): MainAxis / 가로정렬(교차): CrossAxis"),
        col_test,
    )


if __name__ == "__main__":
    ft.app(target=main)