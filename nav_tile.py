import flet

def nav(page: flet.Page):
    basic_content = flet.Container(
        content=flet.Text("Welcome Sakila"),
        alignment=flet.alignment.center,
        expand=True,
        border_radius=5
    )
    def close_pop_open(e):
        page.open(main_quit)
    def close_pop(e):
        page.close(main_quit)  # 팝업창 종료 명령어
    def close_main(e):
        page.window.close()
        page.window.destroy()
    main_quit = flet.AlertDialog(
        title=flet.Text("Quit"),
        content=flet.Text("Exit?"),
        actions=[flet.TextButton("OK", on_click=close_main),
                 flet.TextButton("Cancel", on_click=close_pop)
                 ], actions_alignment=flet.MainAxisAlignment.END)
    def on_nav_change(index):
        if index == 0:
            basic_content.content.value = "상태"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.PURPLE
        elif index == 1.1:
            basic_content.content.value = "1.1 고객"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BLUE
        elif index == 1.2:
            basic_content.content.value = "1.2 재고"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BROWN_500
        elif index == 1.3:
            basic_content.content.value = "1.3 영화"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.YELLOW_200
        elif index == 1.4:
            basic_content.content.value = "1.4 대여"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.LIGHT_BLUE_100
        elif index == 1.5:
            basic_content.content.value = "1.5 결제"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.DEEP_ORANGE_200
        elif index == 2.1:
            basic_content.content.value = "2.1 고객"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BLUE
        elif index == 2.2:
            basic_content.content.value = "2.2 재고"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BROWN_500
        elif index == 2.3:
            basic_content.content.value = "2.3 영화"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.YELLOW_200
        elif index == 2.4:
            basic_content.content.value = "2.4 대여"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.LIGHT_BLUE_100
        elif index == 2.5:
            basic_content.content.value = "2.5 결제"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.DEEP_ORANGE_200
        elif index == 3.1:
            basic_content.content.value = "3.1 고객"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BLUE
        elif index == 3.2:
            basic_content.content.value = "3.2 재고"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BROWN_500
        elif index == 3.3:
            basic_content.content.value = "3.3 영화"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.YELLOW_200
        elif index == 3.4:
            basic_content.content.value = "3.4 대여"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.LIGHT_BLUE_100
        elif index == 3.5:
            basic_content.content.value = "3.5 결제"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.DEEP_ORANGE_200
        elif index == 4.1:
            basic_content.content.value = "4.1 고객"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BLUE
        elif index == 4.2:
            basic_content.content.value = "4.2 재고"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BROWN_500
        elif index == 4.3:
            basic_content.content.value = "4.3 영화"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.YELLOW_200
        elif index == 4.4:
            basic_content.content.value = "4.4 배우"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.LIGHT_BLUE_100
        elif index == 4.5:
            basic_content.content.value = "4.5 장르"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.DEEP_ORANGE_200
        elif index == 5:
            basic_content.content.value = "통계"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BLUE
        elif index == 6:
            basic_content.content.value = "관리"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BROWN_500

        basic_content.update()
    tile_column = flet.Column(
        controls=[
            flet.ListTile(
                leading=flet.Icon(flet.Icons.MENU_ROUNDED),
                title=flet.Text("Status"),
                on_click=lambda e: on_nav_change(0)
            ),flet.Divider(
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.SCREEN_SEARCH_DESKTOP_ROUNDED),
                title=flet.Text("Search"),
                bgcolor=flet.Colors.BLUE_GREY_200,
                controls=[
                    flet.ListTile(
                        title=flet.Text("Customer"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.1)
                    ),flet.ListTile(
                        title=flet.Text("Inventory"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.2)
                    ),flet.ListTile(
                        title=flet.Text("Film"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.3)
                    ),flet.ListTile(
                        title=flet.Text("Rental"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.4)
                    ),flet.ListTile(
                        title=flet.Text("Payment"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(1.5)
                    ),
                ]
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.CHANGE_CIRCLE),
                title=flet.Text("Change"),
                bgcolor=flet.Colors.BLUE_GREY_200,
                controls=[
                    flet.ListTile(
                        title=flet.Text("Customer"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.1)
                    ),flet.ListTile(
                        title=flet.Text("Inventory"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.2)
                    ),flet.ListTile(
                        title=flet.Text("Film"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.3)
                    ),flet.ListTile(
                        title=flet.Text("Rental"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.4)
                    ),flet.ListTile(
                        title=flet.Text("Payment"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(2.5)
                    ),
                ]
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.DELETE),
                title=flet.Text("Delete"),
                bgcolor=flet.Colors.BLUE_GREY_200,
                controls=[
                    flet.ListTile(
                        title=flet.Text("Customer"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.1)
                    ),flet.ListTile(
                        title=flet.Text("Inventory"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.2)
                    ),flet.ListTile(
                        title=flet.Text("Film"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.3)
                    ),flet.ListTile(
                        title=flet.Text("Rental"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.4)
                    ),flet.ListTile(
                        title=flet.Text("Payment"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(3.5)
                    ),
                ]
            ),flet.ExpansionTile(
                leading=flet.Icon(flet.Icons.ADD_BOX),
                title=flet.Text("Add"),
                bgcolor=flet.Colors.BLUE_GREY_200,
                controls=[
                    flet.ListTile(
                        title=flet.Text("Customer"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.1)
                    ),flet.ListTile(
                        title=flet.Text("Inventory"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.2)
                    ),flet.ListTile(
                        title=flet.Text("Film"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.3)
                    ),flet.ListTile(
                        title=flet.Text("Actor"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.4)
                    ),flet.ListTile(
                        title=flet.Text("Category"),
                        content_padding=flet.padding.only(left=40),
                        on_click=lambda e: on_nav_change(4.5)
                    ),
                ]
            ),flet.Divider(
            ),flet.ListTile(
                leading=flet.Icon(flet.Icons.QUERY_STATS),
                title=flet.Text("Statistic"),
                on_click=lambda e: on_nav_change(5)
            ),flet.ListTile(
                leading=flet.Icon(flet.Icons.MANAGE_ACCOUNTS),
                title=flet.Text("Manager"),
                on_click=lambda e: on_nav_change(6)
            ),flet.ListTile(
                leading=flet.Icon(flet.Icons.EXIT_TO_APP),
                title=flet.Text("Exit"),
                on_click=close_pop_open
            )
        ], scroll=flet.ScrollMode.AUTO
    )
    ex_tile = flet.Container(
        width=180,
        bgcolor=flet.Colors.BLUE_GREY_100,
        padding=2,
        border_radius=5,
        content=tile_column
    )
    return ex_tile, basic_content