import flet
from window import Font, Ratios
from query import Search

def build_rental_ui(page, store_id, conn):
    rental_data = flet.ListView(expand=True, spacing=0)
    # Status
    def total_rental_query():
        cursor = conn.cursor()
        try:
            cursor.execute(Search.return_total_query, (store_id,))
            total_rental_data = cursor.fetchone()
            if total_rental_data:
                rental_search_total_query(None)
                print(f"Total Rentals: {total_rental_data[0]}")
                return total_rental_data[0]
            else:
                print("조회 실패")
                return
        except:
            return

    def overdue_query():
        cursor = conn.cursor()
        try:
            cursor.execute(Search.return_overdue_query, (store_id,))
            overdue_data = cursor.fetchone()
            if overdue_data:
                print(f"Overdue: {overdue_data[0]}")
                return overdue_data[0]
            else:
                print("조회 실패")
                return
        except:
            return

    def due_today_query():
        cursor = conn.cursor()
        try:
            cursor.execute(Search.return_due_today_query, (store_id,))
            due_total_data = cursor.fetchone()
            if due_total_data:
                print(f"Total Rentals: {due_total_data[0]}")
                return due_total_data[0]
            else:
                print("조회 실패")
                return
        except:
            return

    def rental_search_total_query(e):
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_total_query, (store_id,))
            rental_id_data = cursor.fetchall()
            print(rental_id_data)
            if rental_id_data:
                rental_data.controls.clear()
                for row in rental_id_data:
                    status_normal = Font.status_overdue
                    status_color = Font.status_overdue
                    if row[5] == 'Unreturned':
                        status_normal = Font.status_normal
                        status_color = Font.status_unreturned
                    rental_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    flet.Text(
                                        str(row[0]), expand=Ratios.id, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[1], expand=Ratios.name, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[2], expand=Ratios.email, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[2]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[3]), expand=Ratios.date, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[3])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[4]), expand=Ratios.date, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[5], expand=Ratios.status, text_align="center", color=status_color,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                if rental_data.page:
                    rental_data.update()
            else:
                rental_data.controls.clear()
                rental_data.controls.append(
                    flet.Container(content=flet.Row(controls=[flet.Text("Not Data"), ],
                                                    alignment=flet.MainAxisAlignment.CENTER, )))
                rental_data.update()
        except Exception as err:
            print(f"Search Rental error : {err}")

    def rental_search_overdue_query(e):
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_overdue_query, (store_id,))
            rental_id_data = cursor.fetchall()
            print(rental_id_data)
            if rental_id_data:
                rental_data.controls.clear()
                for row in rental_id_data:
                    status_normal = Font.status_overdue
                    status_color = Font.status_overdue
                    if row[5] == 'Unreturned':
                        status_normal = Font.status_normal
                        status_color = Font.status_unreturned
                    rental_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    flet.Text(
                                        str(row[0]), expand=Ratios.id, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[1], expand=Ratios.name, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[2], expand=Ratios.email, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[2]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[3]), expand=Ratios.date, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[3])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[4]), expand=Ratios.date, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[5], expand=Ratios.status, text_align="center", color=status_color,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                rental_data.update()
            else:
                rental_data.controls.clear()
                rental_data.controls.append(
                    flet.Container(content=flet.Row(controls=[flet.Text("Not Data"), ],
                                                    alignment=flet.MainAxisAlignment.CENTER, )))
                rental_data.update()
        except Exception as err:
            print(f"Search Rental error : {err}")

    def rental_search_due_today_query(e):
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_due_today_query, (store_id,))
            rental_id_data = cursor.fetchall()
            print(rental_id_data)
            if rental_id_data:
                rental_data.controls.clear()
                for row in rental_id_data:
                    status_normal = Font.status_overdue
                    status_color = Font.status_overdue
                    if row[5] == 'Unreturned':
                        status_normal = Font.status_normal
                        status_color = Font.status_unreturned
                    rental_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    flet.Text(
                                        str(row[0]), expand=Ratios.id, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[1], expand=Ratios.name, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[2], expand=Ratios.email, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[2]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[3]), expand=Ratios.date, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[3])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[4]), expand=Ratios.date, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[5], expand=Ratios.status, text_align="center", color=status_color,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                rental_data.update()
            else:
                rental_data.controls.clear()
                rental_data.controls.append(
                    flet.Container(content=flet.Row(controls=[flet.Text("Not Data"), ],
                                                    alignment=flet.MainAxisAlignment.CENTER, )))
                rental_data.update()
        except Exception as err:
            print(f"Search Rental error : {err}")

    total_rentals = flet.Container(
            bgcolor=flet.Colors.GREY_200,
            on_click=rental_search_total_query,
            expand=1,
            padding=10,
            border_radius=10,
            height=80,
            ink=True,
            alignment=flet.alignment.center_left,
            border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
            content=flet.Column([
                flet.Text("Total Rentals:", style=flet.TextThemeStyle.TITLE_MEDIUM),
                flet.Text(total_rental_query(), style=flet.TextThemeStyle.HEADLINE_SMALL, weight=flet.FontWeight.BOLD)
            ], spacing=1)
        )
    overdue = flet.Container(
        bgcolor=flet.Colors.GREY_200,
        on_click=rental_search_overdue_query,
        expand=1,
        padding=10,
        border_radius=10,
        height=80,
        ink=True,
        alignment=flet.alignment.center_left,
        border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
        content=flet.Column([
            flet.Text("Overdue:", style=flet.TextThemeStyle.TITLE_MEDIUM, color=flet.Colors.ERROR),
            flet.Text(overdue_query(), style=flet.TextThemeStyle.HEADLINE_SMALL, weight=flet.FontWeight.BOLD, color=flet.Colors.ERROR)
        ], spacing=1)
    )
    due_today = flet.Container(
        bgcolor=flet.Colors.GREY_200,
        on_click=rental_search_due_today_query,
        expand=1,
        padding=10,
        border_radius=10,
        height=80,
        ink=True,
        alignment=flet.alignment.center_left,
        border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
        content=flet.Column([
            flet.Text("Due Today:", style=flet.TextThemeStyle.TITLE_MEDIUM),
            flet.Text(due_today_query(), style=flet.TextThemeStyle.HEADLINE_SMALL, weight=flet.FontWeight.BOLD)
        ], spacing=1)
    )
    # Search
    def rental_search_data_query(e):
        cart_customer_id = []
        def close_pop(e):
            page.close(error_quit)
            input_rental.focus()
        error_quit = flet.AlertDialog(
            title=flet.Text("ERROR"),
            content=flet.Text(f"Rental ID or Customer Name Not Found [{input_rental.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop, autofocus=True)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        try:
            cart_customer_id.append(int(input_rental.value))
            print(f"Search Rental ID {int(input_rental.value)}")
        except:
            customer_name = f"%{input_rental.value}%"
            print(f"Search Customer Name {input_rental.value}")
            cursor = conn.cursor()
            try:
                cursor.execute(Search.rental_search_name_query, (store_id, customer_name))
                customer_name_list = cursor.fetchall()
                if customer_name_list:
                    for row in customer_name_list:
                        cart_customer_id.append(row[0])
                    print(f"List Check {cart_customer_id}")
                else:
                    error_quit.content.value = f"Customer Name Not Found [{input_rental.value}]"
                    page.open(error_quit)
                    return
            except:
                page.open(error_quit)
                return
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_id_query, (store_id, cart_customer_id))
            rental_id_data = cursor.fetchall()
            print(rental_id_data)
            if rental_id_data:
                rental_data.controls.clear()
                for row in rental_id_data:
                    status_normal = Font.status_overdue
                    status_color = Font.status_overdue
                    if row[5] == 'Returned':
                        status_normal = Font.status_normal
                        status_color = flet.Colors.GREEN
                    if row[5] == 'Unreturned':
                        status_normal = Font.status_normal
                        status_color = Font.status_unreturned
                    rental_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    flet.Text(
                                        str(row[0]), expand=Ratios.id, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[1], expand=Ratios.name, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[2], expand=Ratios.email, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[2]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[3]), expand=Ratios.date, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[3])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[4]), expand=Ratios.date, text_align="center", color=status_normal,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[5], expand=Ratios.status, text_align="center", color=status_color,
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                rental_data.update()
                input_rental.focus()
            else:
                error_quit.content.value = f"Rental ID Not Found [{int(input_rental.value)}]"
                print(f"Not Rental ID {int(input_rental.value)}")
                page.open(error_quit)
        except Exception as err:
            print(f"Search Rental error : {err}")
    input_rental = flet.TextField(
        hint_text=" Press Enter to Search", on_submit=rental_search_data_query, label=" Rental ID or Customer Name ↵",
        text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=True)

    # Filter
    # filter_rental = flet.Column(
    #     controls=[
    #         flet.Dropdown(
    #             label="Filter",
    #             bgcolor=flet.Colors.PRIMARY_CONTAINER,
    #             options=[
    #                 flet.DropdownOption("Total Rentals"),
    #                 flet.DropdownOption("Overdue"),
    #                 flet.DropdownOption("Due Today"),
    #             ]
    #         )
    #     ],alignment=flet.MainAxisAlignment.CENTER)

    header = flet.Container(
        content = flet.Row(
            controls=[
                flet.Text("ID", expand=Ratios.id, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Name", expand=Ratios.name, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Title", expand=Ratios.email, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Rental Date", expand=Ratios.date, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Due Date", expand=Ratios.date, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Status", expand=Ratios.status, text_align="center"),
            ], alignment=flet.MainAxisAlignment.START, spacing=5
        ), padding=10, border_radius=5, bgcolor=flet.Colors.PRIMARY_CONTAINER, height=40
    )
    view_rental = flet.Column(
        controls=[
            header, rental_data
        ],
        expand=True, spacing=5
    )
    return total_rentals, overdue, due_today, input_rental, view_rental