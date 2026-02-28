import flet

class Popup:
    def __init__(self, page: flet.Page):
        self.page = page

        self.main_quit = flet.AlertDialog(
            modal=True,
            title=flet.Text("Quit"),
            content=flet.Text("Exit?"),
            actions_alignment = flet.MainAxisAlignment.END,
            actions=[
                flet.TextButton("OK", on_click=self.show_main_close, autofocus=True),
                flet.TextButton("Cancel", on_click=self.show_close)
            ]
        )

        self.error = flet.AlertDialog(
            modal=True,
            title=flet.Text("Failed"),
            content=flet.Text("Your ID or password is incorrect."),
            actions_alignment=flet.MainAxisAlignment.END,
            actions=[
                flet.TextButton("OK", on_click=self.show_error_close, autofocus=True),
            ]
        )

    # noinspection PyCallingNonCallable : 밑줄 코드 Pycharm 경고 제거

    def show_open(self, e):
        if e.data == "close":
            # noinspection PyCallingNonCallable
            self.page.open(self.main_quit)

    def show_close(self, e):
        self.page.close(self.main_quit)  # 팝업창 종료 명령어

    def show_main_close(self, e):
        self.page.window.close()
        self.page.window.destroy()  # 윈도우 창 종료 명령어

    def show_error_open(self, message: str, actions=None, title=None):
        self.error.content.value = message
        if actions is not None:
            self.error.actions = actions
        else:
            self.error.actions = [
                flet.TextButton("OK", on_click=self.show_error_close, autofocus=True),
            ]
        if title is not None:
            self.error.title.value = title
        else:
            self.error.title.value = "Failed"
        # noinspection PyCallingNonCallable
        self.page.open(self.error)

    def show_error_close(self, e):
        self.page.close(self.error)