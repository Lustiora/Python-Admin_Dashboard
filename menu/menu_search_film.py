import flet
from window import Font

def build_film_ui(page, conn):
    def handle_search(e):
        film_title_value = f"%{input_film_title.value}%"
        def close_pop(e):
            page.close(error_quit)  # 팝업창 종료 명령어
        error_quit = flet.AlertDialog(
            title=flet.Text("Film"),
            content=flet.Text(f"Film Name Not Found [{input_film_title.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ select 
                        fid , 
                        title , 
                        description , 
                        category , 
                        price , 
                        length , 
                        rating , 
                        actors  
                    from film_list
                    where title Ilike %s or description ILike %s or actors ILike %s 
                    order by
                        fid , 
                        title """,(film_title_value,film_title_value,film_title_value,)
            )
            film_data = cursor.fetchall()
            if film_data:
                table_film_list.rows.clear()
                for row in film_data:
                    table_film_list.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(row[0])),
                            flet.DataCell(flet.Text(row[1])),
                            flet.DataCell(flet.Text(row[2])),
                            flet.DataCell(flet.Text(row[3])),
                            flet.DataCell(flet.Text(row[4])),
                            flet.DataCell(flet.Text(row[5])),
                            flet.DataCell(flet.Text(row[6])),
                            flet.DataCell(flet.Text(row[7])),
                        ])
                    )
                table_film_list.update()
            else:
                page.open(error_quit)
        except Exception as err:
            print(f"Search Film error : {err}")
    input_film_title = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10, autofocus=True)
    search_title = flet.Button("Search", on_click=handle_search, width=80, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    table_film_list = flet.DataTable(
        columns=[
            flet.DataColumn(flet.Text("ID")),
            flet.DataColumn(flet.Text("Title")),
            flet.DataColumn(flet.Text("Description")),
            flet.DataColumn(flet.Text("Category")),
            flet.DataColumn(flet.Text("Price")),
            flet.DataColumn(flet.Text("Length")),
            flet.DataColumn(flet.Text("Rating")),
            flet.DataColumn(flet.Text("Actors")),
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
    ui_film_list = flet.Row(
        controls=[flet.Column([table_film_list], scroll=flet.ScrollMode.ALWAYS)],
        scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    return input_film_title, search_title, ui_film_list