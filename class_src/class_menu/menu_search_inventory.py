import flet
from class_window import Font, Ratios
from class_query import Search

def build_inventory_ui(page, store_id, conn):
    inventory_id_data = flet.ListView(expand=True, spacing=0)
    def query_inventory(e):
        cart_inventory_id = [] # ID 상자
        def close_pop(e):
            page.close(error_quit)
            input_inventory.focus()
        error_quit = flet.AlertDialog(
            title=flet.Text("Inventory"),
            content=flet.Text(f"Film Title Not Found [{input_inventory.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop, autofocus=True)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        try:
            cart_inventory_id.append(int(input_inventory.value)) # ANY(%s) 조회를 위해 상자 보관
            print(f"Search Inventory ID : {int(input_inventory.value)}")
        except:
            str_film_title = f"%{input_inventory.value}%"
            print("Not ID -> Title Search")
            cursor = conn.cursor()
            try:
                cursor.execute(Search.film_title_query,(str_film_title,))
                film_title = cursor.fetchall()
                if film_title:
                    print(f"Title Check : {input_inventory.value}")
                    for row in film_title: # 검색어에 해당하는 ID 값들을 상자에 보관하기 위한 반복
                        cart_inventory_id.append(row[0]) # .append로 상자에 보관
                    print(f"List Check : {cart_inventory_id}")
                else:
                    print(f"Not Film Title {input_inventory.value}")
                    page.open(error_quit)
                    return # 조회 실패시 쿼리 실행 방지
            except:
                print(f"Error. Not Film Title {input_inventory.value}")
                page.open(error_quit)
                return # 조회 실패시 쿼리 실행 방지
        cursor = conn.cursor()
        try:
            cursor.execute(Search.inventory_id_query,(cart_inventory_id,))
            inventory_data = cursor.fetchall()
            # print(inventory_data)
            if inventory_data:
                inventory_id_data.controls.clear()
                for row in inventory_data:
                    status_color = flet.Colors.BLACK
                    store_color = flet.Colors.BLACK
                    if row[3] == 'Checked out':
                        status_color = flet.Colors.RED_ACCENT
                    if row[6] == store_id:
                        if row[2] == '🇦🇺 Woodridge':
                            store_color = flet.Colors.ORANGE
                        if row[2] == '🇨🇦 Lethbridge':
                            store_color = flet.Colors.BLUE
                    else:
                        store_color = flet.Colors.RED_ACCENT
                    inventory_id_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    flet.Text(
                                        str(row[0]), expand=Ratios.id, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[1], expand=Ratios.name, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[2], expand=Ratios.store, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[2], color=store_color),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[3], expand=Ratios.status, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[3], color=status_color),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[4]), expand=Ratios.date, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[5]), expand=Ratios.rate, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[5])),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                inventory_id_data.update()
                input_inventory.focus()
            else:
                print(f"Not Inventory ID : {int(input_inventory.value)}")
                page.open(error_quit)
        except Exception as err:
            print(f"Search Inventory error : {err}")
    input_inventory = flet.TextField(label=" Inventory ID or Film Title ↵", on_submit=query_inventory, hint_text=" Press Enter to Search",
        text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=True)
    header = flet.Container(
        content = flet.Row(
            controls=[
                flet.Text("ID", expand=Ratios.id, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Title", expand=Ratios.name, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Store", expand=Ratios.store, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Status", expand=Ratios.status, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Last Rental Date", expand=Ratios.date, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Rental Rate", expand=Ratios.rate, text_align="center"),
            ], alignment=flet.MainAxisAlignment.START, spacing=5
        ), padding=10, border_radius=5, bgcolor=flet.Colors.PRIMARY_CONTAINER, height=40
    )
    view_inventory = flet.Column(
        controls=[
            header, inventory_id_data
        ],
        expand=True, spacing=5
    )
    return input_inventory, view_inventory