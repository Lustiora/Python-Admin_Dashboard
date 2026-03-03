import flet
from class_window import Font, Ratios, Colors

def input_text(content=None, on_submit=None, hint_text=None, value=None, autofocus=True):
    return flet.TextField(label=content, on_submit=on_submit, hint_text=hint_text, value=value,
       text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=autofocus
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

def details_btn(text:str, disabled=None, action=None):
    if disabled is False:
        color = Colors.status_normal_btn_color
        bgcolor = Colors.status_normal_btn_bgcolor
    else:
        color = Colors.status_disabled_btn_color
        bgcolor = Colors.status_disabled_btn_bgcolor
    return flet.Button(
        text,
        width=float('inf'),
        height=50,
        color=color,
        bgcolor=bgcolor,
        disabled=disabled,
        style=flet.ButtonStyle(
            shape=flet.RoundedRectangleBorder(radius=5),
            overlay_color=flet.Colors.INVERSE_PRIMARY
        ),
        on_click=action
    )