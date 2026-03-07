from escpos.printer import File
import os, datetime
import flet

def receipt_print(action, **receipt_data):
    now = datetime.datetime.now()
    popup = receipt_data["popup"]

    store_address = receipt_data["store_address"]
    payment_id = receipt_data["id"]
    payment_date = receipt_data["date"]
    user_name = receipt_data["name"]
    subtotal = receipt_data["subtotal"]
    tax = receipt_data["tax"]
    total_text = receipt_data["total_text"]
    total = receipt_data["total"]
    if action == "print":
        # Viewer
        # https://receiptline.github.io/designer/

        appdata = os.path.join(os.path.expanduser("~"), "Documents")
        if not os.path.exists(appdata):
            try:
                os.makedirs(appdata)
            except PermissionError:
                appdata = os.getcwd()

        file_path = os.path.join(appdata, f"receipt_{payment_id}_{now.strftime('%Y-%m-%d')}_{now.strftime('%H%M%S')}.bin")
        p = File(file_path)

        with open("class_src/assets/logo.pbm", "rb") as f:
            f.readline() # 1 Line Not Read
            f.readline()
            raw_bitmap_data = f.read()
            header = b'\x1d\x76\x30\x00\x10\x00\x80\x00' # W128 H128 pbm image

        p._raw(header) # _raw : Use Binary Data
        p._raw(raw_bitmap_data)
        p.ln(2)

        p.text("^^Payment Receipt\n")
        p.ln(1)
        p.text(f"|Store : {store_address}\n")
        p.text(f"|Receipt ID : || \"{payment_id}\n")
        p.text("|Date :\n")
        p.text(f"| \"{payment_date}\n")
        p.text("|Name :\n")
        p.text(f"| \"{user_name}\n")

        p.text("\n-\n")
        p.ln(1)
        p.text("|_Film || _\"Rate($)\n")
        p.ln(1)
        for data in receipt_data["receipt_data"]:
            p.text(f"|{data[0]}\n") # Film Title
            p.text(f"| \"${data[1]}\n") # Film Rate
        p.text("\n-\n")
        p.ln(1)

        p.text(f"|Sub Total : || {subtotal}\n")
        p.text(f"|Tax : || {tax}\n")
        p.text(f"|\"{total_text}\n")
        p.text(f"| \"{total}\n")
        p.text("\n-\n")
        p.ln(1)

        p.text("{code:")
        p.text(f"{payment_id}")
        p.text("; option:code39,4,72,nohri}\n")
        p.ln(1)
        p.text("|Print Date :\n")
        p.text(f"| {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        p.ln(1)
        p.cut()

        popup.show_popup_open(
            title="Receipt",
            content=flet.Text(
                spans=[
                    flet.TextSpan(f"Payment Receipt Print Success.\n\n"),
                    flet.TextSpan(file_path, style=flet.TextStyle(color="green")),
                ]
            )
        )
    elif action == "email":
        popup.show_popup_open(
            title="Receipt",
            message="Feature not implemented. Email Receipt.")