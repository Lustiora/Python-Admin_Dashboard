import flet
from class_window import Font, Ratios
from class_popup import Popup
from class_query import Search
from math import ceil

def view_table(conn, row, receipt_details, receipt_container, status_normal, status_color, btn_color, btn_bgcolor):
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
                    flet.Text(
                        payment_id, color=status_normal, expand=True,
                        max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                ], expand=Ratios.id, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    flet.Text(
                        row[1], color=status_normal, expand=True,
                        max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                ], expand=Ratios.name, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    flet.Text(
                        str(row[2]), color=status_normal, expand=True,
                        max_lines=2, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[2])),
                ], expand=Ratios.date, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    flet.Column([
                        flet.Text(
                            row[3], color=status_normal, max_lines=1, tooltip=row[9],
                            overflow=flet.TextOverflow.ELLIPSIS),
                        flet.Text(
                            row[8], color=status_normal, max_lines=1, tooltip=row[9]),
                    ],expand=True, spacing=0),
                    flet.Container(width=4),
                ], expand=Ratios.title, alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    flet.Text(
                        f"${str(row[4])}", color=status_normal, expand=True,
                        max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                ], expand=Ratios.rate, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    flet.Column([
                        flet.Text(
                            status, color=status_color, max_lines=1, tooltip=row[7],
                            overflow=flet.TextOverflow.ELLIPSIS),
                        flet.Text(
                            days, color=status_color, max_lines=1, tooltip=row[7],
                            overflow=flet.TextOverflow.ELLIPSIS),
                    ], expand=True, spacing=0),
                ], expand=Ratios.status, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Button(content=receipt_view, expand=Ratios.status,
                            on_click=lambda e:view_open_receipt(None, conn, receipt_details, receipt_container, payment_id),
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
                flet.Text("ID", expand=Ratios.id, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Name", expand=Ratios.name, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Payment Date", expand=Ratios.date, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Title", expand=Ratios.title, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Total Amount", expand=Ratios.rate, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Status", expand=Ratios.status, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Actions", expand=Ratios.status, text_align="center"),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=38
        ), margin=5, border_radius=5
    )

