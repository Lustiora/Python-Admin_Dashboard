import flet
from window_popup import Popup
from window_setting import Font, Colors, Ratios
import material as mat

class Code:
    page_content_id = flet.TextField(label="Customer ID :", expand=True, content_padding=10, read_only=True,
                                     text_align="center", color=Colors.customer_id, border_color=Colors.border_color)

def rent(**kwargs):
    print("Rent Page")
    page = kwargs.get("page")
    staff_store_id = kwargs.get("staff_store_id")
    conn = kwargs.get("conn")
    popup = Popup(page=page)
    customer_list = flet.ListView(expand=True, spacing=0)

    customer_list.controls.clear()

    customer_list.controls.append(
        flet.Container(
            margin=flet.margin.only(top=10),
            content=flet.Row(
                expand=True,
                spacing=5,
                height=20,
                alignment=flet.MainAxisAlignment.START,
                controls=[
                    mat.data_text("ID 1", expand=Ratios.id),
                    flet.VerticalDivider(width=1),
                    mat.data_text("Name 1", expand=Ratios.name),
                    flet.VerticalDivider(width=1),
                    mat.data_text("Status 1", expand=Ratios.status),
                ],
            )
        )
    )
    customer_list.controls.append(
        flet.Container(
            margin=flet.margin.only(top=10),
            content=flet.Row(
                expand=True,
                spacing=5,
                height=20,
                alignment=flet.MainAxisAlignment.START,
                controls=[
                    mat.data_text("ID 2", expand=Ratios.id),
                    flet.VerticalDivider(width=1),
                    mat.data_text("Name 2   2", expand=Ratios.name),
                    flet.VerticalDivider(width=1),
                    mat.data_text("Status 2", expand=Ratios.status),
                ],
            )
        )
    )

    if customer_list.page:
        customer_list.update()

    def rent_page_close(e):
        page.close(rent_page)

    rent_page_main = flet.Column(
        expand=4,
        controls=[
            flet.Row(
                controls=[
                    flet.Icon(flet.Icons.PERM_MEDIA),
                    flet.Text("DVD Rent", size=Font.big_fontsize, weight="bold"),
                    flet.TextField(
                        expand=Ratios.id, content_padding=flet.padding.only(left=10, right=10, top=5, bottom=5), max_length=30, autofocus=True,
                        border_color=Colors.border_color, height=30, on_submit="", hint_text="Customer ID or Barcode",),
                    flet.Button("Search", on_click="", width=150),
                    # flet.Button("Inventory Search", on_click="", width=150),
                ]
            ),
            flet.Divider(),
            flet.Container(
                content=flet.Row(
                    alignment=flet.MainAxisAlignment.START,
                    spacing=5,
                    height=20,
                    controls=[
                        mat.header_text("Customer ID", expand=Ratios.id),
                        flet.VerticalDivider(width=1),
                        mat.header_text("Customer Name", expand=Ratios.name),
                        flet.VerticalDivider(width=1),
                        mat.header_text("Customer Status", expand=Ratios.status),
                    ]
                )
            ), customer_list
        ]
    )

    rent_page_side = flet.Column(
        expand=1,
        spacing=15,
        alignment=flet.MainAxisAlignment.CENTER,
        controls=[
            flet.Row(
                alignment=flet.MainAxisAlignment.CENTER,
                controls=[
                    flet.Button("Customer ID", on_click="", width=100),
                ]
            ),
            flet.Row(
                alignment=flet.MainAxisAlignment.CENTER,
                controls=[
                    flet.Button("Inventory ID", on_click="", width=100),
                ]
            ),
            flet.Divider(),
            flet.Text("All Amount"),
            flet.Text("Tax"),
            flet.Text("Total Amount"),
            flet.Divider(),
            flet.Row(
                alignment=flet.MainAxisAlignment.CENTER,
                controls=[
                    flet.Button("Payment", on_click="", width=100),
                ]
            ),
        ]
    )

    rent_page = flet.AlertDialog(
        modal=True,
        inset_padding=10,
        content_padding=10,
        actions_padding=flet.padding.only(top=-5, bottom=10, left=0, right=10),
        actions=[flet.Button("Cancel", on_click=rent_page_close)],
        content=flet.Column(
            width=800,
            height=360,
            spacing=0,
            offset=flet.Offset(0, 0),
            animate_offset=flet.Animation(600, flet.AnimationCurve.EASE_OUT_BACK),
            controls=[
                flet.Row(
                    spacing=0,
                    expand=True,
                    controls=[
                        rent_page_main,
                        flet.VerticalDivider(),
                        rent_page_side
                    ]
                ),
                flet.Divider(),
            ]
        )
    )

    page.open(rent_page)