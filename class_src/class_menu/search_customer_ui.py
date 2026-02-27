import flet
from class_window import Font, Ratios
from class_query import Search
from class_popup import Popup
from material import (input_text, header_text, data_text, context_menu,
                      context_customer_id_data)

def view_header():
    return flet.Container(
        content=flet.Row(
            controls=[
                header_text("Store", expand=Ratios.store),
                flet.VerticalDivider(width=1),
                header_text("Name", expand=Ratios.name),
                flet.VerticalDivider(width=1),
                header_text("Customer ID", expand=Ratios.id),
                flet.VerticalDivider(width=1),
                header_text("Email", expand=Ratios.email),
                flet.VerticalDivider(width=1),
                header_text("Phone", expand=Ratios.phone),
                flet.VerticalDivider(width=1),
                header_text("Address", expand=Ratios.address),
                flet.VerticalDivider(width=1),
                header_text("Create Date", expand=Ratios.date),
                flet.VerticalDivider(width=1),
                header_text("Status", expand=Ratios.status),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=20
        ), margin=5
    )

def view_table(page, store_id, row, status_color, store_color):
    if row[7] == 'Overdue':
        status_color = Font.status_overdue
    if row[8] == store_id:
        if row[0] == '🇦🇺 Woodridge':
            store_color = flet.Colors.ORANGE
        if row[0] == '🇨🇦 Lethbridge':
            store_color = flet.Colors.BLUE
    else:
        store_color = flet.Colors.RED_ACCENT
    return flet.Container(
    content=flet.Row(
        controls=[
            data_text(row[0], expand=Ratios.store, color=store_color),
            flet.VerticalDivider(width=1),
            data_text(row[1], expand=Ratios.name),
            flet.VerticalDivider(width=1),
            data_text(str(row[2]), expand=Ratios.id),
            flet.VerticalDivider(width=1),
            data_text(row[3], expand=Ratios.email),
            flet.VerticalDivider(width=1),
            data_text(row[4], expand=Ratios.phone),
            flet.VerticalDivider(width=1),
            data_text(row[5], expand=Ratios.address),
            flet.VerticalDivider(width=1),
            data_text(str(row[6])[:10], expand=Ratios.date),
            flet.VerticalDivider(width=1),
            flet.Row(expand=Ratios.status, controls=[
                flet.Text(
                    row[7], text_align="center",
                    no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[7],
                    color=status_color, expand=3),
                flet.PopupMenuButton(
                    items=[
                        context_menu(row[1], True, 20, weight=flet.FontWeight.BOLD,
                                     alignment=flet.alignment.center, icon=flet.Icons.PERSON),
                        flet.PopupMenuItem(height=1),
                        context_menu("Rentals Data", icon=flet.Icons.CALENDAR_MONTH,
                                     on_click=lambda e:context_customer_id_data(None, page, row[1], "rental")),
                        context_menu("Payments Data", icon=flet.Icons.ATTACH_MONEY,
                                     on_click=lambda e:context_customer_id_data(None, page, row[1], "payment")),
                        flet.PopupMenuItem(height=1),
                        context_menu("Edit", icon=flet.Icons.MODE_EDIT_OUTLINE,
                                     on_click=lambda e:context_customer_id_data(None, page, row[1], "edit")),
                        context_menu(content="Delete", color=flet.Colors.ERROR,
                                     icon=flet.Icons.DELETE_OUTLINED,
                                     on_click=lambda e:context_customer_id_data(None, page, row[1], "delete")),
                    ], expand=1, shadow_color=flet.Colors.GREY_100, icon=flet.Icons.MENU, icon_size=30,
                    padding=0
                )
            ],)
        ], alignment=flet.MainAxisAlignment.START, spacing=5, height=38
    ), margin=5, border_radius=5, expand=True)

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
            str_customer_name = f"%{input_customer.value.strip()}%"
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
                    print(f"Not Customer Name : {input_customer.value.strip()}")
                    popup.show_error_open(
                        message=f"Customer Name Not Found [{input_customer.value.strip()}]"
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
                    status_color = Font.status_normal
                    store_color = Font.status_normal
                    customer_id_data.controls.append(
                        view_table(page, store_id, row, status_color, store_color)
                    )
                customer_id_data.update()
            else:
                print(f"Customer ID Not Found {int(input_customer.value.strip())}")
                popup.show_error_open(
                    message=f"Customer ID Not Found [{input_customer.value.strip()}]"
                )
                input_customer.focus()
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Customer error : {err}")

    input_customer = input_text(
        " Customer ID or Name ↵", on_submit=query_customer, hint_text=" Press Enter to Search")

    view_customer = flet.Column(
        controls=[
            view_header(), customer_id_data
        ],
        expand=True, spacing=5
    )

    return input_customer, view_customer