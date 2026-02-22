import flet
from window import Font, Ratios

def build_payment_ui():
    input_payment = flet.TextField(
            hint_text=" Press Enter to Search", on_submit="", label=" Payment ID or Customer Name ↵",
            text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=True)
    receipt_details = (
        flet.Column([
            flet.Row([
                flet.Column([
                    flet.Text("Receipt ID:"),
                    flet.Text("Date:"),
                    flet.Text("Customer:")
                ], expand=1, horizontal_alignment=flet.CrossAxisAlignment.START),
                flet.Column([
                    flet.Text("ID"),
                    flet.Text("Time"),
                    flet.Text("Name")
                ], expand=1, horizontal_alignment=flet.CrossAxisAlignment.END)
            ]),
            flet.Divider(height=1),
            flet.Container(expand=1), # 영수증 결제 목록 리스트 출력예정 (스크롤)
            flet.Divider(height=1),
            flet.Row([
                flet.Column([
                    flet.Text("Subtotal:"),
                    flet.Text("Tax (10%):"),
                    flet.Text("Total:", weight=flet.FontWeight.BOLD)
                ], expand=1, horizontal_alignment=flet.CrossAxisAlignment.START),
                flet.Column([
                    flet.Text("$$"),
                    flet.Text("$"),
                    flet.Text("$$$", weight=flet.FontWeight.BOLD)
                ], expand=1, horizontal_alignment=flet.CrossAxisAlignment.END)
            ]),
            flet.Button("Print Receipt", width=200,
                        color=flet.Colors.ON_PRIMARY_CONTAINER,
                        bgcolor=flet.Colors.PRIMARY_CONTAINER,
                        style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=5), overlay_color=flet.Colors.INVERSE_PRIMARY)),
            flet.Button("Email Receipt", width=200,
                        color=flet.Colors.ON_PRIMARY_CONTAINER,
                        bgcolor=flet.Colors.PRIMARY_CONTAINER,
                        style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=5), overlay_color=flet.Colors.INVERSE_PRIMARY)),
        ], height=1, alignment=flet.MainAxisAlignment.SPACE_BETWEEN)
    )
    return input_payment, receipt_details