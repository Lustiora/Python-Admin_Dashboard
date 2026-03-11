import flet
from window_setting import Font, Ratios, Colors

# ================================================
#   search.py
# ================================================
def view_container(view_content):
    return flet.Container(
        alignment=flet.alignment.top_left,
        expand=True,
        content=flet.SelectionArea(content=view_content),
        border_radius=5,
        border=flet.border.all(color=Colors.border_color),
    )

# ================================================
#   navigation_tile.py
# ================================================
def list_tile(title, event, index=None, icon=None):
    return flet.ListTile(
        leading=flet.Icon(icon),
        title=flet.Text(title),
        on_click=lambda e: event(index)
    )

def list_tile_menu(title, event, index):
    return flet.ListTile(
        title=flet.Text(title),
        content_padding=flet.padding.only(left=40),
        on_click=lambda e: event(index)
    )

# ================================================
#   search_...ui.py
# ================================================
def input_text(content=None, on_submit=None, hint_text=None, value=None, height=None, autofocus=True):
    return flet.TextField(label=content, on_submit=on_submit, hint_text=hint_text, value=value,
        text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=autofocus,
        border_color=Colors.border_color, height=height
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