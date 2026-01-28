import flet as ft
import datetime


def main(page: ft.Page):
    page.title = "Sakila Query Tool"
    page.padding = 20

    # ---------------------------------------------------------
    # 1. [로그 창] (DBeaver의 Execution Log 역할)
    # ---------------------------------------------------------
    log_list = ft.ListView(
        expand=True,
        spacing=2,
        padding=10,
        auto_scroll=True,  # ★ 핵심: 새 로그가 오면 자동으로 스크롤 내림
    )

    # 로그 출력용 컨테이너 (까만 터미널 느낌)
    log_container = ft.Container(
        content=log_list,
        bgcolor=ft.Colors.BLACK,  # 터미널 배경색
        border_radius=5,
        padding=5,
        expand=True,
    )

    # 로그 추가 함수
    def add_log(message, msg_type="info"):
        now = datetime.datetime.now().strftime("%H:%M:%S")

        # 타입별 색상 지정
        if msg_type == "error":
            color = ft.Colors.RED_ACCENT
            prefix = "[ERROR]"
        elif msg_type == "success":
            color = ft.Colors.GREEN_ACCENT
            prefix = "[OK]"
        else:
            color = ft.Colors.WHITE
            prefix = "[INFO]"

        # 로그 한 줄 추가 (Consolas 폰트 추천)
        log_list.controls.append(
            ft.Text(f"{now} {prefix} - {message}", color=color, font_family="Consolas", size=14, selectable=True)
        )
        log_list.update()

    # ---------------------------------------------------------
    # 2. [결과 그리드 창] (DBeaver의 Result Grid 역할)
    # ---------------------------------------------------------
    result_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("First Name")),
            ft.DataColumn(ft.Text("Last Name")),
            ft.DataColumn(ft.Text("Email"), numeric=False),
        ],
        rows=[],
        border=ft.border.all(1, "grey"),
        vertical_lines=ft.border.all(1, "grey"),
        horizontal_lines=ft.border.all(1, "grey"),
        heading_row_color=ft.Colors.BLUE_GREY_100,
    )

    # 데이터 테이블은 가로/세로 스크롤이 필요하므로 Row/Column + scroll 조합
    result_container = ft.Column(
        controls=[ft.Row([result_table], scroll=ft.ScrollMode.ALWAYS)],  # 가로 스크롤
        scroll=ft.ScrollMode.AUTO,  # 세로 스크롤
        expand=True
    )

    # ---------------------------------------------------------
    # 3. [탭 구성] 결과 탭 / 로그 탭
    # ---------------------------------------------------------
    output_tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Result Grid",
                icon=ft.Icons.TABLE_CHART,
                content=result_container,  # 여기에 테이블 넣기
            ),
            ft.Tab(
                text="Execution Log",
                icon=ft.Icons.TERMINAL,
                content=log_container,  # 여기에 로그창 넣기
            ),
        ],
        expand=True,
    )

    # ---------------------------------------------------------
    # 4. 테스트 동작 (버튼 클릭 시)
    # ---------------------------------------------------------
    def run_query(e):
        # 1. 로그 탭으로 강제 이동 (선택 사항)
        # output_tabs.selected_index = 1
        # output_tabs.update()

        # 2. 로그 출력
        add_log("Fetching data from database...", "info")

        try:
            # 3. 데이터 추가 (가짜 데이터)
            import random
            row_id = len(result_table.rows) + 1
            result_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(row_id))),
                    ft.DataCell(ft.Text(f"User{row_id}")),
                    ft.DataCell(ft.Text("Doe")),
                    ft.DataCell(ft.Text(f"user{row_id}@sakila.com")),
                ])
            )
            result_table.update()

            # 성공 로그
            add_log(f"Query executed successfully. 1 row fetched.", "success")
        except Exception as ex:
            add_log(f"Query failed: {str(ex)}", "error")

    # ---------------------------------------------------------
    # 5. 화면 배치
    # ---------------------------------------------------------
    page.add(
        ft.Row([
            ft.ElevatedButton("Run Query (Test)", icon=ft.Icons.PLAY_ARROW, on_click=run_query),
            ft.ElevatedButton("Clear Logs", icon=ft.Icons.CLEAR_ALL,
                              on_click=lambda e: (log_list.controls.clear(), log_list.update()))
        ]),
        ft.Divider(),
        # 화면의 남은 공간을 탭이 다 차지하도록
        ft.Container(content=output_tabs, expand=True)
    )


ft.app(target=main)