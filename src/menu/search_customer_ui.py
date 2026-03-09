import flet, os, datetime, csv
from window_setting import Colors, Ratios
from full_query import Search
from window_popup import Popup
import material as mat
import menu.context_menu as ctm

def view_header():
    return flet.Container(
        content=flet.Row(
            controls=[
                mat.header_text("ID", expand=Ratios.id),
                flet.VerticalDivider(width=1),
                mat.header_text("Name", expand=Ratios.name),
                flet.VerticalDivider(width=1),
                mat.header_text("Email", expand=Ratios.email),
                flet.VerticalDivider(width=1),
                mat.header_text("Phone", expand=Ratios.phone),
                flet.VerticalDivider(width=1),
                mat.header_text("Address", expand=Ratios.address),
                flet.VerticalDivider(width=1),
                mat.header_text("Last Rental Date", expand=Ratios.last_date),
                flet.VerticalDivider(width=1),
                mat.header_text("Status", expand=Ratios.status+1),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=20
        ), margin=5
    )

def view_table(row, input_data, **kwargs):
    page = kwargs.get("page")
    staff_store_id = kwargs.get("staff_store_id")
    conn = kwargs.get("conn")
    status_color = Colors.status_normal
    customer_id = str(row[0])
    customer_name = row[1]
    customer_email = row[2]
    customer_phone = row[3]
    customer_address = row[4]
    customer_last_rental_date = row[5]
    customer_status = row[6]

    customer_params = {
        "page": page,
        "customer_name": customer_name,
        "staff_store_id": staff_store_id,
        "customer_id": customer_id,
        "conn": conn,
        "input_data": input_data,
    }

    if customer_status == 'Overdue':
        status_color = Colors.status_overdue

    return flet.Container(
    content=flet.Row(
        controls=[
            mat.data_text(customer_id, color=status_color, expand=Ratios.id),
            flet.VerticalDivider(width=1),
            flet.Row([
                flet.Container(width=4),
                mat.data_text(customer_name, color=status_color, expand=True, text_align="left"),
            ], expand=Ratios.name, spacing=0),
            flet.VerticalDivider(width=1),
            mat.data_text(customer_email, color=status_color, expand=Ratios.email),
            flet.VerticalDivider(width=1),
            mat.data_text(customer_phone, color=status_color, expand=Ratios.phone),
            flet.VerticalDivider(width=1),
            mat.data_text(customer_address, color=status_color, expand=Ratios.address),
            flet.VerticalDivider(width=1),
            mat.data_text(customer_last_rental_date, color=status_color, expand=Ratios.last_date),
            flet.VerticalDivider(width=1),
            flet.Row(expand=Ratios.status+1, controls=[
                flet.Text(
                    customer_status, text_align="center",
                    no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[6],
                    color=status_color, expand=3),
                flet.PopupMenuButton(
                    items=[
                        ctm.context_menu(customer_name, True, 20, weight=flet.FontWeight.BOLD,
                                     alignment=flet.alignment.center, icon=flet.Icons.PERSON),
                        flet.PopupMenuItem(height=1),
                        ctm.context_menu("Rentals Data", icon=flet.Icons.CALENDAR_MONTH,
                                     on_click=lambda e:ctm.context_customer_id_data(None, "rental", **customer_params)),
                        ctm.context_menu("Payments Data", icon=flet.Icons.ATTACH_MONEY,
                                     on_click=lambda e:ctm.context_customer_id_data(None, "payment", **customer_params)),
                        flet.PopupMenuItem(height=1),
                        ctm.context_menu("Edit", icon=flet.Icons.MODE_EDIT_OUTLINE,
                                     on_click=lambda e:ctm.context_customer_id_data(None, "edit", **customer_params)),
                        ctm.context_menu(content="Delete", color=flet.Colors.ERROR,
                                     icon=flet.Icons.DELETE_OUTLINED,
                                     on_click=lambda e:ctm.context_customer_id_data(None, "delete", **customer_params)),
                    ], expand=1, shadow_color=flet.Colors.GREY_100, icon=flet.Icons.MENU, icon_size=30,
                    padding=0
                )
            ],)
        ], alignment=flet.MainAxisAlignment.START, spacing=5, height=38
    ), margin=5, border_radius=5, expand=True)

def export_csv(e, export_data):
    now = datetime.datetime.now()
    appdata = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(appdata):
        try:
            os.makedirs(appdata)
        except PermissionError:
            appdata = os.getcwd()
    file_path = os.path.join(appdata, f"customer_data_{now.strftime('%Y-%m-%d')}_{now.strftime('%H%M%S')}.csv")

    column = ["Customer ID", "Name", "Email", "Phone", "Address", "Last Rental Date", "Status"]
    with open(file_path, "w", encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column)
        writer.writerows(export_data)
        print("Save Customer Data")

def build_customer_ui(initial_value="", **kwargs):
    page = kwargs.get("page")
    conn = kwargs.get("conn")
    staff_store_id = kwargs.get("staff_store_id")
    popup = Popup(page=page)
    customer_id_data = flet.ListView(expand=True, spacing=0)
    def query_customer(e, initial_value=None):
        input_data = None
        cart_customer_id = [] # ID 상자
        if not input_customer.value.strip():
            popup.show_popup_open(
                message="Please enter your customer id or name."
            )
            input_customer.focus()
            return
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
                cursor.execute(Search.customer_name_query,(staff_store_id, customer_name,))
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
                        popup.show_popup_open(
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
                popup.show_popup_open(
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
                if export_btn.page:
                    export_btn.disabled = False
                    export_btn.color = Colors.status_normal_btn_color
                    export_btn.border_color = Colors.status_normal_btn_color
                    export_btn.on_click = lambda e: export_csv(e, customer_data)
                    export_btn.update()
            else:
                print(f"Customer ID Not Found {input_customer.value}")
                input_customer.focus()
                popup.show_popup_open(
                    message=f"Customer ID Not Found [{input_customer.value}]"
                )
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Customer error : {err}")

    input_customer = mat.input_text(
        " Customer ID or Name ↵", value=initial_value, on_submit=query_customer, hint_text=" Press Enter to Search")

    view_customer = flet.Column(
        controls=[
            view_header(), customer_id_data
        ],
        expand=True, spacing=5
    )

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

    if initial_value:
        query_customer(None, initial_value)
        input_customer.autofocus = False

    return input_customer, view_customer, export_btn