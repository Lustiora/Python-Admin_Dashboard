import flet
from math import ceil
from class_window import Font, Ratios
from class_query import Search
from class_popup import Popup

def today_status(query, view_page, status_name:str, status_query, status_color=None, select_page=None):
    return flet.Container(
        on_click=lambda e:query(None, view_page, select_page),
        expand=1,
        padding=10,
        border_radius=10,
        height=80,
        ink=True,
        alignment=flet.alignment.center_left,
        border=flet.border.all(color=flet.Colors.BLACK),
        content=flet.Column([
            flet.Text(status_name, style=flet.TextThemeStyle.TITLE_MEDIUM, color=status_color),
            flet.Text(status_query, style=flet.TextThemeStyle.HEADLINE_SMALL, weight=flet.FontWeight.BOLD, color=status_color)
        ], spacing=1)
    )

def status_page(conn, query, store_id):
    cursor = conn.cursor()
    try:
        cursor.execute(query, (store_id,))
        data = cursor.fetchone()
        if data:
            conn.commit()
            return data[0]
        else:
            print("Status Page Query Search Failed")
    except Exception as err:
        conn.rollback()
        print(f"Status Page Query Search Failed \n{err}")

def view_header():
    return flet.Container(
        content=flet.Row(
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
        ), padding=10, border_radius=5, height=40,
    )

def view_table(row, status_normal, status_color):
    return flet.Container(
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
    )

def view_table_rental_data(rental_data, rental_id_data, connect_module, connect_module_count, connect_module_page:int, query, page_num, select_page):
    # print(f"page_num.selected_index : {page_num.selected_index}")
    # print(f"connect_module_page : {connect_module_page}")
    # print(f"connect_module : {connect_module}")
    page_sync = [connect_module_page]
    # print(f"page_sync : {page_sync}")
    # print(f"select_page : {select_page}")
    if page_sync != connect_module:
        page_num.selected_index = 0
    if select_page is None:
        page_num.selected_index = 0
    count_pages = []
    count_pages.clear()
    page_num.visible = True
    if rental_id_data:
        connect_module_count.clear()
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
                view_table(row, status_normal, status_color)
            )
            connect_module_count.append(row[0])
        connect_module.clear()
        connect_module.append(connect_module_page)
        connect_module_count.clear()
        count = int(ceil(query / 10))
        for i in range(count):
            pages = str(i + 1)
            count_pages.append(flet.Text(pages))
        if len(count_pages) <= 1:
            page_num.visible = False
        else:
            page_num.controls = count_pages
        if page_num.page:
            page_num.update()
        if rental_data.page:
            rental_data.update()
    else:
        page_num.visible = False
        if page_num.page:
            page_num.update()
        if rental_data.page:
            rental_data.update()
        rental_data.controls.clear()
        rental_data.controls.append(
            flet.Container(content=flet.Row(controls=[flet.Text("Not Data"), ],
                                            alignment=flet.MainAxisAlignment.CENTER, )))
        rental_data.update()
    # print(f"count_pages : {count_pages}")

