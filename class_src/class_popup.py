import flet
import time

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

        self.show = flet.AlertDialog(
            modal=True,
            title=flet.Text("Failed"),
            content=flet.Text("Your ID or password is incorrect."),
            actions_alignment=flet.MainAxisAlignment.END,
            actions=[
                flet.TextButton("OK", on_click=self.show_popup_close, autofocus=True),
            ]
        )

    # noinspection PyCallingNonCallable : 밑줄 코드 Pycharm 경고 제거

    def show_open(self, e):
        if e.data == "close":
            # noinspection PyCallingNonCallable
            self.page.open(self.main_quit)

    def show_close(self, e):
        self.page.close(self.main_quit)  # 팝업창 종료 명령어
        time.sleep(0.1) # Ghost Popup 방지

    def show_main_close(self, e):
        self.page.window.close()
        self.page.window.destroy()  # 윈도우 창 종료 명령어

    def show_popup_open(self, message:str=None, actions=None, title=None, content=None):
        self.show.content.value = message
        if actions is not None:
            self.show.actions = actions
        else:
            self.show.actions = [
                flet.TextButton("OK", on_click=self.show_popup_close, autofocus=True),
            ]
        if title is not None:
            if title == "Null":
                self.show.title = None
            else:
                self.show.title.value = title
        else:
            self.show.title.value = "Failed"
        if content is not None:
            self.show.content = content
        # noinspection PyCallingNonCallable
        self.page.open(self.show)

    def show_popup_close(self, e):
        self.page.close(self.show)
        time.sleep(0.1) # Ghost Popup 방지