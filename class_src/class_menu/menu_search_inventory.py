import flet
from class_window import Font, Ratios
from class_query import Search
from class_popup import Popup
from material import input_text, header_text, context_menu, data_text

def build_inventory_ui(page, store_id, conn):
    popup = Popup(page=page)
    inventory_id_data = flet.ListView(expand=True, spacing=0)
    def query_inventory(e):
        cart_inventory_id = [] # ID 상자
        try:
            cart_inventory_id.append(int(input_inventory.value)) # ANY(%s) 조회를 위해 상자 보관
            # print(f"Search Inventory ID : {int(input_inventory.value)}")
        except:
            str_film_title = f"%{input_inventory.value.strip()}%"
            # print("Not ID -> Title Search")
            cursor = conn.cursor()
            try:
                cursor.execute(Search.film_title_query,(str_film_title,))
                film_title = cursor.fetchall()
                if film_title:
                    # print(f"Title Check : {input_inventory.value}")
                    for row in film_title: # 검색어에 해당하는 ID 값들을 상자에 보관하기 위한 반복
                        cart_inventory_id.append(row[0]) # .append로 상자에 보관
                    # print(f"List Check : {cart_inventory_id}")
                else:
                    print(f"Not Film Title : {input_inventory.value.strip()}")
                    popup.show_error_open(
                        message=f"Film Title Not Found [{input_inventory.value.strip()}]"
                    )
                    input_inventory.focus()
                    return # 조회 실패시 쿼리 실행 방지
                conn.commit()
            except Exception as err:
                conn.rollback()
                print(f"Error. Not Film Title {err}")
                popup.show_error_open(
                    message="Error. Not Film Title"
                )
                input_inventory.focus()
                return # 조회 실패시 쿼리 실행 방지
        cursor = conn.cursor()
        try:
            cursor.execute(Search.inventory_id_query,(cart_inventory_id,))
            inventory_data = cursor.fetchall()
            # print(inventory_data)
            if inventory_data:
                inventory_id_data.controls.clear()
                for row in inventory_data:
                    status_color = Font.status_normal
                    store_color = Font.status_normal
                    if row[3] == 'Checked out':
                        status_color = Font.status_overdue
                    if row[6] == store_id:
                        if row[2] == '🇦🇺 Woodridge':
                            store_color = flet.Colors.ORANGE
                        if row[2] == '🇨🇦 Lethbridge':
                            store_color = flet.Colors.BLUE
                    else:
                        store_color = Font.status_overdue
                    inventory_id_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    data_text(str(row[0]), expand=Ratios.id),
                                    flet.VerticalDivider(width=1),
                                    data_text(row[1], expand=Ratios.name, text_align="left"),
                                    flet.VerticalDivider(width=1),
                                    data_text(row[2], expand=Ratios.store, color=store_color),
                                    flet.VerticalDivider(width=1),
                                    data_text(row[3], expand=Ratios.status, color=status_color),
                                    flet.VerticalDivider(width=1),
                                    data_text(str(row[4]), expand=Ratios.date),
                                    flet.VerticalDivider(width=1),
                                    data_text(str(row[5]), expand=Ratios.rate),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5, height=30
                            ), margin=5, border_radius=5, expand=True
                        )
                    )
                inventory_id_data.update()
            else:
                print(f"Inventory ID Not Found {input_inventory.value.strip()}")
                popup.show_error_open(
                    message=f"Inventory ID Not Found [{input_inventory.value.strip()}]"
                )
                input_inventory.focus()
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Inventory error : {err}")

    input_inventory = input_text(
        " Inventory ID or Film Title ↵", on_submit=query_inventory, hint_text=" Press Enter to Search")

    header = flet.Container(
        content = flet.Row(
            controls=[
                header_text("Inventory ID", expand=Ratios.id),
                flet.VerticalDivider(width=1),
                header_text("Title", expand=Ratios.name),
                flet.VerticalDivider(width=1),
                header_text("Store", expand=Ratios.store),
                flet.VerticalDivider(width=1),
                header_text("Status", expand=Ratios.status),
                flet.VerticalDivider(width=1),
                header_text("Last Rental Date", expand=Ratios.date),
                flet.VerticalDivider(width=1),
                header_text("Rental Rate", expand=Ratios.rate),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=20
        ), margin=5
    )
    view_inventory = flet.Column(
        controls=[
            header, inventory_id_data
        ],
        expand=True, spacing=5
    )
    return input_inventory, view_inventory