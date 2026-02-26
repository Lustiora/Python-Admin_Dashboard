import flet
from class_window import Font, Ratios

def input_text(content=None, on_submit=None, hint_text=None):
    return flet.TextField(label=content, on_submit=on_submit, hint_text=hint_text,
       text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=True
    )

def header_text(content=None, expand=None):
    return flet.Text(
        content, expand=expand, text_align="center", no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS,
    )

def data_text(content=None, expand=None, color=None, max_lines=None, text_align="center"):
    return flet.Text(
        content, expand=expand, text_align=text_align,
        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=content, color=color, max_lines=max_lines
    )

def context_menu(content, disabled=False, height=35, color=flet.Colors.BLACK, weight=None, alignment=flet.alignment.center_left, icon=None):
    return flet.PopupMenuItem(
        content=flet.Container(
            content=flet.Row([flet.Icon(icon, color=color),flet.Text(value=content, color=color, weight=weight)]),
            expand=True,
            alignment=alignment
        ), disabled=disabled, height=height,
    )