import flet, os, datetime, csv
from window_setting import Colors, Ratios
from full_query import Search
from window_popup import Popup
import material as mat

def view_header(case=None):
    if not case:
        return flet.Container(
            content=flet.Row(
                controls=[
                    mat.header_text("Film ID", expand=Ratios.id),
                    flet.VerticalDivider(width=1),
                    mat.header_text("Title", expand=Ratios.title),
                    flet.VerticalDivider(width=1),
                    mat.header_text("Last Rental Date", expand=Ratios.date),
                    flet.VerticalDivider(width=1),
                    mat.header_text("Rental / Inventory", expand=Ratios.store),
                ], alignment=flet.MainAxisAlignment.START, spacing=5, height=20
            ), margin=5
        )
    else:
        return flet.Container(
            content=flet.Row(
                controls=[
                    mat.header_text("ID", expand=Ratios.id),
                    flet.VerticalDivider(width=1),
                    mat.header_text("Title", expand=Ratios.title),
                    flet.VerticalDivider(width=1),
                    mat.header_text("Status", expand=Ratios.status),
                    flet.VerticalDivider(width=1),
                    mat.header_text("Last Rental Date", expand=Ratios.date),
                    flet.VerticalDivider(width=1),
                    mat.header_text("Rental Rate", expand=Ratios.rate),
                ], alignment=flet.MainAxisAlignment.START, spacing=5, height=20
            ), margin=5
        )

def export_csv(e, export_data):
    now = datetime.datetime.now()
    appdata = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(appdata):
        try:
            os.makedirs(appdata)
        except PermissionError:
            appdata = os.getcwd()
    file_path = os.path.join(appdata, f"inventory_data_{now.strftime('%Y-%m-%d')}_{now.strftime('%H%M%S')}.csv")

    column = ["Inventory ID", "Film Title", "Status", "Last Rental Date", "Rental Rate"]
    with open(file_path, "w", encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column)
        writer.writerows(export_data)
        print("Save Inventory Data")

def build_inventory_ui(**kwargs):
    page = kwargs.get("page")
    conn = kwargs.get("conn")
    staff_store_id = kwargs.get("staff_store_id")
    popup = Popup(page=page)
    inventory_id_data = flet.ListView(expand=True, spacing=0)
    def query_inventory(e, initial_value=None):
        cart_inventory_id = [] # ID 상자
        if not initial_value:
            if not input_inventory.value.strip():
                popup.show_popup_open(
                    message="Please enter your inventory id or film title or film tag."
                )
                input_inventory.focus()
                return
        try:
            cart_inventory_id.append(int(input_inventory.value)) # ANY(%s) 조회를 위해 상자 보관
            # print(f"Search Inventory ID : {int(input_inventory.value)}")
        except:
            cursor = conn.cursor()
            if initial_value:
                str_film_title_tag = initial_value
                # print(input_inventory.value.split())
            else:
                str_film_title_tag = f"{"&".join(input_inventory.value.split())}"
                # print(str_film_title_tag)
                # print("Not ID -> Title Search")
            try:
                if initial_value:
                    cursor.execute(Search.film_title_query, (staff_store_id, str_film_title_tag,))
                else:
                    cursor.execute(Search.film_title_tag_query,(staff_store_id, str_film_title_tag,))
                film_title = cursor.fetchall()
                if film_title:
                    # print(f"Title Check : {input_inventory.value}")
                    for row in film_title: # 검색어에 해당하는 ID 값들을 상자에 보관하기 위한 반복
                        cart_inventory_id.append(row[0]) # .append로 상자에 보관
                    # print(f"List Check : {cart_inventory_id}")
                else:
                    print(f"Not Film Title or Tag : {input_inventory.value.strip()}")
                    input_inventory.focus()
                    popup.show_popup_open(
                        message=f"Film Title or Tag Not Found [{input_inventory.value.strip()}]"
                    )
                    return # 조회 실패시 쿼리 실행 방지
                conn.commit()
            except Exception as err:
                conn.rollback()
                print(f"Error. Not Film Title or Tag {err}")
                input_inventory.focus()
                popup.show_popup_open(
                    message="Error. Not Film Title or Tag"
                )
                return # 조회 실패시 쿼리 실행 방지
        cursor = conn.cursor()
        try:
            cursor.execute(Search.inventory_id_query,(cart_inventory_id,))
            inventory_data = cursor.fetchall()
            # print(inventory_data)
            if inventory_data:
                inventory_id_data.controls.clear()
                for row in inventory_data:
                    status_color = Colors.status_normal
                    if row[2] == 'Checked out':
                        status_color = Colors.status_overdue
                    inventory_id_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    mat.data_text(str(row[0]), expand=Ratios.id),
                                    flet.VerticalDivider(width=1),
                                    flet.Row(
                                        [flet.Container(width=4),
                                        mat.data_text(row[1], expand=True, text_align="left")]
                                    , expand=Ratios.title, spacing=0),
                                    flet.VerticalDivider(width=1),
                                    mat.data_text(row[2], expand=Ratios.status, color=status_color),
                                    flet.VerticalDivider(width=1),
                                    mat.data_text(str(row[3]), expand=Ratios.date),
                                    flet.VerticalDivider(width=1),
                                    mat.data_text(str(row[4]), expand=Ratios.rate),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5, height=30
                            ), margin=5, border_radius=5, expand=True
                        )
                    )
                inventory_id_data.update()
                if view_inventory.page:
                    view_inventory.controls[0] = view_header(case=1)
                    view_inventory.update()
                if export_btn.page:
                    export_btn.disabled = False
                    export_btn.color = Colors.status_normal_btn_color
                    export_btn.border_color = Colors.status_normal_btn_color
                    export_btn.on_click = lambda e: export_csv(e, inventory_data)
                    export_btn.update()
            else:
                print(f"Inventory ID Not Found {input_inventory.value.strip()}")
                input_inventory.focus()
                popup.show_popup_open(
                    message=f"Inventory ID Not Found [{input_inventory.value.strip()}]"
                )
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Inventory error : {err}")

    def first_view_inventory(e):
        try:
            cursor = conn.cursor()
            cursor.execute(Search.first_view_query,(staff_store_id,))
            inventory_data = cursor.fetchall()
            if inventory_data:
                inventory_id_data.controls.clear()
                for row in inventory_data:
                    title = flet.Container(content=mat.data_text(content=row[1]))
                    inventory_id_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                alignment=flet.MainAxisAlignment.START,
                                spacing=5,
                                height=30,
                                controls=[
                                    mat.data_text(str(row[0]), expand=Ratios.id),
                                    flet.VerticalDivider(width=1),
                                    flet.TextButton(content=title, expand=Ratios.title, on_click=lambda e, r=row[1]:query_inventory(e, r)),
                                    flet.VerticalDivider(width=1),
                                    mat.data_text(str(row[2]), expand=Ratios.date),
                                    flet.VerticalDivider(width=1),
                                    mat.data_text(str(row[3]), expand=Ratios.store),
                                ],
                            ),
                        )
                    )
                if inventory_id_data.page:
                    inventory_id_data.update()
                conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"First View Inventory error : {err}")

    input_inventory = mat.input_text(
        " Inventory ID or Film Title or Tag ↵", on_submit=query_inventory, hint_text=" Press Enter to Search")

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

    view_inventory = flet.Column(
        controls=[
            view_header(None), inventory_id_data
        ],
        expand=True, spacing=5
    )

    first_view_inventory(None)


    return input_inventory, view_inventory, export_btn