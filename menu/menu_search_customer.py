import flet
from window import Font

def search_customer_id(page, conn):
    def customer_id_module(e):
        int_customer_id = int(customer_id_text.value)
        def close_pop(e):
            page.close(error_quit)  # 팝업창 종료 명령어
        error_quit = flet.AlertDialog(
            title=flet.Text("Customer"),
            content=flet.Text(f"Customer ID Not Found [{customer_id_text.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ select 
                        c.customer_id , 
                        c.create_date  , 
                        c.first_name , 
                        c.last_name , 
                        c.email ,
                        a.address
                    from customer c 
                    inner join address a 
                        on c.address_id = a.address_id
                    where c.activebool is true
                        and c.customer_id = %s""",(int_customer_id,)
            )
            customer_data = cursor.fetchone()
            if customer_data:
                customer_id_data.rows.clear()
                customer_id_data.rows.append(
                    flet.DataRow(cells=[
                        flet.DataCell(flet.Text(customer_data[0])),
                        flet.DataCell(flet.Text(customer_data[1])),
                        flet.DataCell(flet.Text(customer_data[2])),
                        flet.DataCell(flet.Text(customer_data[3])),
                        flet.DataCell(flet.Text(customer_data[4])),
                        flet.DataCell(flet.Text(customer_data[5])),
                    ])
                )
                customer_id_data.update()
            else:
                page.open(error_quit)
        except Exception as err:
            print(f"Search Customer error : {err}")
    customer_id_text = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10, autofocus=True)
    search_id = flet.Button(
        "Search", on_click=customer_id_module, width=80, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    customer_id_data = flet.DataTable(
        columns=[
            flet.DataColumn(flet.Text("ID", width=25)),
            flet.DataColumn(flet.Text("Create Date", width=74)),
            flet.DataColumn(flet.Text("First Name", width=80)),
            flet.DataColumn(flet.Text("Last Name", width=80)),
            flet.DataColumn(flet.Text("Email",width=235)),
            flet.DataColumn(flet.Text("Address",width=156)),
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
    customer_id = flet.Row(
        controls=[
            flet.Column([customer_id_data], scroll=flet.ScrollMode.ALWAYS)
        ],scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    return customer_id_text, search_id, customer_id

def search_customer_name(page, store_id, conn):
    def customer_name_module(e):
        customer_name_value = f"%{customer_name_text.value}%"
        def close_pop(e):
            page.close(error_quit)  # 팝업창 종료 명령어
        error_quit = flet.AlertDialog(
            title=flet.Text("Customer"),
            content=flet.Text(f"Customer Name Not Found [{customer_name_text.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ select
                        id ,
                        name ,
                        address ,
                        "zip code" ,
                        phone ,
                        city ,
                        country ,
                        notes
                    from customer_list
                    where name Ilike %s
                        and sid = %s
                    order by id , name """,(customer_name_value,store_id,)
            )
            customer_data = cursor.fetchall()
            if customer_data:
                customer_name_data.rows.clear()
                for sc_row in customer_data:
                    customer_name_data.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(sc_row[0])),
                            flet.DataCell(flet.Text(sc_row[1])),
                            flet.DataCell(flet.Text(sc_row[2])),
                            flet.DataCell(flet.Text(sc_row[3])),
                            flet.DataCell(flet.Text(sc_row[4])),
                            flet.DataCell(flet.Text(sc_row[5])),
                            flet.DataCell(flet.Text(sc_row[6])),
                            flet.DataCell(flet.Text(sc_row[7])),
                        ])
                    )
                customer_name_data.update()
            else:
                page.open(error_quit)
        except Exception as err:
            print(f"Search Customer error : {err}")
    customer_name_text = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10, autofocus=True)
    search_name = flet.Button("Search", on_click=customer_name_module, width=80, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    customer_name_data = flet.DataTable(
        columns=[
            flet.DataColumn(flet.Text("ID")),
            flet.DataColumn(flet.Text("Name")),
            flet.DataColumn(flet.Text("Address")),
            flet.DataColumn(flet.Text("Zip Code")),
            flet.DataColumn(flet.Text("Phone")),
            flet.DataColumn(flet.Text("City")),
            flet.DataColumn(flet.Text("Country")),
            flet.DataColumn(flet.Text("Notes")),
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
    customer_name = flet.Row(
        controls=[flet.Column([customer_name_data], scroll=flet.ScrollMode.ALWAYS)],
        scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    return customer_name_text, search_name, customer_name