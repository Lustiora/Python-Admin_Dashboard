import flet
from math import ceil
from class_window import Font, Ratios
from class_query import Search

def today_status(query, view_page, status_name: str, status_query, status_color=None):
    return flet.Container(
        bgcolor=flet.Colors.GREY_200,
        on_click=lambda e:query(None, view_page),
        expand=1,
        padding=10,
        border_radius=10,
        height=80,
        ink=True,
        alignment=flet.alignment.center_left,
        border=flet.border.all(1, "flet.Colors.BLUE_GREY_50"),
        content=flet.Column([
            flet.Text(status_name, style=flet.TextThemeStyle.TITLE_MEDIUM, color=status_color),
            flet.Text(status_query, style=flet.TextThemeStyle.HEADLINE_SMALL, weight=flet.FontWeight.BOLD, color=status_color)
        ], spacing=1)
    )

def build_rental_ui(page, store_id, conn):
    rental_data = flet.ListView(expand=True, spacing=0)
    view_page = 0
    connect_module = []
    connect_module_count = []
    def select_view_page(select_page):
        try:
            if 0 in connect_module: # 검색 조회
                # print(f"Search load {select_page}")
                select_page = int(select_page)
                view_page = select_page * 10
                rental_search_data_query(None, view_page)
            if 1 in connect_module: # Total Rentals
                # print(f"Total load {select_page}")
                select_page = int(select_page)
                view_page = select_page * 10
                rental_search_total_query(None, view_page)
            if 2 in connect_module: # Overdue
                # print(f"Overdue load {select_page}")
                select_page = int(select_page)
                view_page = select_page * 10
                rental_search_overdue_query(None, view_page)
            if 3 in connect_module: # Due Today
                # print(f"Due Today load {select_page}")
                select_page = int(select_page)
                view_page = select_page * 10
                rental_search_due_today_query(None, view_page)
        except:
            print(f"Error select view page {connect_module}")
            return
    # Status
    def total_rental_query():
        cursor = conn.cursor()
        try:
            cursor.execute(Search.return_total_query, (store_id,))
            total_rental_data = cursor.fetchone()
            if total_rental_data:
                # print(f"Total Rentals: {total_rental_data[0]}")
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
                # print(f"Overdue: {overdue_data[0]}")
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
                # print(f"Due Today: {due_total_data[0]}")
                return due_total_data[0]
            else:
                print("조회 실패")
                return
        except:
            return

    def rental_search_total_query(e, view_page):
        def page_count():
            connect_module_count.clear()
            count_pages = []
            count = int(ceil(total_rental_query() / 10))
            for i in range(count):
                pages = str(i+1)
                count_pages.append(flet.Text(pages))
            if len(count_pages) == 1:
                count_pages.append(flet.Text())
            page_num.controls = count_pages
            if page_num.page:
                page_num.update()
        try:
            cursor = conn.cursor()
            cursor.execute(Search.return_search_total_query, (store_id, view_page))
            rental_id_data = cursor.fetchall()
            # print(rental_id_data)
            if rental_id_data:
                connect_module_count.clear()
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
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[0]), color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    ], expand=Ratios.id, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[1], color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    ], expand=Ratios.name, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[2], text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[7]),
                                        flet.Text(
                                            row[6], text_align="right", color=status_normal, expand=True,
                                            max_lines=1, tooltip=row[7]),
                                        flet.Container(width=5),
                                    ], expand=Ratios.title, alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[3]), text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[3])),
                                    ], expand=Ratios.date, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[4]), text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    ], expand=Ratios.date, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[5], text_align="left", color=status_color, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                    ], expand=Ratios.status, spacing=0),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True
                            # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                    connect_module_count.append(row[0])
                connect_module.clear()
                connect_module.append(1)
                page_count()
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

    def rental_search_overdue_query(e, view_page):
        def page_count():
            connect_module_count.clear()
            count_pages = []
            count = int(ceil(overdue_query() / 10))
            for i in range(count):
                pages = str(i+1)
                count_pages.append(flet.Text(pages))
            if len(count_pages) == 1:
                count_pages.append(flet.Text())
            page_num.controls = count_pages
            if page_num.page:
                page_num.update()
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_overdue_query, (store_id, view_page,))
            rental_id_data = cursor.fetchall()
            # print(rental_id_data)
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
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[0]), color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    ], expand=Ratios.id, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[1], color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    ], expand=Ratios.name, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[2], text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[7]),
                                        flet.Text(
                                            row[6], text_align="right", color=status_normal, expand=True,
                                            max_lines=1, tooltip=row[7]),
                                        flet.Container(width=5),
                                    ], expand=Ratios.title, alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[3]), text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[3])),
                                    ], expand=Ratios.date, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[4]), text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    ], expand=Ratios.date, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[5], text_align="left", color=status_color, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                    ], expand=Ratios.status, spacing=0),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True
                            # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                connect_module.clear()
                connect_module.append(2)
                page_count()
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

    def rental_search_due_today_query(e, view_page):
        def page_count():
            connect_module_count.clear()
            count_pages = []
            count = int(ceil(due_today_query() / 10))
            for i in range(count):
                pages = str(i+1)
                count_pages.append(flet.Text(pages))
            if len(count_pages) == 1:
                count_pages.append(flet.Text())
            page_num.controls = count_pages
            if page_num.page:
                page_num.update()
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_due_today_query, (store_id, view_page,))
            rental_id_data = cursor.fetchall()
            # print(rental_id_data)
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
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[0]), color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    ], expand=Ratios.id, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[1], color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    ], expand=Ratios.name, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[2], text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[7]),
                                        flet.Text(
                                            row[6], text_align="right", color=status_normal, expand=True,
                                            max_lines=1, tooltip=row[7]),
                                        flet.Container(width=5),
                                    ], expand=Ratios.title, alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[3]), text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[3])),
                                    ], expand=Ratios.date, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[4]), text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    ], expand=Ratios.date, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[5], text_align="left", color=status_color, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                    ], expand=Ratios.status, spacing=0),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True
                            # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                connect_module.clear()
                connect_module.append(3)
                page_count()
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

    total_rentals = today_status(
        query=rental_search_total_query,
        view_page=view_page,
        status_name="Total Rentals:",
        status_query=total_rental_query()
    )

    overdue = today_status(
        query=rental_search_overdue_query,
        view_page=view_page,
        status_name="Overdue:",
        status_query=overdue_query(),
        status_color=flet.Colors.ERROR
    )

    due_today = today_status(
        query=rental_search_due_today_query,
        view_page=view_page,
        status_name="Due Today:",
        status_query=due_today_query()
    )

    # Search
    def rental_search_data_query(e, view_page):
        cart_customer_id = []
        connect_count = []
        def close_pop(e):
            page.close(error_quit)
            input_rental.focus()
        error_quit = flet.AlertDialog(
            title=flet.Text("ERROR"),
            content=flet.Text(f"Rental ID or Customer Name Not Found [{input_rental.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop, autofocus=True)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        def page_count():
            count_pages = []
            count = int(ceil(int(connect_module_count[0]) / 10))
            for i in range(count):
                pages = str(i+1)
                count_pages.append(flet.Text(pages))
            page_num.controls = count_pages
            if page_num.page:
                page_num.update()
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
                    # print(f"List Check {cart_customer_id}")
                else:
                    error_quit.content.value = f"Customer Name Not Found [{input_rental.value}]"
                    page.open(error_quit)
                    return
            except:
                page.open(error_quit)
                return
        try:
            cursor = conn.cursor()
            if cart_customer_id:
                connect_module_count.clear()
                cursor.execute(Search.rental_search_count_query, (store_id, cart_customer_id,))
                connect_count.append(cursor.fetchone())
                for count in connect_count:
                    connect_module_count.append(int(count[0]))
        except:
            page.open(error_quit)
            return
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_id_query, (store_id, cart_customer_id, view_page,))
            rental_id_data = cursor.fetchall()
            # print(rental_id_data)
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
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[0]), color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[0])),
                                    ], expand=Ratios.id, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[1], color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[1]),
                                    ], expand=Ratios.name, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[2], text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[7]),
                                        flet.Text(
                                            row[6], text_align="right", color=status_normal, expand=True,
                                            max_lines=1, tooltip=row[7]),
                                        flet.Container(width=5),
                                    ], expand=Ratios.title, alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[3]), text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[3])),
                                    ], expand=Ratios.date, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            str(row[4]), text_align="left", color=status_normal, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[4])),
                                    ], expand=Ratios.date, spacing=0),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Row([
                                        flet.Container(width=5),
                                        flet.Text(
                                            row[5], text_align="left", color=status_color, expand=True,
                                            max_lines=1, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[5]),
                                    ], expand=Ratios.status, spacing=0),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True
                            # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                connect_module.clear()
                connect_module.append(0)
                page_count()
                if rental_data.page:
                    rental_data.update()
                input_rental.focus()
            else:
                error_quit.content.value = f"Rental ID Not Found [{int(input_rental.value)}]"
                print(f"Not Rental ID {int(input_rental.value)}")
                page.open(error_quit)
        except Exception as err:
            print(f"Search Rental error : {err}")

        # print(f"{count_num / 10} / {ceil(count_num / 10, 0) * 10}")

    input_rental = flet.TextField(
        hint_text=" Press Enter to Search", on_submit=lambda e:rental_search_data_query(None, view_page), label=" Rental ID or Customer Name ↵",
        text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=30, autofocus=True)

    # Filter
    # filter_rental = flet.Row(
    #     controls=[
    #         flet.Dropdown(
    #             label="Filter",
    #             value="name_asc",
    #             bgcolor=flet.Colors.PRIMARY_CONTAINER,
    #             on_change="",
    #             options=[
    #                 flet.DropdownOption(text="ID ▲", key="id_asc"),
    #                 flet.DropdownOption(text="ID ▼", key="id_desc"),
    #                 flet.DropdownOption(text="Name ▲", key="name_asc"),
    #                 flet.DropdownOption(text="Name ▼", key="name_desc"),
    #                 flet.DropdownOption(text="Rental Date ▲", key="rental_date_asc"),
    #                 flet.DropdownOption(text="Rental Date ▼", key="rental_date_desc"),
    #                 flet.DropdownOption(text="Due Date ▲", key="due_date_asc"),
    #                 flet.DropdownOption(text="Due Date ▼", key="due_date_desc"),
    #                 flet.DropdownOption(text="Over Due ▲", key="over_due_asc"),
    #                 flet.DropdownOption(text="Over Due ▼", key="over_due_desc"),
    #             ]
    #         )
    #     ]
    # )

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

    page_num = flet.CupertinoSlidingSegmentedButton(
        selected_index=0,
        thumb_color=flet.Colors.BLUE_400,
        on_change=lambda e: select_view_page(e.data),
        controls=[
            flet.Text("Min"),
            flet.Text("Max"),
        ],
    )

    page_row = flet.Container(
        height=40,
        content=flet.Row(
            height=40,
            controls=[
                flet.Row(
                    controls=[page_num],
                    expand=True,
                    scroll=flet.ScrollMode.AUTO,
                )
            ]
        )
    )

    view_rental = flet.Column(
        controls=[
            header, rental_data, page_row
        ],
        expand=True, spacing=5
    )

    rental_search_total_query(None, 0)

    return total_rentals, overdue, due_today, input_rental, view_rental