import flet
from class_window import Font, Ratios
from class_query import Search
from class_popup import Popup

def build_customer_ui(page, store_id, conn):
    popup = Popup(page=page)
    customer_id_data = flet.ListView(expand=True, spacing=0)
    def query_customer(e):
        cart_customer_id = [] # ID 상자
        try:
            cart_customer_id.append(int(input_customer.value)) # ANY(%s) 조회를 위해 상자 보관
            # cart_customer_id = int(input_customer.value) -> ID 상자를 만들지 않는 경우 사용가능 | ANY(%s) -> ERROR
            # print(f"Search Customer ID : {int(input_customer.value)}")
        except:
            str_customer_name = f"%{input_customer.value}%"
            # print("Not ID -> Name Search")
            cursor = conn.cursor()
            try:
                cursor.execute(Search.customer_name_query,(str_customer_name,str_customer_name,))
                customer_name_id = cursor.fetchall()
                if customer_name_id:
                    # print(f"Name Check : {input_customer.value}")
                    for row in customer_name_id: # 검색어에 해당하는 ID 값들을 상자에 보관하기 위한 반복
                        cart_customer_id.append(row[0]) # .append로 상자에 보관
                    # print(f"List Check : {cart_customer_id}")
                else:
                    print(f"Not Customer Name : {input_customer.value}")
                    popup.show_error_open(
                        message=f"Customer Name Not Found [{input_customer.value}]"
                    )
                    input_customer.focus()
                    return # 조회 실패시 쿼리 실행 방지
                conn.commit()
            except Exception as err:
                conn.rollback()
                print(f"Error. Customer Search : {err}")
                popup.show_error_open(
                    message="Error. Customer Search"
                )
                input_customer.focus()
                return # 조회 실패시 쿼리 실행 방지
        cursor = conn.cursor()
        try:
            cursor.execute(Search.customer_id_query,(cart_customer_id,))
            customer_data = cursor.fetchall()
            if customer_data:
                customer_id_data.controls.clear()
                for row in customer_data:
                    status_color = flet.Colors.BLACK
                    store_color = flet.Colors.BLACK
                    if row[7] == 'Overdue':
                        status_color = flet.Colors.RED_ACCENT
                    if row[8] == store_id:
                        if row[0] == '🇦🇺 Woodridge':
                            store_color = flet.Colors.ORANGE
                        if row[0] == '🇨🇦 Lethbridge':
                            store_color = flet.Colors.BLUE
                    else:
                        store_color = flet.Colors.RED_ACCENT
                    customer_id_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    flet.Text(
                                        row[0], expand=Ratios.store, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[0], color=store_color),
                                    flet.VerticalDivider(width=1),
                                    flet.Text(
                                        row[1], expand=Ratios.name, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    flet.VerticalDivider(width=1),
                                    flet.Text(
                                        str(row[2]), expand=Ratios.id, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[2])),
                                    flet.VerticalDivider(width=1),
                                    flet.Text(
                                        row[3], expand=Ratios.email, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[3]),
                                    flet.VerticalDivider(width=1),
                                    flet.Text(
                                        row[4], expand=Ratios.phone, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[4]),
                                    flet.VerticalDivider(width=1),
                                    flet.Text(
                                        row[5], expand=Ratios.address, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                    flet.VerticalDivider(width=1),
                                    flet.Text(
                                        str(row[6])[:10], expand=Ratios.date, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[6])[:10]),
                                    flet.VerticalDivider(width=1),
                                    flet.Text(
                                        row[7], expand=Ratios.status, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[7], color=status_color),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                customer_id_data.update()
            else:
                print(f"Not Customer ID : {int(input_customer.value)}")
                popup.show_error_open(
                    message=f"Customer ID Not Found [{input_customer.value}]"
                )
                input_customer.focus()
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Customer error : {err}")
    input_customer = flet.TextField(label=" Customer ID or Name ↵", on_submit=query_customer, hint_text=" Press Enter to Search",
        text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=True)
    header = flet.Container(
        content = flet.Row(
            controls=[
                flet.Text("Store", expand=Ratios.store, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Name", expand=Ratios.name, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("ID", expand=Ratios.id, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Email", expand=Ratios.email, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Phone", expand=Ratios.phone, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Address", expand=Ratios.address, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Create Date", expand=Ratios.date, text_align="center"),
                flet.VerticalDivider(width=1),
                flet.Text("Status", expand=Ratios.status, text_align="center"),
            ], alignment=flet.MainAxisAlignment.START, spacing=5
        ), padding=10, border_radius=5, height=40
    )
    view_customer = flet.Column(
        controls=[
            header, customer_id_data
        ],
        expand=True, spacing=5
    )
    return input_customer, view_customer