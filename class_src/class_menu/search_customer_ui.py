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
                header_text("Customer ID", expand=Ratios.id),
                flet.VerticalDivider(width=1),
                header_text("Store", expand=Ratios.store),
                flet.VerticalDivider(width=1),
                header_text("Name", expand=Ratios.name),
                flet.VerticalDivider(width=1),
                header_text("Email", expand=Ratios.email),
                flet.VerticalDivider(width=1),
                header_text("Phone", expand=Ratios.phone),
                flet.VerticalDivider(width=1),
                header_text("Address", expand=Ratios.address),
                flet.VerticalDivider(width=1),
                header_text("Last Rental Date", expand=Ratios.last_date),
                flet.VerticalDivider(width=1),
                header_text("Status", expand=Ratios.status),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=20
        ), margin=5
    )

def view_table(row, input_data, **kwargs):
    page = kwargs.get("page")
    staff_store_id = kwargs.get("staff_store_id")
    conn = kwargs.get("conn")
    status_color = Font.status_normal
    store_color = Font.status_normal
    customer_id = str(row[0])
    customer_store = row[1]
    if row[1] == 1:
        customer_store = "🇨🇦 Lethbridge"
        store_color = Font.store_Lethbridge
    elif row[1] == 2:
        customer_store = "🇦🇺 Woodridge"
        store_color = Font.store_Woodridge
    customer_name = row[2]
    customer_email = row[3]
    customer_phone = row[4]
    customer_address = row[5]
    customer_last_rental_date = row[6]
    customer_status = row[7]
    customer_store_id = row[8]
    customer_last_rental_store_id = row[9]

    rental_flag = None
    if row[9] == 1:
        rental_flag = "🇨🇦 "
    elif row[9] == 2:
        rental_flag = "🇦🇺 "

    customer_params = {
        "page": page,
        "customer_name": customer_name,
        "staff_store_id": staff_store_id,
        "customer_last_rental_store_id": customer_last_rental_store_id,
        "customer_id": customer_id,
        "conn": conn,
        "input_data": input_data,
    }

    if customer_status == 'Overdue':
        status_color = Font.status_overdue
    if not customer_store_id == staff_store_id:
        store_color = flet.Colors.GREY_500

    return flet.Container(
    content=flet.Row(
        controls=[
            data_text(customer_id, expand=Ratios.id),
            flet.VerticalDivider(width=1),
            data_text(customer_store, expand=Ratios.store, color=store_color),
            flet.VerticalDivider(width=1),
            flet.Row([
                flet.Container(width=4),
                data_text(customer_name, color=status_color, expand=True, text_align="left"),
            ], expand=Ratios.name, spacing=0),
            flet.VerticalDivider(width=1),
            data_text(customer_email, expand=Ratios.email),
            flet.VerticalDivider(width=1),
            data_text(customer_phone, expand=Ratios.phone),
            flet.VerticalDivider(width=1),
            data_text(customer_address, expand=Ratios.address),
            flet.VerticalDivider(width=1),
            flet.Row([
                flet.Text(value=rental_flag, width=25),
                data_text(customer_last_rental_date, color=status_color, expand=True, text_align="left"),
            ], expand=Ratios.last_date, spacing=0),
            flet.VerticalDivider(width=1),
            flet.Row(expand=Ratios.status, controls=[
                flet.Text(
                    customer_status, text_align="center",
                    no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[7],
                    color=status_color, expand=3),
                flet.PopupMenuButton(
                    items=[
                        context_menu(customer_name, True, 20, weight=flet.FontWeight.BOLD,
                                     alignment=flet.alignment.center, icon=flet.Icons.PERSON),
                        flet.PopupMenuItem(height=1),
                        context_menu("Rentals Data", icon=flet.Icons.CALENDAR_MONTH,
                                     on_click=lambda e:context_customer_id_data(None, "rental", **customer_params)),
                        context_menu("Payments Data", icon=flet.Icons.ATTACH_MONEY,
                                     on_click=lambda e:context_customer_id_data(None, "payment", **customer_params)),
                        flet.PopupMenuItem(height=1),
                        context_menu("Edit", icon=flet.Icons.MODE_EDIT_OUTLINE,
                                     on_click=lambda e:context_customer_id_data(None, "edit", **customer_params)),
                        context_menu(content="Delete", color=flet.Colors.ERROR,
                                     icon=flet.Icons.DELETE_OUTLINED,
                                     on_click=lambda e:context_customer_id_data(None, "delete", **customer_params)),
                    ], expand=1, shadow_color=flet.Colors.GREY_100, icon=flet.Icons.MENU, icon_size=30,
                    padding=0
                )
            ],)
        ], alignment=flet.MainAxisAlignment.START, spacing=5, height=38
    ), margin=5, border_radius=5, expand=True)

