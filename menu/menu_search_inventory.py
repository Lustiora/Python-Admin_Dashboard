import flet
from window import Font

def search_inventory_data(page, conn):
    def stock_id_module(e):
        int_inventory_id = int(inventory_id.value)
        def close_pop(e):
            page.close(error_quit)  # 팝업창 종료 명령어
        error_quit = flet.AlertDialog(
            title=flet.Text("Inventory"),
            content=flet.Text(f"Inventory ID Not Found [{inventory_id.value}]"),
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
                stock_id_data.rows.clear()
                stock_id_data.rows.append(
                    flet.DataRow(cells=[
                        flet.DataCell(flet.Text(inventory_data[0])),
                        flet.DataCell(flet.Text(inventory_data[1])),
                        flet.DataCell(flet.Text(inventory_data[2])),
                    ])
                )
                stock_id_data.update()
            else:
                page.open(error_quit)
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def stock_rental_module(e):
        int_inventory_id = int(inventory_id.value)
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
                stock_rental_data.rows.clear()
                for row in inventory_data:
                    stock_rental_data.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(row[0])),
                            flet.DataCell(flet.Text(row[1])),
                            flet.DataCell(flet.Text(row[2])),
                        ])
                    )
                stock_rental_data.update()
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def stock_title_module(e):
        int_inventory_id = int(inventory_id.value)
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
                stock_title_data.rows.clear()
                for row in inventory_data:
                    stock_title_data.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(row[0])),
                            flet.DataCell(flet.Text(row[1])),
                            flet.DataCell(flet.Text(row[2])),
                        ])
                    )
                stock_title_data.update()
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def iv_bu(e): # Double Event
        stock_id_module(e)
        stock_rental_module(e)
        stock_title_module(e)
    inventory_id = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10, autofocus=True)
    search = flet.Button(
        "Search", on_click=iv_bu, width=80, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    stock_id_data = flet.DataTable(
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
    stock_id = flet.Row(
        controls=[
            flet.Column([stock_id_data], scroll=flet.ScrollMode.ALWAYS)
        ],scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    stock_rental_data = flet.DataTable(
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
    stock_rental = flet.Row(
        controls=[
            flet.Column([stock_rental_data], scroll=flet.ScrollMode.ALWAYS)
        ], scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    stock_title_data = flet.DataTable(
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
    stock_title = flet.Row(
        controls=[
            flet.Column([stock_title_data], scroll=flet.ScrollMode.ALWAYS)
        ], scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    return inventory_id, search, stock_id, stock_rental, stock_title