import flet, os, datetime, csv
from math import ceil
from window_setting import Colors, Ratios
from window_popup import Popup
from full_query import Search
import material as mat
from printing import receipt_print

def view_table(conn, row, receipt_details, receipt_container, status_normal, status_color, btn_color, btn_bgcolor, store_address, popup):
    if "Overdue" in row[7]:
        status = row[7].split(" (")[0]
        days = row[7].split("due ")[1]
    else:
        status = row[7]
        days = ""
    payment_id = str(row[0])
    receipt_view = flet.Text("Receipt View", max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    return flet.Container(
        content=flet.Row(
            controls=[
                flet.Row([
                    flet.Container(width=4),
                    mat.data_text(payment_id, color=status_normal, expand=True,max_lines=1),
                ], expand=Ratios.id, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    mat.data_text(row[1], color=status_normal, expand=True, max_lines=1),
                ], expand=Ratios.name, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    mat.data_text(str(row[2]), color=status_normal, expand=True, max_lines=2, text_align="left"),
                ], expand=Ratios.date, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    flet.Column([
                        mat.data_text(row[3], color=status_normal, max_lines=1),
                        mat.data_text(row[8], color=status_normal, max_lines=1),
                    ],expand=True, spacing=0),
                    flet.Container(width=4),
                ], expand=Ratios.title, alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    mat.data_text(f"${str(row[4])}", color=status_normal, expand=True, max_lines=1),
                ], expand=Ratios.total_rate, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    flet.Column([
                        mat.data_text(status, color=status_color, max_lines=1),
                        mat.data_text(days, color=status_color, max_lines=1),
                    ], expand=True, spacing=0),
                ], expand=Ratios.status, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Button(content=receipt_view, expand=Ratios.status,
                            on_click=lambda e:view_open_receipt(None, conn, receipt_details, receipt_container, payment_id, store_address, popup),
                            color=btn_color, bgcolor=btn_bgcolor,
                            style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=5),
                                                   overlay_color=flet.Colors.INVERSE_PRIMARY)),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=38
        ), margin=5, border_radius=5, expand=True
    )