def build_customer_ui(initial_value="", **kwargs):
    page = kwargs.get("page")
    conn = kwargs.get("conn")
    popup = Popup(page=page)
    customer_id_data = flet.ListView(expand=True, spacing=0)
    def query_customer(e, initial_value=None):
        input_data = None
        cart_customer_id = [] # ID 상자
        try:
            cart_customer_id.append(int(input_customer.value)) # ANY(%s) 조회를 위해 상자 보관
            # cart_customer_id = int(input_customer.value) -> ID 상자를 만들지 않는 경우 사용가능 | ANY(%s) -> ERROR
            # print(f"Search Customer ID : {int(input_customer.value)}")
        except:
            if initial_value:
                customer_name = f"%{initial_value}%"
                input_data = initial_value
            else:
                customer_name = f"%{input_customer.value.strip()}%"
                input_data = input_customer.value
            # print("Not ID -> Name Search")
            cursor = conn.cursor()
            try:
                cursor.execute(Search.customer_name_query,(customer_name,))
                customer_name_id = cursor.fetchall()
                if customer_name_id:
                    # print(f"Name Check : {input_customer.value}")
                    for row in customer_name_id: # 검색어에 해당하는 ID 값들을 상자에 보관하기 위한 반복
                        cart_customer_id.append(row[0]) # .append로 상자에 보관
                    # print(f"List Check : {cart_customer_id}")
                else:
                    if customer_id_data.page:
                        customer_id_data.update()
                        input_customer.focus()
                        print(f"Not Customer Name : {input_data}")
                        popup.show_error_open(
                            message=f"Customer Name Not Found [{input_data}]"
                        )
                    else:
                        customer_id_data.controls.clear()
                    return # 조회 실패시 쿼리 실행 방지
                conn.commit()
            except Exception as err:
                conn.rollback()
                print(f"Error. Customer Search : {err}")
                input_customer.focus()
                popup.show_error_open(
                    message="Error. Customer Search"
                )
                return # 조회 실패시 쿼리 실행 방지
        cursor = conn.cursor()
        try:
            cursor.execute(Search.customer_id_query,(cart_customer_id,))
            customer_data = cursor.fetchall()
            if customer_data:
                customer_id_data.controls.clear()
                for row in customer_data:
                    customer_id_data.controls.append(
                        view_table(row, input_data, **kwargs)
                    )
                if customer_id_data.page:
                    customer_id_data.update()
            else:
                print(f"Customer ID Not Found {input_customer.value}")
                input_customer.focus()
                popup.show_error_open(
                    message=f"Customer ID Not Found [{input_customer.value}]"
                )
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Customer error : {err}")

    input_customer = input_text(
        " Customer ID or Name ↵", value=initial_value, on_submit=query_customer, hint_text=" Press Enter to Search")

    view_customer = flet.Column(
        controls=[
            view_header(), customer_id_data
        ],
        expand=True, spacing=5
    )

    if initial_value:
        query_customer(None, initial_value)
        input_customer.autofocus = False

    return input_customer, view_customer