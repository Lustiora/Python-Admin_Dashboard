import flet

def main(page: flet.Page):
    page.title = "Dialog Styles"
    page.window.width = 400
    page.window.height = 300

    # 1. [기본] Material 스타일 다이얼로그 설정
    def close_material(e):
        page.close(dlg_material)

    dlg_material = flet.AlertDialog(
        title=flet.Text("Basic Style"),
        content=flet.Text("This is the standard Material Design style."),
        actions=[
            flet.TextButton("OK", on_click=close_material),
            flet.TextButton("Cancel", on_click=close_material),
        ],
        actions_alignment=flet.MainAxisAlignment.END,
    )

    # 2. [아이폰] Cupertino 스타일 다이얼로그 설정
    def close_cupertino(e):
        page.close(dlg_cupertino)

    dlg_cupertino = flet.CupertinoAlertDialog(
        title=flet.Text("iOS Style"),
        content=flet.Text("This is the Cupertino style."),
        actions=[
            flet.CupertinoDialogAction("OK", is_destructive_action=True, on_click=close_cupertino),
            flet.CupertinoDialogAction("Cancel", on_click=close_cupertino),
        ],
    )

    # 화면에 버튼 2개 배치 (Row 사용)
    page.add(
        flet.Row(
            controls=[
                flet.ElevatedButton(
                    "Open Basic Dialog",
                    on_click=lambda e: page.open(dlg_material)
                ),
                flet.ElevatedButton(
                    "Open iOS Dialog",
                    on_click=lambda e: page.open(dlg_cupertino)
                ),
            ],
            alignment=flet.MainAxisAlignment.CENTER, # 버튼 중앙 정렬
        )
    )

flet.app(target=main)