def view_header():
    return flet.Container(
        content=flet.Row(
            controls=[
                mat.header_text("ID", expand=Ratios.id),
                flet.VerticalDivider(width=1),
                mat.header_text("Name", expand=Ratios.name),
                flet.VerticalDivider(width=1),
                mat.header_text("Payment Date", expand=Ratios.date),
                flet.VerticalDivider(width=1),
                mat.header_text("Title", expand=Ratios.title),
                flet.VerticalDivider(width=1),
                mat.header_text("Total Amount", expand=Ratios.total_rate),
                flet.VerticalDivider(width=1),
                mat.header_text("Status", expand=Ratios.status),
                flet.VerticalDivider(width=1),
                mat.header_text("Actions", expand=Ratios.status),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=20
        ), margin=5, border_radius=5
    )

def view_table_payment_data(conn, payment_data, payment_id_data, connect_module, connect_module_count,
                            connect_module_page:int, query, page_num, select_page, receipt_details, receipt_container, store_address, popup):
    # print(f"page_num.selected_index : {page_num.selected_index}")
    # print(f"connect_module_page : {connect_module_page}")
    # print(f"connect_module : {connect_module}")
    page_sync = [connect_module_page]
    # print(f"page_sync : {page_sync}")
    # print(f"select_page : {select_page}")
    if page_sync != connect_module:
        page_num.selected_index = 0
    if select_page is None:
        page_num.selected_index = 0
    count_pages = []
    count_pages.clear()
    page_num.visible = True
    if payment_id_data:
        connect_module_count.clear()
        payment_data.controls.clear()
        for row in payment_id_data:
            status_normal = Colors.status_overdue
            status_color = Colors.status_overdue
            btn_color = Colors.status_overdue_btn_color
            btn_bgcolor = Colors.status_overdue_btn_bgcolor
            if row[7] == 'Returned':
                status_normal = Colors.status_normal
                status_color = Colors.status_returned
                btn_color = Colors.status_normal_btn_color
                btn_bgcolor = Colors.status_normal_btn_bgcolor
            if row[7] == 'Unreturned':
                status_normal = Colors.status_normal
                status_color = Colors.status_unreturned
                btn_color = Colors.status_unreturned_btn_color
                btn_bgcolor = Colors.status_unreturned_btn_bgcolor
            payment_data.controls.append(
                view_table(conn, row, receipt_details, receipt_container, status_normal, status_color, btn_color, btn_bgcolor, store_address, popup)
            )
            connect_module_count.append(row[0])
        connect_module.clear()
        connect_module.append(connect_module_page)
        connect_module_count.clear()
        count = int(ceil(query / 10))
        for i in range(count):
            pages = str(i + 1)
            count_pages.append(flet.Text(pages))
        if len(count_pages) <= 1:
            page_num.visible = False
        else:
            page_num.controls = count_pages
        if page_num.page:
            page_num.update()
        if payment_data.page:
            payment_data.update()
    else:
        page_num.visible = False
        if page_num.page:
            page_num.update()
        if payment_data.page:
            payment_data.update()
        payment_data.controls.clear()
        payment_data.controls.append(
            flet.Container(content=flet.Row(controls=[flet.Text("Not Data"), ],
                                            alignment=flet.MainAxisAlignment.CENTER, )))
        payment_data.update()
    # print(f"count_pages : {count_pages}")

def receipt(conn, store_address, popup, payment_id:int=None):
    payment_film_data = flet.ListView(expand=True, spacing=0)
    payment_receipt_data = []
    view_payment_id = flet.Text("ID", weight=flet.FontWeight.BOLD)
    view_payment_date = flet.Text("Date", weight=flet.FontWeight.BOLD, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    view_payment_name = flet.Text("Name", weight=flet.FontWeight.BOLD, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    view_payment_subtotal = flet.Text("Sub")
    view_payment_tax = flet.Text("TAX")
    view_payment_total_text = flet.Text("Total:", weight=flet.FontWeight.BOLD, width=170, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    view_payment_total_amount = flet.Text("Total", weight=flet.FontWeight.BOLD)

    tmdb_api_image = "https://image.tmdb.org/t/p/w200"

    cursor = conn.cursor()
    try:
        payment_film_data.controls.clear()
        cursor.execute(Search.payment_receipt_query,(payment_id,))
        data = cursor.fetchone()
        if data:
            view_payment_id.value = data[0]
            view_payment_date.value = data[1]
            view_payment_name.value = data[2]
            view_payment_total_text.value = f"{data[4]}:"
            view_payment_subtotal.value = f"${data[6]:.2f}"
            view_payment_tax.value = f"${data[7]:.2f}"
            view_payment_total_amount.value = f"${data[8]:.2f}"
        film_data = cursor.fetchall()
        if film_data:
            for row in film_data:
                payment_receipt_data.append([row[4], str(row[5])])
                payment_film_data.controls.append(
                    flet.Container(
                        expand=True,
                        padding=10,
                        content=flet.Column([
                            flet.Row([
                                flet.Image(src=f"{tmdb_api_image}{row[3]}",width=60, height=90),
                                flet.Column([
                                    flet.Text(row[4], expand=True, no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, max_lines=3),
                                    flet.Text(row[5])
                                ], expand=True,)
                            ]),
                            flet.Divider(height=1),
                        ], spacing=20)
                    )
                )
        def printing(e, action):
            payment_receipt_print = {
                "id": data[0],
                "date": data[1],
                "name": data[2],
                "subtotal": f"${data[6]:.2f}",
                "tax": f"${data[7]:.2f}",
                "total": f"${data[8]:.2f}",
                "total_text": f"{data[4]}:",
                "store_address": store_address,
                "receipt_data": payment_receipt_data,
                "popup": popup,
            }
            receipt_print(action, **payment_receipt_print)
        if payment_film_data.page:
            payment_film_data.update()
        conn.commit()
    except Exception as err:
        conn.rollback()
        print(f"Error : {err}")
    return flet.Column([
        flet.Row([flet.Text("Receipt ID:"),view_payment_id,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Row([flet.Text("Date:"),view_payment_date,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Row([flet.Text("Customer:"),view_payment_name,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Divider(height=1),
        payment_film_data,
        flet.Divider(height=1),
        flet.Row([flet.Text("Subtotal:"), view_payment_subtotal,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Row([flet.Text("Tax (10%):"), view_payment_tax,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Row([view_payment_total_text, view_payment_total_amount,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        mat.details_btn("Print Receipt", action=lambda e: printing(e,"print")),
        mat.details_btn("Email Receipt", action=lambda e: printing(e,"email")),
    ], expand=True, width=250)

def view_open_receipt(e, conn, receipt_details, receipt_container, payment_id, store_address, popup):
    # print("open receipt")
    if not payment_id:
        return
    else:
        receipt_details.visible = True
        receipt_container.content = receipt(conn, store_address, popup, payment_id)
        receipt_details.update()

def view_close_receipt(e, receipt_details):
    # print("close receipt")
    receipt_details.visible = False
    receipt_details.update()

def export_csv(e, export_data):
    now = datetime.datetime.now()
    appdata = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(appdata):
        try:
            os.makedirs(appdata)
        except PermissionError:
            appdata = os.getcwd()
    file_path = os.path.join(appdata, f"payment_data_{now.strftime('%Y-%m-%d')}_{now.strftime('%H%M%S')}.csv")

    column = ["Payment ID", "Name", "Payment Date", "Film Title", "Total Amount", "Status"]
    with open(file_path, "w", encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column)
        writer.writerows(export_data)
        print("Save Payment Data")

def build_payment_ui(initial_value="", **kwargs):
    page = kwargs.get("page")
    popup = Popup(page=page)
    store_id = kwargs.get("staff_store_id")
    store_address = kwargs.get("staff_store_address")
    conn = kwargs.get("conn")
    payment_data = flet.ListView(expand=True, spacing=0)
    view_page = 0
    connect_module = []
    connect_module_count = []

    def select_view_page(select_page):
        # print("try")
        try:
            if 0 in connect_module: # 검색 조회
                # print(f"Search load {select_page}")
                view_page = int(select_page) * 10
                payment_search_data_query(None, view_page, select_page, store_address)
        except:
            print(f"Error select view page {connect_module}")
            return

    def payment_search_data_query(e, view_page, select_page, store_address, initial_value=None):
        connect_module_page = 0
        cart_payment_id = []
        connect_count = []
        if not input_payment.value.strip():
            popup.show_popup_open(
                message="Please enter your payment id or customer name."
            )
            input_payment.focus()
            return
        try:
            cart_payment_id.append(int(input_payment.value))
        except:
            if initial_value:
                customer_name = f"%{initial_value}%"
                input_data = initial_value
            else:
                customer_name = f"%{input_payment.value.strip()}%"
                input_data = input_payment.value
            cursor = conn.cursor()
            try:
                cursor.execute(Search.payment_search_name_query, (store_id, customer_name))
                customer_name_list = cursor.fetchall()
                if customer_name_list:
                    for row in customer_name_list:
                        cart_payment_id.append(row[0])
                else:
                    print(f"Customer not found or no Payment history at this location. : {input_data}")
                    popup.show_popup_open(
                        message="Customer not found or no Payment history at this location."
                    )
                    if not initial_value:
                        input_payment.focus()
                    return
                conn.commit()
            except Exception as err:
                conn.rollback()
                print(f"Error. Customer Name Search {err}")
        cursor = conn.cursor()
        if cart_payment_id:
            connect_module_count.clear()
            cursor.execute(Search.payment_search_count_query, (store_id, cart_payment_id,))
            connect_count.append(cursor.fetchone())
            for count in connect_count:
                connect_module_count.append(int(count[0]))
        try:
            cursor = conn.cursor()
            cursor.execute(Search.payment_search_id_query, (store_id, cart_payment_id, view_page,))
            payment_id_data = cursor.fetchall()
            if not payment_id_data:
                print(f"Payment ID Not Found {input_payment.value}")
                input_payment.focus()
                popup.show_popup_open(
                    message=f"Payment ID Not Found [{input_payment.value}]"
                )
            view_table_payment_data(conn, payment_data, payment_id_data, connect_module, connect_module_count,
                                    connect_module_page, connect_module_count[0], page_num, select_page, receipt_details, receipt_container, store_address, popup)
            conn.commit()
            if export_btn.page:
                export_btn.disabled = False
                export_btn.color = Colors.status_normal_btn_color
                export_btn.border_color = Colors.status_normal_btn_color
                export_btn.on_click = lambda e: export_csv(e, payment_id_data)
                export_btn.update()
        except Exception as err:
            conn.rollback()
            print(f"Search Payment error : {err}")

    def search_payment(e, view_page, select_page):
        page_num.selected_index = 0
        receipt_details.visible = False
        receipt_details.update()
        payment_search_data_query(e, view_page, select_page, store_address)

    page_num = flet.CupertinoSlidingSegmentedButton(
        visible=False,  # True = 표시, False = 숨김
        selected_index=0,
        on_change=lambda e: select_view_page(e.data),
        controls=[
            flet.Text("Min"),
            flet.Text("Max"),
        ])

    page_row = flet.Container(
        height=40,
        content=flet.Row(
            height=40,
            controls=[
                flet.Row(
                    controls=[page_num],
                    expand=True,
                    scroll=flet.ScrollMode.AUTO,
                )]))

    input_payment = mat.input_text(" Payment ID or Customer Name ↵", value=initial_value,
        on_submit=lambda e:search_payment(None, view_page, 0),
        hint_text=" Press Enter to Search"
    )

    receipt_container = flet.Container(
        content=receipt(conn, store_address, popup),
        expand=True,
        padding=10,
        border_radius=5,
        border=flet.border.all(color=Colors.border_color),
    )

    receipt_details = flet.Row([
        flet.VerticalDivider(width=1),
        flet.Column(
            controls=[
                flet.Row([
                    flet.Container(
                        expand=3,
                        alignment=flet.alignment.center_left,
                        padding=flet.padding.only(left=10),
                        content=flet.Text("Receipt Details", style=flet.TextThemeStyle.TITLE_LARGE,
                            weight=flet.FontWeight.BOLD),
                    ), flet.Container(
                        expand=1,
                        alignment=flet.alignment.center_right,
                        content=flet.IconButton(
                            icon=flet.Icons.CLOSE_ROUNDED,
                            on_click=lambda e:view_close_receipt(None, receipt_details)
                        ),
                    ),
                ], height=40, spacing=0,
                ), receipt_container
            ], width=250,
        )
    ], spacing=20, visible=False,)

    export_btn = flet.Button(
        text="Export",
        color=Colors.status_disabled_btn_color,
        bgcolor=Colors.status_disabled_btn_bgcolor,
        disabled=True,
        style=flet.ButtonStyle(
            shape=flet.RoundedRectangleBorder(radius=5),
            overlay_color=flet.Colors.INVERSE_PRIMARY
        )
    )

    view_payment = flet.Column(
        expand=True,
        spacing=5,
        controls=[view_header(), payment_data, page_row]
    )

    if initial_value:
        payment_search_data_query(None, 0, 0, initial_value)
        input_payment.autofocus = False

    return input_payment, view_payment, receipt_details, export_btn