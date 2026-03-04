import flet

from class_query import Edit
from class_popup import Popup
from class_window import Font, Colors

def customer_edit(**kwargs):
    page = kwargs["page"]
    customer_name = kwargs["customer_name"]
    customer_id = kwargs["customer_id"]
    conn = kwargs["conn"]
    popup = Popup(page=page)

    edit_page_content_id = flet.TextField(label="Customer ID :", expand=True, content_padding=10, read_only=True,
                                          text_align="center", color=Colors.customer_id)
    edit_page_content_first_name = flet.TextField(label="First Name :", expand=True, content_padding=10, max_length=50,
                                                  autofocus=True)
    edit_page_content_address = flet.TextField(label="Address :", expand=True, content_padding=10, max_length=255)
    edit_page_content_email = flet.TextField(label="Email :", expand=True, content_padding=10, max_length=254)
    edit_page_content_country = flet.TextField(label="Country :", expand=True, content_padding=10, max_length=100)

    active_switch = flet.Switch(expand=4, value=False, disabled=True, label="Active   ",
                                label_position="left", label_style=flet.TextStyle(weight="bold"))
    edit_page_content_last_name = flet.TextField(label="Last Name :", expand=True, content_padding=10, max_length=50)
    edit_page_content_postal_code = flet.TextField(label="Postal Code :", expand=True, content_padding=10, max_length=20)
    edit_page_content_phone = flet.TextField(label="Phone Number :", expand=True, content_padding=10, max_length=20)
    edit_page_content_city = flet.TextField(label="City :", expand=True, content_padding=10, max_length=100)

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
                    edit_page_content_address,
                    edit_page_content_email,
                    edit_page_content_country,
                ]
            ),flet.VerticalDivider(),
            flet.Column(
                expand=True,
                controls=[
                    flet.Row(controls=[flet.Text(expand=1), active_switch], expand=True),
                    edit_page_content_last_name,
                    edit_page_content_postal_code,
                    edit_page_content_phone,
                    edit_page_content_city
                ]
            ),
        ]
    )

    def edit_page_open(e, **customer_data):
        edit_page_content_id.value = customer_data["customer_id"]
        edit_page_content_first_name.value = customer_data["customer_first_name"]
        edit_page_content_address.value = customer_data["customer_address"]
        edit_page_content_email.value = customer_data["customer_email"]
        edit_page_content_country.value = customer_data["customer_country"]

        active_switch.value = customer_data["customer_state"]
        edit_page_content_last_name.value = customer_data["customer_last_name"]
        edit_page_content_postal_code.value = customer_data["customer_postal_code"]
        edit_page_content_phone.value = customer_data["customer_phone"]
        edit_page_content_city.value = customer_data["customer_city"]

        page.open(edit_page)

    def edit_page_close(e):
        page.close(edit_page)

    def edit_page_save(e):
        c_firstname = edit_page_content_first_name.value.strip()
        c_last_name = edit_page_content_last_name.value.strip()
        c_email = edit_page_content_email.value.strip()
        c_active = active_switch.value
        c_id = edit_page_content_id.value.strip()
        c_address = edit_page_content_address.value.strip()
        c_postal_code = edit_page_content_postal_code.value.strip()
        c_phone = edit_page_content_phone.value.strip()
        c_city = edit_page_content_city.value.strip()
        # c_id
        c_country = edit_page_content_country.value.strip()
        try:
            cursor = conn.cursor()
            try: # 고객 이름, 이메일, 활성상태
                cursor.execute(Edit.customer_edit_query_1,(c_firstname,c_last_name,c_email,c_active,c_id))
                print("Save 1")
            except Exception as err_1:
                conn.rollback()
                print(f"ERROR 1 {err_1}")
                return
            try: # 고객 주소, 우편번호, 연락처, 도시
                cursor.execute(Edit.customer_edit_query_2,(c_address,c_postal_code,c_phone,c_city,c_id))
                print("Save 2")
            except Exception as err_2:
                print(f"ERROR 2 {err_2}")
                try:
                    cursor.execute(Edit.customer_edit_query_3,(c_city,c_country))
                except Exception as err_3:
                    print(f"ERROR 3 {err_3}")
                    conn.rollback()
                    return
            conn.commit()
            popup.show_popup_open(
                message=f"Save Success {customer_id}:{customer_name}",
                actions=[flet.Button("OK", on_click=popup.show_popup_close, autofocus=True)]
            )
        except Exception as err:
            conn.rollback()
            popup.show_popup_open(
                message=f"Save Failed\n\n{err}",
                actions=[flet.Button("OK", on_click=popup.show_popup_close, autofocus=True)]
            )
        page.close(edit_page)

    edit_page = flet.AlertDialog(
        modal=True,
        actions=[
            flet.Button("OK", on_click=edit_page_save),
            flet.Button("Cancel", on_click=edit_page_close),
        ],
        content=flet.Column(
            width=400,
            height=400,
            controls=[
                flet.Text("Customer Edit",size=Font.big_fontsize, weight="bold"),
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
