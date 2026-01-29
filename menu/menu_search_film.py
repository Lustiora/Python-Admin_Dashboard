import flet
from window import Font

def search_film_title(page, conn):
    def sfq_title(e):
        film_title_value = f"%{film_title_text.value}%"
        def close_pop(e):
            page.close(error_quit)  # 팝업창 종료 명령어
        error_quit = flet.AlertDialog(
            title=flet.Text("Film"),
            content=flet.Text(f"Film Name Not Found [{film_title_text.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ select 
                        f.film_id ,
                        f.release_year ,
                        f.title ,
                        l."name" ,
                        f.rental_duration ,
                        f.rental_rate ,
                        f.replacement_cost ,
                        f.rating ,
                        f.description
                    from film f 
                    inner join "language" l 
                        on f.language_id = l.language_id
                    where f.title Ilike %s or f.description ILike %s
                    order by
                        f.film_id ,
                        f.release_year ,
                        f.title ,
                        f.description """,(film_title_value,film_title_value,)
            )
            film_data = cursor.fetchall()
            if film_data:
                film_title_data.rows.clear()
                for row in film_data:
                    film_title_data.rows.append(
                        flet.DataRow(cells=[
                            flet.DataCell(flet.Text(row[0])),
                            flet.DataCell(flet.Text(row[1])),
                            flet.DataCell(flet.Text(row[2])),
                            flet.DataCell(flet.Text(row[3])),
                            flet.DataCell(flet.Text(row[4])),
                            flet.DataCell(flet.Text(row[5])),
                            flet.DataCell(flet.Text(row[6])),
                            flet.DataCell(flet.Text(row[7])),
                            flet.DataCell(flet.Text(row[8])),
                        ])
                    )
                film_title_data.update()
            else:
                page.open(error_quit)
        except Exception as err:
            print(f"Search Film error : {err}")
    film_title_text = flet.TextField(text_size=Font.fontsize, width=150, height=30, content_padding=5, max_length=10, autofocus=True)
    search_title = flet.Button("Search", on_click=sfq_title, width=80, style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    film_title_data = flet.DataTable(
        columns=[
            flet.DataColumn(flet.Text("ID")),
            flet.DataColumn(flet.Text("Year")),
            flet.DataColumn(flet.Text("Title")),
            flet.DataColumn(flet.Text("Language")),
            flet.DataColumn(flet.Text("Rental Duration")),
            flet.DataColumn(flet.Text("Rental Rate")),
            flet.DataColumn(flet.Text("Replacement Cost")),
            flet.DataColumn(flet.Text("rating")),
            flet.DataColumn(flet.Text("Description")),
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
    film_title = flet.Row(
        controls=[flet.Column([film_title_data], scroll=flet.ScrollMode.ALWAYS)],
        scroll=flet.ScrollMode.AUTO,
        expand=True,
    )
    return film_title_text, search_title, film_title