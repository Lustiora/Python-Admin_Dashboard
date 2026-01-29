import flet
from window import Font

def search_inventory_id(page, conn):
    def ivq_id(e):
        iv_id = int(inventory.value)
        def close_pop(e):
            page.close(error_quit)  # 팝업창 종료 명령어
        error_quit = flet.AlertDialog(
            title=flet.Text("Inventory"),
            content=flet.Text(f"Inventory ID Not Found [{inventory.value}]"),
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
                    where i.inventory_id = %s """,(iv_id,)
            )
            inventory_data = cursor.fetchone()
            if inventory_data:
                si_id.rows.clear()
                si_id.rows.append(
                    flet.DataRow(cells=[
                        flet.DataCell(flet.Text(inventory_data[0])),
                        flet.DataCell(flet.Text(inventory_data[1])),
                        flet.DataCell(flet.Text(inventory_data[2])),
                    ])
                )
                si_id.update()
            else:
                page.open(error_quit)
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def ivq_rt(e):
        iv_rt = int(inventory.value)
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
                    order by r.rental_date desc , r.return_date desc """,(iv_rt,)
            )
            inventory_data = cursor.fetchall()
            if inventory_data:
                si_rt.rows.clear()
                for row in inventory_data:
                    si_rt.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(row[0])),
                            flet.DataCell(flet.Text(row[1])),
                            flet.DataCell(flet.Text(row[2])),
                        ])
                    )
                si_rt.update()
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def ivq_ti(e):
        iv_ti = int(inventory.value)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ with search_iv_title_1 as (
                        select f.film_id
                        from inventory i 
                        inner join film f 
                            on i.film_id = f.film_id
                        where i.inventory_id = %s
                    ), search_iv_title_2 as (
                        select 
                            row_number() over (partition by i.inventory_id order by r.rental_date desc) as row ,
                            i.inventory_id , 
                            f.title ,
                            r.rental_date ,
                            r.return_date 
                        from inventory i 
                        inner join search_iv_title_1 s 
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
                    from search_iv_title_2 
                    where row = 1 """,(iv_ti,)
            )
            inventory_data = cursor.fetchall()
            if inventory_data:
                si_ti.rows.clear()
                for row in inventory_data:
                    si_ti.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(row[0])),
                            flet.DataCell(flet.Text(row[1])),
                            flet.DataCell(flet.Text(row[2])),
                        ])
                    )
                si_ti.update()
        except Exception as err:
            print(f"Search Inventory error : {err}")
    def iv_bu(e): # Double Event
        ivq_id(e)
        ivq_rt(e)
        ivq_ti(e)
    inventory = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10, autofocus=True)
    search = flet.Button(
        "Search", on_click=iv_bu, width=80, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    si_id = flet.DataTable(
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
    s_i_id = flet.Row(
        controls=[
            flet.Column([si_id], scroll=flet.ScrollMode.ALWAYS)
        ],scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    si_rt = flet.DataTable(
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
    s_i_rt = flet.Row(
        controls=[
            flet.Column([si_rt], scroll=flet.ScrollMode.ALWAYS)
        ], scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    si_ti = flet.DataTable(
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
    s_i_ti = flet.Row(
        controls=[
            flet.Column([si_ti], scroll=flet.ScrollMode.ALWAYS)
        ], scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    return inventory, search, s_i_id, s_i_rt, s_i_ti