def view_table_payment_data(conn, payment_data, payment_id_data, connect_module, connect_module_count,
                            connect_module_page:int, query, page_num, select_page, receipt_details, receipt_container):
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
            status_normal = Font.status_overdue
            status_color = Font.status_overdue
            btn_color = Font.status_overdue_btn_color
            btn_bgcolor = Font.status_overdue_btn_bgcolor
            if row[7] == 'Returned':
                status_normal = Font.status_normal
                status_color = Font.status_returned
                btn_color = Font.status_normal_btn_color
                btn_bgcolor = Font.status_normal_btn_bgcolor
            if row[7] == 'Unreturned':
                status_normal = Font.status_normal
                status_color = Font.status_unreturned
                btn_color = Font.status_unreturned_btn_color
                btn_bgcolor = Font.status_unreturned_btn_bgcolor
            payment_data.controls.append(
                view_table(conn, row, receipt_details, receipt_container, status_normal, status_color, btn_color, btn_bgcolor)
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

def receipt(conn, payment_id:int=None):
    payment_film_data = flet.ListView(expand=True, spacing=0)
    view_payment_id = flet.Text("ID", weight=flet.FontWeight.BOLD)
    view_payment_date = flet.Text("Date", weight=flet.FontWeight.BOLD, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    view_payment_name = flet.Text("Name", weight=flet.FontWeight.BOLD, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    view_payment_subtotal = flet.Text("Sub")
    view_payment_tex = flet.Text("TEX")
    view_payment_total_amount = flet.Text("total", weight=flet.FontWeight.BOLD)

    tmdb_api_image = "https://image.tmdb.org/t/p/w200"

    cursor = conn.cursor()
    try:
        payment_film_data.controls.clear()
        cursor.execute(Search.payment_id_receipt_query,(payment_id,))
        data = cursor.fetchone()
        if data:
            view_payment_id.value = data[0]
            view_payment_date.value = data[1]
            view_payment_name.value = data[2]
            view_payment_subtotal.value = f"${data[3]:.2f}"
            view_payment_tex.value = f"${data[4]:.2f}"
            view_payment_total_amount.value = f"${data[5]:.2f}"
        cursor.execute(Search.payment_receipt_query,(payment_id,))
        film_data = cursor.fetchall()
        if film_data:
            for row in film_data:
                payment_film_data.controls.append(
                    flet.Container(
                        expand=True,
                        padding=10,
                        content=flet.Column([
                            flet.Row([
                                flet.Image(src=f"{tmdb_api_image}{row[2]}",width=60, height=90),
                                flet.Column([
                                    flet.Text(row[0]),
                                    flet.Text(row[1])
                                ])
                            ]),
                            flet.Divider(height=1),
                        ], spacing=20)
                    )
                )
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
        flet.Row([flet.Text("Tax (10%):"), view_payment_tex,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Row([flet.Text("Total:", weight=flet.FontWeight.BOLD), view_payment_total_amount,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Button("Print Receipt", width=float('inf'), height=50,
                    color=flet.Colors.ON_PRIMARY_CONTAINER,
                    bgcolor=flet.Colors.PRIMARY_CONTAINER,
                    style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=5),
                                           overlay_color=flet.Colors.INVERSE_PRIMARY)),
        flet.Button("Email Receipt", width=float('inf'), height=50,
                    color=flet.Colors.ON_PRIMARY_CONTAINER,
                    bgcolor=flet.Colors.PRIMARY_CONTAINER,
                    style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=5),
                                           overlay_color=flet.Colors.INVERSE_PRIMARY)),
    ], expand=True, width=250)

def view_open_receipt(e, conn, receipt_details, receipt_container, payment_id):
    # print("open receipt")
    if not payment_id:
        return
    else:
        receipt_details.visible = True
        receipt_container.content = receipt(conn, payment_id)
        receipt_details.update()

def view_close_receipt(e, receipt_details):
    # print("close receipt")
    receipt_details.visible = False
    receipt_details.update()

def build_payment_ui(page, store_id, conn):
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
                payment_search_data_query(None, view_page, select_page)
        except:
            print(f"Error select view page {connect_module}")
            return

    def payment_search_data_query(e, view_page, select_page):
        popup = Popup(page=page)
        connect_module_page = 0
        cart_customer_id = []
        connect_count = []
        try:
            cart_customer_id.append(int(input_payment.value))
            # print(f"Search payment ID {int(input_payment.value)}")
        except:
            customer_name = f"%{input_payment.value}%"
            # print(f"Search Customer Name {input_payment.value}")
            cursor = conn.cursor()
            try:
                cursor.execute(Search.payment_search_name_query, (store_id, customer_name))
                customer_name_list = cursor.fetchall()
                if customer_name_list:
                    for row in customer_name_list:
                        cart_customer_id.append(row[0])
                else:
                    print(f"Customer Name Not Found [{input_payment.value}]")
                    popup.show_error_open(
                        message=f"Customer Name Not Found [{input_payment.value}]"
                    )
                    return
                conn.commit()
            except Exception as err:
                conn.rollback()
                print(f"Error. Customer Name Search {err}")
        cursor = conn.cursor()
        if cart_customer_id:
            connect_module_count.clear()
            cursor.execute(Search.payment_search_count_query, (store_id, cart_customer_id,))
            connect_count.append(cursor.fetchone())
            for count in connect_count:
                connect_module_count.append(int(count[0]))
        try:
            cursor = conn.cursor()
            cursor.execute(Search.payment_search_id_query, (store_id, cart_customer_id, view_page,))
            payment_id_data = cursor.fetchall()
            if not payment_id_data:
                print(f"Customer ID Not Found [{input_payment.value}]")
            view_table_payment_data(conn, payment_data, payment_id_data, connect_module, connect_module_count,
                                    connect_module_page, connect_module_count[0], page_num, select_page, receipt_details, receipt_container)
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Payment error : {err}")

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

    input_payment = flet.TextField(
        hint_text=" Press Enter to Search", on_submit=lambda e:payment_search_data_query(None, view_page, 0),
        label=" Payment ID or Customer Name ↵", text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10,
        max_length=30, autofocus=True)

    receipt_container = flet.Container(
        content=receipt(conn),
        expand=True,
        padding=10,
        border_radius=5,
        border=flet.border.all(color=flet.Colors.BLACK),
    )

    receipt_details = flet.Row([
        flet.VerticalDivider(width=1),
        flet.Column(
            controls=[
                flet.Row([
                    flet.Text("Receipt Details", style=flet.TextThemeStyle.TITLE_LARGE,
                              weight=flet.FontWeight.BOLD),
                    flet.IconButton(
                        icon=flet.Icons.CLOSE_ROUNDED,
                        on_click=lambda e:view_close_receipt(None, receipt_details)),
                ], height=40,),
                receipt_container
            ],
        )
    ], spacing=20, visible=False,)

    view_payment = flet.Column(
        expand=True,
        spacing=5,
        controls=[view_header(), payment_data, page_row]
    )

    return input_payment, view_payment, receipt_details