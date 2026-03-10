import flet
import time
from window_popup import Popup
from window_setting import Font, Colors
from full_query import Customer

class Code:
    allowed_extensions = ("com", "net", "org", "edu", "gov", "mil")

    error_none = flet.Text(color=flet.Colors.ERROR)
    error_event = flet.AnimatedSwitcher(
        content=error_none,
        duration=500,
        reverse_duration=100,
        switch_in_curve=flet.AnimationCurve.BOUNCE_OUT,
    )

    page_content_id = flet.TextField(label="Customer ID :", expand=True, content_padding=10, read_only=True,
                                     text_align="center", color=Colors.customer_id, border_color=Colors.border_color)
    page_content_first_name = flet.TextField(label="First Name :", expand=True, content_padding=10, max_length=50,
                                             autofocus=True, border_color=Colors.border_color)
    page_content_address = flet.TextField(label="Address :", expand=True, content_padding=10, max_length=255,
                                          border_color=Colors.border_color)
    page_content_email = flet.TextField(label="Email :", expand=True, content_padding=10, max_length=254,
                                        border_color=Colors.border_color)
    country_box = []
    country_list_filter = flet.Dropdown(
        label="Country :",
        alignment=flet.CrossAxisAlignment.START,
        expand=True,
        options=country_box,
        border_color=Colors.border_color,
        on_change=None,
    )

    active_switch = flet.Switch(expand=4, value=False, disabled=True, label="Active   ",
                                label_position="left", label_style=flet.TextStyle(weight="bold"))
    page_content_last_name = flet.TextField(label="Last Name :", expand=True, content_padding=10, max_length=50,
                                            border_color=Colors.border_color)
    page_content_postal_code = flet.TextField(label="Postal Code :", expand=True, content_padding=10, max_length=20,
                                              border_color=Colors.border_color)
    page_content_phone = flet.TextField(label="Phone Number :", expand=True, content_padding=10, max_length=20,
                                        border_color=Colors.border_color)

    city_ref = flet.Ref[flet.Dropdown]()

    city_box = []
    city_list_filter = flet.Dropdown(
        ref=city_ref,
        label="City :",
        alignment=flet.CrossAxisAlignment.START,
        expand=True,
        options=city_box,
        border_color=Colors.border_color
    )

    required_controls = [
        page_content_first_name,
        page_content_last_name,
        page_content_email,
        page_content_address,
        page_content_postal_code,
        page_content_phone,
    ]

    address_required = [
        country_list_filter,
        city_list_filter,
    ]

    page_content_left = flet.Column(
        expand=True,
        controls=[
            page_content_id,
            page_content_first_name,
            page_content_email,
            page_content_address,
            flet.Row(controls=[country_list_filter], expand=True),
        ]
    )

    page_content_right = flet.Column(
        expand=True,
        controls=[
            flet.Row(controls=[flet.Text(expand=1), active_switch], expand=True),
            page_content_last_name,
            page_content_phone,
            page_content_postal_code,
            flet.Row(controls=[city_list_filter], expand=True),
        ]
    )

    page_content = flet.Row(
        expand=True,
        spacing=10,
        vertical_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[page_content_left, flet.VerticalDivider(), page_content_right]
    )

def page_content_clear():
    Code.error_event.content = Code.error_none
    Code.page_content_first_name.value = None
    Code.page_content_last_name.value = None
    Code.page_content_email.value = None
    Code.active_switch.value = None
    Code.page_content_id.value = None
    Code.page_content_address.value = None
    Code.page_content_postal_code.value = None
    Code.page_content_phone.value = None
    Code.city_list_filter.value = None
    Code.country_list_filter.value = None
    Code.city_box.clear()
    Code.city_box.append(flet.DropdownOption(text="Please select a country", key=None, disabled=True), )
    if Code.city_list_filter.page:
        Code.city_list_filter.update()

def test(e):
    print(f"select city id: {e.control.value}")
    pass

