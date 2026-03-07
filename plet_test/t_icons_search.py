import flet as ft


def main(page: ft.Page):
    page.title = "Icon Variant Finder"
    page.window.width = 600
    page.window.height = 500

    # 1. 모든 아이콘 이름 로딩
    all_icons = [icon for icon in dir(ft.Icons) if icon.isupper()]

    # 2. 결과 보여줄 리스트뷰
    result_view = ft.ListView(expand=True, spacing=10, padding=20)

    # 3. 검색 로직 (핵심)
    def find_variants(e):
        search_term = txt_search.value.upper().strip()
        if not search_term: return

        result_view.controls.clear()

        # 검색어가 포함된 모든 아이콘을 찾음
        found_icons = [icon for icon in all_icons if search_term in icon]

        # 보기 좋게 정렬 (짧은 이름 순서대로)
        found_icons.sort(key=len)

        if not found_icons:
            result_view.controls.append(ft.Text("결과가 없습니다."))
        else:
            # 아이콘들을 하나씩 리스트에 추가
            for icon_name in found_icons:
                result_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=getattr(ft.Icons, icon_name), size=40),
                            ft.Column([
                                ft.Text(icon_name, weight="bold"),
                                ft.Text("클릭해서 복사", size=10, color="grey")
                            ])
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.BLUE_GREY_50,
                        border_radius=10,
                        on_click=lambda e, name=icon_name: copy_code(name)
                    )
                )
        result_view.update()

    # 4. 복사 기능
    def copy_code(name):
        code = f"ft.Icons.{name}"
        page.set_clipboard(code)
        page.snack_bar = ft.SnackBar(ft.Text(f"복사됨: {code}"))
        page.snack_bar.open = True
        page.update()

    # 5. UI 구성
    txt_search = ft.TextField(
        label="아이콘 핵심 키워드 (예: HEART, STAR, BOOKMARK)",
        on_submit=find_variants,
        autofocus=True
    )

    btn_search = ft.IconButton(icon=ft.Icons.SEARCH, on_click=find_variants)

    page.add(ft.Container(height=0),
        ft.Row([txt_search, btn_search]),
        ft.Divider(),
        result_view
    )


ft.app(target=main)