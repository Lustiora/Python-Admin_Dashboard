import flet
import time
from class_query import Edit
from class_popup import Popup
from class_window import Font, Colors

def customer_edit(**kwargs):
    page = kwargs["page"]
    customer_name = kwargs["customer_name"]
    customer_id = kwargs["customer_id"]
    conn = kwargs["conn"]
    input_data = kwargs["input_data"]
    popup = Popup(page=page)

    edit_header = flet.Text("Customer Edit",size=Font.big_fontsize, weight="bold")
    error_none = flet.Text(color=flet.Colors.ERROR)
    error_event = flet.AnimatedSwitcher(
        content=error_none,
        duration=500,
        reverse_duration=100,
        switch_in_curve=flet.AnimationCurve.BOUNCE_OUT,
    )

    edit_page_content_id = flet.TextField(label="Customer ID :", expand=True, content_padding=10, read_only=True,
                                          text_align="center", color=Colors.customer_id)
    edit_page_content_first_name = flet.TextField(label="First Name :", expand=True, content_padding=10, max_length=50,
                                                  autofocus=True)
    edit_page_content_address = flet.TextField(label="Address :", expand=True, content_padding=10, max_length=255)
    edit_page_content_email = flet.TextField(label="Email :", expand=True, content_padding=10, max_length=254)
    country_box = []
    country_list_filter = flet.Dropdown(
        label="Country :",
        alignment=flet.CrossAxisAlignment.START,
        expand=True,
        options=country_box
    )

    active_switch = flet.Switch(expand=4, value=False, disabled=True, label="Active   ",
                                label_position="left", label_style=flet.TextStyle(weight="bold"))
    edit_page_content_last_name = flet.TextField(label="Last Name :", expand=True, content_padding=10, max_length=50)
    edit_page_content_postal_code = flet.TextField(label="Postal Code :", expand=True, content_padding=10, max_length=20)
    edit_page_content_phone = flet.TextField(label="Phone Number :", expand=True, content_padding=10, max_length=20)
    city_box = []
    city_list_filter = flet.Dropdown(
        label="City :",
        alignment=flet.CrossAxisAlignment.START,
        expand=True,
        options=city_box
    )

    try:
        cursor = conn.cursor()

        cursor.execute(Edit.country_list_query)
        country_list = cursor.fetchall()
        for row in country_list:
            country_row = f"{row[0]}"
            country = country_row.replace('(\'','').replace('\',)','')
            country_box.append(flet.DropdownOption(text=country, key=country),)
        if country_list_filter.page:
            country_list_filter.update()

        cursor.execute(Edit.city_list_query)
        city_list = cursor.fetchall()
        for row in city_list:
            city_row = f"{row[0]}"
            city = city_row.replace('(\'','').replace('\',)','')
            city_box.append(flet.DropdownOption(text=city, key=city),)
        if city_list_filter.page:
            city_list_filter.update()

        conn.commit()
    except Exception as err:
        conn.rollback()
        print(err)

    edit_page_content = flet.Row(
        expand=True,
        spacing=10,
        vertical_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[
            flet.Column(
                expand=True,
                controls=[
                    edit_page_content_id,
                    edit_page_content_first_name,
                    edit_page_content_email,
                    edit_page_content_address,
                    flet.Row(controls=[country_list_filter], expand=True),
                ]
            ),flet.VerticalDivider(),
            flet.Column(
                expand=True,
                controls=[
                    flet.Row(controls=[flet.Text(expand=1), active_switch], expand=True),
                    edit_page_content_last_name,
                    edit_page_content_phone,
                    edit_page_content_postal_code,
                    flet.Row(controls=[city_list_filter], expand=True),
                ]
            ),
        ]
    )

    def edit_page_open(e, **customer_data):
        edit_page_content_id.value = customer_data["customer_id"]
        edit_page_content_first_name.value = customer_data["customer_first_name"]
        edit_page_content_email.value = customer_data["customer_email"]
        edit_page_content_address.value = customer_data["customer_address"]
        country_list_filter.value = customer_data["customer_country"]

        active_switch.value = customer_data["customer_state"]
        edit_page_content_last_name.value = customer_data["customer_last_name"]
        edit_page_content_phone.value = customer_data["customer_phone"]
        edit_page_content_postal_code.value = customer_data["customer_postal_code"]
        city_list_filter.value = customer_data["customer_city"]

        page.open(edit_page)

    def edit_page_close(e):
        page.close(edit_page)

    def edit_page_save(e):
        def failed_event(text:str):
            error_event.content = flet.Text(text, color=flet.Colors.ERROR, expand=3,text_align="right")
            edit_page.content.offset = flet.Offset(-0.03, 0)
            page.update(edit_page)
            time.sleep(0.07)
            edit_page.content.offset = flet.Offset(0.03, 0)
            page.update(edit_page)
            time.sleep(0.07)
            edit_page.content.offset = flet.Offset(0, 0)
            page.update(edit_page)

        c_first_name = edit_page_content_first_name.value.strip()
        c_last_name = edit_page_content_last_name.value.strip()
        c_email = edit_page_content_email.value.strip()
        c_active = active_switch.value
        c_id = edit_page_content_id.value
        c_address = edit_page_content_address.value.strip()
        c_postal_code = edit_page_content_postal_code.value.strip()
        c_phone = edit_page_content_phone.value.strip()
        c_city = city_list_filter.value.strip()
        # c_id
        c_country = country_list_filter.value.strip()

        customer = {
            "id": c_id,
            "first_name": c_first_name,
            "last_name": c_last_name,
            "email": c_email,
            "phone": c_phone,
            "address": c_address,
            "postal_code": c_postal_code,
            "city": c_city,
            "country": c_country,
            "active": c_active,
        }

        try:
            cursor = conn.cursor()
            try:
                cursor.execute(Edit.customer_address_check_query, (customer["city"], customer["country"]))
                check = cursor.fetchone()
                check_row = f"{check}"
                country_city_check = check_row.replace('(','').replace(',)','')
            except Exception as save_error_1:
                conn.rollback()
                print(f"Address Check Error :\n{save_error_1}")
                return
            if all(char.isdigit() or char == "-" for char in customer["phone"]):
                if all(char.isdigit() for char in customer["postal_code"]):
                    if country_city_check == "1":
                        # print("City and Country Match Clear")
                        try:  # Customer Status Save
                            cursor.execute(Edit.customer_edit_query, (
                                customer["first_name"], customer["last_name"], customer["email"], customer["active"],
                                customer["id"],
                                customer["address"], customer["postal_code"], customer["phone"], customer["city"],
                                customer["id"]
                            ))
                        except Exception as save_error_2:
                            conn.rollback()
                            print(f"Save ERROR {save_error_2}")
                            return
                        conn.commit()
                        page.close(edit_page)
                        message = flet.Text(
                            spans=[
                                flet.TextSpan("Customer "),
                                flet.TextSpan(
                                    f"{customer_name} (ID: {customer_id})",
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
                    else:
                        # print("City and country do not match.")
                        failed_event("City and country do not match.")
                        return
                else:
                    failed_event("Postal Code Numbers only.")
                    return
            else:
                failed_event("Phone Numbers and hyphens only.")
                return
        except Exception as err:
            conn.rollback()
            print(f"Failed to Edit Customer\n{err}")
            return

    edit_page = flet.AlertDialog(
        modal=True,
        actions_alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
        actions=[
            error_event,
            flet.Row([
                flet.Button("OK", on_click=edit_page_save),
                flet.Button("Cancel", on_click=edit_page_close),
            ], tight=True)
        ],
        content=flet.Column(
            width=400,
            height=400,
            offset=flet.Offset(0, 0),
            animate_offset=flet.Animation(600, flet.AnimationCurve.EASE_OUT_BACK),
            controls=[
                edit_header,
                flet.Divider(),
                edit_page_content,
                flet.Divider(),
            ]
        )
    )

    try:
        cursor = conn.cursor()
        cursor.execute(Edit.customer_status_query,(customer_id, customer_name,))
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
            "customer_city": customer_status[8],
            "customer_state": customer_status[9],
        }
        conn.commit()
        edit_page_open(None, **customer_data)
    except Exception as err:
        popup.show_popup_open(
            message=f"Edit Page Open Failed\n\n{err}",
            actions=[flet.Button("OK", on_click=popup.show_popup_close, autofocus=True)]
        )