def customer(setting:str, **kwargs):
    page = kwargs["page"]
    conn = kwargs["conn"]
    staff_store_id = kwargs["staff_store_id"]
    popup = Popup(page=page)

    def city_list(e):
        # print(f"select country id: {e.control.value}")
        Code.city_ref.current.key = str(time.time())
        select_country_id = e.control.value
        try:  # 등록된 도시 목록 리스트
            cursor = conn.cursor()
            cursor.execute(Customer.city_list_query,(select_country_id,))
            city_list = cursor.fetchall()
            Code.city_box.clear()
            Code.city_list_filter.on_change = test
            for row in city_list:
                city_row = f"{row[0]}"
                city_id_row = f"{row[1]}"
                city = city_row.replace('(\'', '').replace('\',)', '')
                city_id = city_id_row.replace('(\'', '').replace('\',)', '')
                Code.city_box.append(flet.DropdownOption(text=city, key=city_id), )
            if Code.city_list_filter.page:
                Code.city_list_filter.update()
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(err)

    try: # 등록된 국가 목록 리스트
        cursor = conn.cursor()
        cursor.execute(Customer.country_list_query)
        country_list = cursor.fetchall()
        for row in country_list:
            country_row = f"{row[0]}"
            country = country_row.replace('(\'','').replace('\',)','')
            country_id = f"{row[1]}"
            Code.country_box.append(flet.DropdownOption(text=country, key=country_id),)
        Code.country_list_filter.on_change = city_list
        if Code.country_list_filter.page:
            Code.country_list_filter.update()
        conn.commit()
    except Exception as err:
        conn.rollback()
        print(err)

    def customer_page_open(e, **customer_data):
        page_content_clear()
        if setting == "add":
            page.open(customer_page)
        elif setting == "edit":
            customer_page.content.height = 400 # id, active 상태 표시 공간 추가
            Code.page_content_id.value = customer_data["customer_id"]
            Code.page_content_first_name.value = customer_data["customer_first_name"]
            Code.page_content_email.value = customer_data["customer_email"]
            Code.page_content_address.value = customer_data["customer_address"]
            Code.country_list_filter.value = customer_data["customer_country_id"]

            Code.active_switch.value = customer_data["customer_state"]
            Code.page_content_last_name.value = customer_data["customer_last_name"]
            Code.page_content_phone.value = customer_data["customer_phone"]
            Code.page_content_postal_code.value = customer_data["customer_postal_code"]
            Code.city_list_filter.value = customer_data["customer_city_id"]
            page.open(customer_page)
        else:
            return

    def customer_page_close(e):
        page.close(customer_page)
        page_content_clear()

    def customer_page_save(e):
        def failed_event(text:str="Please enter a valid email address."):
            Code.error_event.content = flet.Text(text, color=flet.Colors.ERROR, expand=3, text_align="start")
            customer_page.content.offset = flet.Offset(-0.03, 0)
            page.update(customer_page)
            time.sleep(0.07)
            customer_page.content.offset = flet.Offset(0.03, 0)
            page.update(customer_page)
            time.sleep(0.07)
            customer_page.content.offset = flet.Offset(0, 0)
            page.update(customer_page)

        c_active = None
        c_id = None
        if setting == "edit":
            c_active = Code.active_switch.value
            c_id = Code.page_content_id.value

        # 입력값 공란 필터링
        empty_found = False
        for input_text in Code.required_controls:
            if not input_text.value or not input_text.value.strip():
                empty_found = True
        for input_text in Code.address_required:
            if not input_text.value:
                empty_found = True
        if not empty_found:
            c_first_name = Code.page_content_first_name.value.strip()
            c_last_name = Code.page_content_last_name.value.strip()
            c_email = Code.page_content_email.value.strip()
            c_address = Code.page_content_address.value.strip()
            c_postal_code = Code.page_content_postal_code.value.strip()
            c_phone = Code.page_content_phone.value.strip()
            c_city_id = Code.city_list_filter.value
            c_country_id = Code.country_list_filter.value
        else:
            failed_event("Please fill in all required fields.")
            return

        # char.isalpha() for char 이름 형식 오류 필터링
        name = f"{c_first_name}{c_last_name}"
        if not all(char.isalpha() for char in name):
            failed_event("Invalid name format.\nPlease enter letters only.")
            return

        # 이메일 주소 검증 필터링
        if "@" in c_email and "." in c_email:
            c_domain_check = c_email.split("@", 2)[1]
            if "." in c_domain_check:
                c_domain = c_domain_check.split(".", 1)[1]
            else:
                failed_event()
                return
        else:
            failed_event()
            return

        # 최상위 도메인(Code.allowed_extensions) 이외 필터링
        if not c_domain in Code.allowed_extensions:
            failed_event()
            return

        # =========================================================
        # 연락처 검증 필터링 (숫자 갯수, 하이픈 갯수)
        # =========================================================
        # len("".join(c for c in c_phone if c.isdigit())) == 10
        # >>>>
        # for c in c_phone => c 변수 저장
        # if c.isdigit() => 저장된 변수에서 숫자값만 허용
        # "".join() => 허용값 결합
        # len() => 문자열 갯수
        # =========================================================
        # .count("요기") => ("요기") 문자열 갯수
        # =========================================================
        if not (len("".join(c for c in c_phone if c.isdigit())) == 10 and c_phone.count("-") == 2):
            if staff_store_id == 1:  # CA
                # print(f"CA {staff_store_id}")
                failed_event("Invalid phone format. Please use:\nXXX-XXX-XXXX.")
            elif staff_store_id == 2:  # AU
                # print(f"AU {staff_store_id}")
                failed_event("Invalid phone format. Please use:\nXXXX-XXX-XXX or XX-XXXX-XXXX.")
            return

        # 우편번호 숫자 이외 필터링
        if not all(char.isdigit() for char in c_postal_code):
            failed_event("Invalid postal code.\nPlease enter numbers only.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(Customer.customer_address_check_query, (c_city_id, c_country_id))
            check = cursor.fetchone()
            check_row = f"{check}"
            country_city_check = check_row.replace('(', '').replace(',)', '')
        except Exception as save_error_1:
            conn.rollback()
            print(f"Address Check Error :\n{save_error_1}")
            return

        # 올바르지 않은 국가, 도시 매치 필터링
        if not country_city_check == "1":
            failed_event("City and country mismatch.\nPlease check your selection.")
            return

        customer = {
            "id": c_id,
            "first_name": c_first_name,
            "last_name": c_last_name,
            "email": c_email,
            "domain": c_domain,
            "phone": c_phone,
            "address": c_address,
            "postal_code": c_postal_code,
            "city_id": c_city_id,
            "country_id": c_country_id,
            "active": c_active,
        }

        cursor = conn.cursor()
        if setting == "add":
            try:
                cursor.execute(Customer.customer_insert_query, (
                    customer["address"], customer["city_id"], customer["postal_code"], customer["phone"],
                    staff_store_id, customer["first_name"], customer["last_name"], customer["email"]
                ))
                new_customer_id = cursor.fetchone()[0]
                page.close(customer_page)
                message = flet.Text(
                    spans=[
                        flet.TextSpan("Customer "),
                        flet.TextSpan(
                            f"{customer["first_name"]} {customer["last_name"]} (ID: {new_customer_id})",
                            style=flet.TextStyle(weight=flet.FontWeight.BOLD, color="teal")),
                        flet.TextSpan(" has been successfully saved."),
                    ]
                )
                popup.show_popup_open(
                    content=message, title="Save Success",
                    actions=[flet.Button("OK", on_click=popup.show_popup_close, autofocus=True)]
                )
            except Exception as save_error_2:
                conn.rollback()
                print(f"Save ERROR {save_error_2}")
                return
        elif setting == "edit":
            input_data = kwargs["input_data"]
            try:  # Customer Status Save
                cursor.execute(Customer.customer_edit_query, (
                    customer["first_name"], customer["last_name"], customer["email"], customer["active"],
                    customer["id"],
                    customer["address"], customer["postal_code"], customer["phone"], customer["city_id"],
                    customer["id"]
                ))
                conn.commit()
                page.close(customer_page)
                page_content_clear()
                message = flet.Text(
                    spans=[
                        flet.TextSpan("Customer "),
                        flet.TextSpan(
                            f"{edit_customer_name} (ID: {edit_customer_id})",
                            style=flet.TextStyle(weight=flet.FontWeight.BOLD, color="teal")),
                        flet.TextSpan(" has been successfully saved."),
                    ]
                )
                popup.show_popup_open(
                    content=message, title="Save Success",
                    actions=[flet.Button("OK", on_click=popup.show_popup_close, autofocus=True)]
                )
                my_manager = page.session.get("manager")
                if my_manager:
                    my_manager.update_main_page(index=2, customer_name=input_data)
            except Exception as save_error_2:
                conn.rollback()
                print(f"Save ERROR {save_error_2}")
                return

    header = None
    if setting == "add":
        header = flet.Text("Register New Customer", size=Font.big_fontsize, weight="bold")
        Code.page_content_left.controls[0] = flet.Row()
        Code.page_content_right.controls[0] = flet.Row()
    elif setting == "edit":
        header = flet.Text("Customer Customer", size=Font.big_fontsize, weight="bold")

    customer_page_actions = [
        Code.error_event,
        flet.Row([
            flet.Button("OK", on_click=customer_page_save),
            flet.Button("Cancel", on_click=customer_page_close),
        ], tight=True, height=40)
    ]

    customer_page = flet.AlertDialog(
        modal=True,
        actions_alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
        actions=customer_page_actions,
        content=flet.Column(
            width=400,
            height=360,
            offset=flet.Offset(0, 0),
            animate_offset=flet.Animation(600, flet.AnimationCurve.EASE_OUT_BACK),
            controls=[
                header,
                flet.Divider(),
                Code.page_content,
                flet.Divider(),
            ]
        )
    )

    try:
        if setting == "add":
            customer_page_open(None)
        elif setting == "edit":
            edit_customer_name = kwargs["customer_name"]
            edit_customer_id = kwargs["customer_id"]
            cursor = conn.cursor()
            cursor.execute(Customer.customer_status_query, (edit_customer_id, edit_customer_name,))
            customer_status = cursor.fetchone()
            customer_data = {
                "customer_id": customer_status[0],
                "customer_first_name": customer_status[1],
                "customer_last_name": customer_status[2],
                "customer_email": customer_status[3],
                "customer_phone": customer_status[4],
                "customer_address": customer_status[5],
                "customer_postal_code": customer_status[6],
                "customer_country": customer_status[7],
                "customer_country_id": customer_status[8],
                "customer_city": customer_status[9],
                "customer_city_id": customer_status[10],
                "customer_state": customer_status[11],
            }
            conn.commit()
            customer_page_open(None, **customer_data)
    except Exception as err:
        conn.rollback()
        popup.show_popup_open(
            message=f"Customer Setting Page Open Failed\n\n{err}",
            actions=[flet.Button("OK", on_click=popup.show_popup_close, autofocus=True)]
        )

def customer_delete(**kwargs):
    page = kwargs["page"]
    conn = kwargs["conn"]
    customer_id = kwargs["customer_id"]
    customer_name = kwargs["customer_name"]
    input_data = kwargs["input_data"]
    try:
        cursor = conn.cursor()
        cursor.execute(Customer.customer_delete_query,(customer_id,customer_name,))
        conn.commit()
        print(f"Customer Deleted Successfully. ID: {customer_id}, Name: {customer_name}")
        my_manager = page.session.get("manager")
        if my_manager:
            my_manager.update_main_page(index=2, customer_name=input_data)
    except Exception as err:
        print(err)
        conn.rollback()