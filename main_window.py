# -- Import --
import flet
from menubar.menubar import menu_bar
# -- Module --
def main_window(page: flet.Page):
    # -- Frame --
    page.title = "Sakila"
    page.window.width = 1024
    page.window.height = 768
    page.window.resizable = True
    page.window.min_width = 1024
    page.window.min_height = 768
    page.vertical_alignment = flet.MainAxisAlignment.START
    page.window.center()
    # -- Menubar --
    page.add(menu_bar())
    # -- Statusbar --

    # -- Update --
    page.update()
# -- Run Test --
# flet.app(target=main_window)