def build_rental_ui(page, store_id, conn):
    rental_data = flet.ListView(expand=True, spacing=0)
    view_page = 0
    connect_module = []
    connect_module_count = []

    def select_view_page(select_page):
        try:
            if 0 in connect_module: # 검색 조회
                # print(f"Search load {select_page}")
                view_page = int(select_page) * 10
                rental_search_data_query(None, view_page, select_page)
            if 1 in connect_module: # Total Rentals
                # print(f"Total load {select_page}")
                view_page = int(select_page) * 10
                rental_search_total_query(None, view_page, select_page)
            if 2 in connect_module: # Overdue
                # print(f"Overdue load {select_page}")
                view_page = int(select_page) * 10
                rental_search_overdue_query(None, view_page, select_page)
            if 3 in connect_module: # Due Today
                # print(f"Due Today load {select_page}")
                view_page = int(select_page) * 10
                rental_search_due_today_query(None, view_page, select_page)
        except:
            print(f"Error select view page {connect_module}")
            return

    # Status

    total_rental_data = status_page(conn, Search.return_total_query, store_id)
    overdue_data = status_page(conn, Search.return_overdue_query, store_id)
    due_today_data = status_page(conn, Search.return_due_today_query, store_id)

    def rental_search_total_query(e, view_page, select_page):
        connect_module_page = 1
        try:
            cursor = conn.cursor()
            cursor.execute(Search.return_search_total_query, (store_id, view_page))
            rental_id_data = cursor.fetchall()
            view_table_rental_data(rental_data, rental_id_data, connect_module, connect_module_count,
                                   connect_module_page, total_rental_data, page_num, select_page)
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Rental error : {err}")

    def rental_search_overdue_query(e, view_page, select_page):
        connect_module_page = 2
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_overdue_query, (store_id, view_page,))
            rental_id_data = cursor.fetchall()
            view_table_rental_data(rental_data, rental_id_data, connect_module, connect_module_count,
                                   connect_module_page, overdue_data, page_num, select_page)
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Rental error : {err}")

    def rental_search_due_today_query(e, view_page, select_page):
        connect_module_page = 3
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_due_today_query, (store_id, view_page,))
            rental_id_data = cursor.fetchall()
            view_table_rental_data(rental_data, rental_id_data, connect_module, connect_module_count,
                                   connect_module_page, due_today_data, page_num, select_page)
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Rental error : {err}")

    # Search
    def rental_search_data_query(e, view_page, select_page):
        popup = Popup(page=page)
        connect_module_page = 0
        cart_customer_id = []
        connect_count = []
        try:
            cart_customer_id.append(int(input_rental.value))
            # print(f"Search Rental ID {int(input_rental.value)}")
        except:
            customer_name = f"%{input_rental.value}%"
            # print(f"Search Customer Name {input_rental.value}")
            cursor = conn.cursor()
            try:
                cursor.execute(Search.rental_search_name_query, (store_id, customer_name))
                customer_name_list = cursor.fetchall()
                if customer_name_list:
                    for row in customer_name_list:
                        cart_customer_id.append(row[0])
                else:
                    print(f"Customer Name Not Found [{input_rental.value}]")
                    popup.show_error_open(
                        message=f"Customer Name Not Found [{input_rental.value}]"
                    )
                    return
                conn.commit()
            except Exception as err:
                conn.rollback()
                print(f"Error. Customer Name Search {err}")
        cursor = conn.cursor()
        if cart_customer_id:
            connect_module_count.clear()
            cursor.execute(Search.rental_search_count_query, (store_id, cart_customer_id,))
            connect_count.append(cursor.fetchone())
            for count in connect_count:
                connect_module_count.append(int(count[0]))
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_id_query, (store_id, cart_customer_id, view_page,))
            rental_id_data = cursor.fetchall()
            if not rental_id_data:
                print(f"Customer ID Not Found [{input_rental.value}]")
            view_table_rental_data(rental_data, rental_id_data, connect_module, connect_module_count,
                                   connect_module_page, connect_module_count[0], page_num, select_page)
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Rental error : {err}")

    total_rentals = today_status(
        query=rental_search_total_query,
        view_page=view_page,
        status_name="Total Rentals:",
        status_query=total_rental_data
    )

    overdue = today_status(
        query=rental_search_overdue_query,
        view_page=view_page,
        status_name="Overdue:",
        status_query=overdue_data,
        status_color=flet.Colors.ERROR
    )

    due_today = today_status(
        query=rental_search_due_today_query,
        view_page=view_page,
        status_name="Due Today:",
        status_query=due_today_data
    )

    input_rental = flet.TextField(
        hint_text=" Press Enter to Search", on_submit=lambda e:rental_search_data_query(None, view_page, 0),
        label=" Rental ID or Customer Name ↵", text_size=Font.big_fontsize, expand=Ratios.id,
        content_padding=10, max_length=30, autofocus=True
    )

    page_num = flet.CupertinoSlidingSegmentedButton(
        visible=True, # True = 표시, False = 숨김
        selected_index=0,
        on_change=lambda e: select_view_page(e.data),
        controls=[
            flet.Text("Min"),
            flet.Text("Max"),
    ])

    page_row = flet.Container(
        height=40,
        content=flet.Row(
            height=40,
            controls=[
                flet.Row(
                    controls=[page_num],
                    expand=True,
                    scroll=flet.ScrollMode.AUTO,
    )]))

    view_rental = flet.Column(
        expand=True,
        spacing=5,
        controls=[view_header(), rental_data, page_row]
    )

    rental_search_total_query(None, 0,0)

    return total_rentals, overdue, due_today, input_rental, view_rental