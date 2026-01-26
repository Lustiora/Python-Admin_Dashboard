# -- Import --
import flet
# -- Menubar --
def menu_bar():
    def open_pop(e):
        e.page.open(main_quit)
    def close_pop(e):
        e.page.close(main_quit)  # 팝업창 종료 명령어
    def close_main(e):
        e.page.window.close()  # 윈도우 창 종료 명령어
    main_quit = flet.AlertDialog(
        title=flet.Text("Quit"),
        content=flet.Text("Exit?"),
        actions=[flet.TextButton("OK", on_click=close_main),
                 flet.TextButton("Cancel", on_click=close_pop)
                 ], actions_alignment=flet.MainAxisAlignment.END)
    def handle_menu_item_click(e):
        print(f"{e.control.content.value}.on_click")

    return flet.Row(
            [
                flet.MenuBar(
                    expand=True,
                    style=flet.MenuStyle(
                        alignment=flet.Alignment(-1,-1),
                        bgcolor=flet.Colors.RED_100,
                        mouse_cursor={
                            flet.ControlState.HOVERED: flet.MouseCursor.WAIT,
                            flet.ControlState.DEFAULT: flet.MouseCursor.ZOOM_OUT,
                        },
                    ),
                    controls=[
                        flet.SubmenuButton(
                            content=flet.Text("File"),
                            controls=[
                                flet.MenuItemButton(
                                    content=flet.Text("Status"),
                                    leading=flet.Icon(flet.Icons.INFO),
                                    style=flet.ButtonStyle(
                                        bgcolor={
                                            flet.ControlState.HOVERED: flet.Colors.GREEN_100
                                        }
                                    ),
                                    on_click=handle_menu_item_click,
                                ),
                                flet.MenuItemButton(
                                    content=flet.Text("Quit"),
                                    leading=flet.Icon(flet.Icons.CLOSE),
                                    style=flet.ButtonStyle(
                                        bgcolor={
                                            flet.ControlState.HOVERED: flet.Colors.GREEN_100
                                        }
                                    ),
                                    on_click=open_pop,
                                ),
                            ],
                        ),
                        flet.SubmenuButton(
                            content=flet.Text("View"),
                            controls=[
                                flet.SubmenuButton(
                                    content=flet.Text("Zoom"),
                                    controls=[
                                        flet.MenuItemButton(
                                            content=flet.Text("Magnify"),
                                            leading=flet.Icon(flet.Icons.ZOOM_IN),
                                            close_on_click=False,
                                            style=flet.ButtonStyle(
                                                bgcolor={
                                                    flet.ControlState.HOVERED: flet.Colors.PURPLE_200
                                                }
                                            ),
                                            on_click=handle_menu_item_click,
                                        ),
                                        flet.MenuItemButton(
                                            content=flet.Text("Minify"),
                                            leading=flet.Icon(flet.Icons.ZOOM_OUT),
                                            close_on_click=False,
                                            style=flet.ButtonStyle(
                                                bgcolor={
                                                    flet.ControlState.HOVERED: flet.Colors.PURPLE_200
                                                }
                                            ),
                                            on_click=handle_menu_item_click,
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                )
            ]
        )