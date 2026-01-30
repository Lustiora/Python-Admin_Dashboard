import flet
from window import Font

def build_inventory_ui(page, conn):
    def query_basic_info(e):
        int_inventory_id = int(input_inventory_id.value)
        def close_pop(e):
            page.close(error_quit)  # 팝업창 종료 명령어
        error_quit = flet.AlertDialog(
            title=flet.Text("Inventory"),
            content=flet.Text(f"Inventory ID Not Found [{input_inventory_id.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ select 
                        i.inventory_id ,
                        f.title , 
                        f.description 
                    from inventory i
                    inner join film f 
                        on i.film_id = f.film_id
                    where i.inventory_id = %s """,(int_inventory_id,)
            )
            inventory_data = cursor.fetchone()
            if inventory_data:
                table_basic_info.rows.clear()
                table_basic_info.rows.append(
                    flet.DataRow(cells=[
                        flet.DataCell(flet.Text(inventory_data[0])),
                        flet.DataCell(flet.Text(inventory_data[1])),
                        flet.DataCell(flet.Text(inventory_data[2])),
                    ])
                )
                table_basic_info.update()
            else:
                page.open(error_quit)
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def query_rental_history(e):
        int_inventory_id = int(input_inventory_id.value)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ select 
                        r.rental_id , 
                        r.rental_date , 
                        r.return_date  
                    from inventory i
                    inner join rental r 
                        on i.inventory_id = r.inventory_id
                    where i.inventory_id = %s
                    order by r.rental_date desc , r.return_date desc """,(int_inventory_id,)
            )
            inventory_data = cursor.fetchall()
            if inventory_data:
                table_rental_history.rows.clear()
                for row in inventory_data:
                    table_rental_history.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(row[0])),
                            flet.DataCell(flet.Text(row[1])),
                            flet.DataCell(flet.Text(row[2])),
                        ])
                    )
                table_rental_history.update()
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def query_current_status(e):
        int_inventory_id = int(input_inventory_id.value)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ with search_int_inventory_idtle_1 as (
                        select f.film_id
                        from inventory i 
                        inner join film f 
                            on i.film_id = f.film_id
                        where i.inventory_id = %s
                    ), search_int_inventory_idtle_2 as (
                        select 
                            row_number() over (partition by i.inventory_id order by r.rental_date desc) as row ,
                            i.inventory_id , 
                            f.title ,
                            r.rental_date ,
                            r.return_date 
                        from inventory i 
                        inner join search_int_inventory_idtle_1 s 
                            on i.film_id = s.film_id
                        inner join film f 
                            on i.film_id = f.film_id 
                        left join rental r 
                            on i.inventory_id = r.inventory_id 
                    )
                    select 
                        inventory_id , 
                        title, 
                        case 
                            when rental_date is not null and return_date is null then 'Checked out'
                            else 'In stock' 
                        end as status
                    from search_int_inventory_idtle_2 
                    where row = 1 """,(int_inventory_id,)
            )
            inventory_data = cursor.fetchall()
            if inventory_data:
                table_current_status.rows.clear()
                for row in inventory_data:
                    table_current_status.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(row[0])),
                            flet.DataCell(flet.Text(row[1])),
                            flet.DataCell(flet.Text(row[2])),
                        ])
                    )
                table_current_status.update()
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def on_click_search(e): # Double Event
        query_basic_info(e)
        query_rental_history(e)
        query_current_status(e)
    input_inventory_id = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10, autofocus=True)
    btn_search = flet.Button(
        "Search", on_click=on_click_search, width=80, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    table_basic_info = flet.DataTable(
        columns=[
            flet.DataColumn(flet.Text("ID", width=60)),
            flet.DataColumn(flet.Text("Title", width=150)),
            flet.DataColumn(flet.Text("Description", width=608)),
        ],
        rows=[],
        border=flet.border.all(1, "flet.Colors.BLUE_GREY_100"), # DataTable Titlebar
        vertical_lines=flet.border.all(1, "flet.Colors.BLUE_GREY_100"), # DataTable Titlebar
        horizontal_lines=flet.border.all(1, "flet.Colors.BLUE_GREY_100"), # DataTable Titlebar
        heading_row_color=flet.Colors.GREY_300, # DataTable Titlebar Inside Color
        heading_row_height=Font.height, # DataTable Titlebar Height
        data_row_min_height=Font.height-2, # DataTable Data Min Height
        data_row_max_height=Font.height-2, # DataTable Data Max Height
    )
    ui_basic_info = flet.Row(
        controls=[
            flet.Column([table_basic_info], scroll=flet.ScrollMode.ALWAYS)
        ],scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    table_rental_history = flet.DataTable(
        columns=[
            flet.DataColumn(flet.Text("Rental ID", width=60)),
            flet.DataColumn(flet.Text("Rental Date", width=130)),
            flet.DataColumn(flet.Text("Return Date", width=120)),
        ],
        rows=[],
        border=flet.border.all(1, "flet.Colors.BLUE_GREY_100"),  # DataTable Titlebar
        vertical_lines=flet.border.all(1, "flet.Colors.BLUE_GREY_100"),  # DataTable Titlebar
        horizontal_lines=flet.border.all(1, "flet.Colors.BLUE_GREY_100"),  # DataTable Titlebar
        heading_row_color=flet.Colors.GREY_300,  # DataTable Titlebar Inside Color
        heading_row_height=Font.height,  # DataTable Titlebar Height
        data_row_min_height=Font.height - 2,  # DataTable Data Min Height
        data_row_max_height=Font.height - 2,  # DataTable Data Max Height
    )
    ui_rental_history = flet.Row(
        controls=[
            flet.Column([table_rental_history], scroll=flet.ScrollMode.ALWAYS)
        ], scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    table_current_status = flet.DataTable(
        columns=[
            flet.DataColumn(flet.Text("ID", width=60)),
            flet.DataColumn(flet.Text("Title", width=152)),
            flet.DataColumn(flet.Text("Status", width=100)),
        ],
        rows=[],
        border=flet.border.all(1, "flet.Colors.BLUE_GREY_100"),  # DataTable Titlebar
        vertical_lines=flet.border.all(1, "flet.Colors.BLUE_GREY_100"),  # DataTable Titlebar
        horizontal_lines=flet.border.all(1, "flet.Colors.BLUE_GREY_100"),  # DataTable Titlebar
        heading_row_color=flet.Colors.GREY_300,  # DataTable Titlebar Inside Color
        heading_row_height=Font.height,  # DataTable Titlebar Height
        data_row_min_height=Font.height - 2,  # DataTable Data Min Height
        data_row_max_height=Font.height - 2,  # DataTable Data Max Height
    )
    ui_current_status = flet.Row(
        controls=[
            flet.Column([table_current_status], scroll=flet.ScrollMode.ALWAYS)
        ], scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    return input_inventory_id, btn_search, ui_basic_info, ui_rental_history, ui_current_status