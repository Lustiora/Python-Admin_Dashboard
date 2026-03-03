import flet
from math import ceil
from class_window import Colors, Ratios
from class_query import Search, Rental
from class_popup import Popup
import material as mat

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
                mat.header_text("Rental ID", expand=Ratios.id),
                flet.VerticalDivider(width=1),
                mat.header_text("Name", expand=Ratios.name),
                flet.VerticalDivider(width=1),
                mat.header_text("Title", expand=Ratios.title),
                flet.VerticalDivider(width=1),
                mat.header_text("Rental Date", expand=Ratios.date),
                flet.VerticalDivider(width=1),
                mat.header_text("Due Date", expand=Ratios.date),
                flet.VerticalDivider(width=1),
                mat.header_text("Status", expand=Ratios.status),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=20
        ), margin=5, border_radius=5
    )

def view_table(page, conn, row, rental_history, history_container, connect_module_page, status_normal, btn_color, btn_bgcolor, btn_overlay):
    rental_id = str(row[0])
    customer_name = row[1]
    status_view = flet.Text(row[5], expand=True, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    return flet.Container(
        content=flet.Row(
            controls=[
                flet.Row([
                    flet.Container(width=4),
                    mat.data_text(rental_id, color=status_normal, expand=True),
                ], expand=Ratios.id, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    mat.data_text(customer_name, color=status_normal, expand=True, max_lines=1),
                ], expand=Ratios.name, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    flet.Column([
                        mat.data_text(row[2], color=status_normal, max_lines=1),
                        mat.data_text(row[6], color=status_normal, max_lines=1),
                    ],expand=True, spacing=0),
                    flet.Container(width=4),
                ], expand=Ratios.title, alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    mat.data_text(str(row[3]), color=status_normal, expand=True, max_lines=2, text_align="left"),
                ], expand=Ratios.date, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Row([
                    flet.Container(width=4),
                    mat.data_text(str(row[4]), color=status_normal, expand=True, max_lines=1),
                ], expand=Ratios.date, spacing=0),
                flet.VerticalDivider(width=1),
                flet.Button(content=status_view, expand=Ratios.status,
                            on_click=lambda e: view_open_history(None, page, conn, rental_history, history_container,
                                                                 connect_module_page, rental_id, customer_name),
                            color=btn_color, bgcolor=btn_bgcolor,
                            style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=5),
                                                   overlay_color=btn_overlay)),
            ], alignment=flet.MainAxisAlignment.START, spacing=5, height=38
        ), margin=5, border_radius=5, expand=True
    )

def view_table_rental_data(
        page, conn, rental_data, rental_id_data, connect_module, connect_module_count, connect_module_page:int,
        query, page_num, select_page, rental_history, history_container):
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
            # Overdue
            status_normal = Colors.status_overdue
            btn_color = Colors.status_overdue_btn_color
            btn_bgcolor = Colors.status_overdue_btn_bgcolor
            btn_overlay = Colors.status_overdue_btn_overlay
            if row[5] == 'Returned':
                status_normal = Colors.status_normal
                btn_color = Colors.status_normal_btn_color
                btn_bgcolor = Colors.status_normal_btn_bgcolor
                btn_overlay = Colors.status_normal_btn_overlay
            if row[5] == 'Unreturned':
                status_normal = Colors.status_unreturned
                btn_color = Colors.status_unreturned_btn_color
                btn_bgcolor = Colors.status_unreturned_btn_bgcolor
                btn_overlay = Colors.status_unreturned_btn_overlay
            rental_data.controls.append(
                view_table(page, conn, row, rental_history, history_container, connect_module_page, status_normal, btn_color, btn_bgcolor, btn_overlay)
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

def history(page, conn, connect_module_page=None, rental_id:int=None, customer_name=None):
    popup = Popup(page=page)
    rental_history_data = flet.ListView(expand=True, spacing=0)
    view_rental_id = flet.Text("ID", weight=flet.FontWeight.BOLD)
    view_rental_name = flet.Text("Name", weight=flet.FontWeight.BOLD, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    view_rental_date = flet.Text("Rental Date", weight=flet.FontWeight.BOLD, max_lines=1, overflow=flet.TextOverflow.ELLIPSIS)
    view_rental_due_date = flet.Text("Due Date")
    view_return_data = flet.Text("Return Date")

    tmdb_api_image = "https://image.tmdb.org/t/p/w200"

    return_btn_disabled = True # 잠김
    cancel_btn_disabled = True
    on_click_actions = None

    def reversed_rental_data(e):
        print("reversed_rental_data")
        rental_history_data.update()
        # try:
        #     cursor = conn.cursor()
        #     cursor.execute(Rental.payment_return_query,{'rid':rental_id})
        #     conn.commit()
        #     popup.show_popup_close(None)
        #     if rental_history_data.page:
        #         rental_history_data.update()
        #         print("update")
        # except Exception as err:
        #     print(err)
        #     return

    def rental_data_return(e):
        print("rental_data_return")
        try:
            cursor = conn.cursor()
            cursor.execute(Rental.payment_return_query, {'rid': rental_id})
            conn.commit()
            popup.show_popup_close(None)
            if rental_history_data.page:
                rental_history_data.update()
                print("update")
            my_manager = page.session.get("manager")
            if my_manager:
                my_manager.update_main_page(index=0, page_index=connect_module_page, rental_id=rental_id, customer_name=customer_name)
        except Exception as err:
            print(err)
            return

    cursor = conn.cursor()
    try:
        rental_history_data.controls.clear()
        cursor.execute(Search.rental_history_data_query,(rental_id,))
        data = cursor.fetchone()
        if data:
            def actions(event):
                return [flet.TextButton("OK", on_click=event),
                        flet.TextButton("Cancel", on_click=popup.show_popup_close)]
            view_rental_id.value = data[0]
            view_rental_name.value = data[1]
            view_rental_date.value = data[4]
            view_rental_due_date.value = str(data[5])
            if data[7] is not None:
                def cancel_actions(e):
                    popup.show_popup_open(
                        "Cancel this Return Data?\n\nNote: The transaction will also be reversed.",
                        title="Warning", actions=actions(reversed_rental_data)
                    )
                return_btn_disabled = True
                cancel_btn_disabled = False
                on_click_actions = cancel_actions
                view_return_data = flet.Text(data[6], color=Colors.status_returned)
            else:
                if data[6] == 'Unreturned':
                    def return_actions(e):
                        popup.show_popup_open(
                            "Proceed with the return?", title="Null", actions=actions(rental_data_return)
                        )
                    return_btn_disabled = False
                    cancel_btn_disabled = True
                    on_click_actions = return_actions
                    view_return_data = flet.Text(data[6], weight=flet.FontWeight.BOLD, color=Colors.status_unreturned)
                else: # Overdue
                    def overdue_return_actions(e):
                        message = flet.Text(
                            spans=[
                                flet.TextSpan("Status: "),
                                flet.TextSpan(f"{data[6]}\n", style=flet.TextStyle(
                                    weight=flet.FontWeight.BOLD, color="red")),
                                flet.TextSpan("Continue with return?"),
                            ]
                        )
                        popup.show_popup_open(
                            content=message, title="Null", actions=actions(rental_data_return))
                    return_btn_disabled = False
                    cancel_btn_disabled = True
                    on_click_actions = overdue_return_actions
                    view_return_data = flet.Text(data[6], weight=flet.FontWeight.BOLD, color=Colors.status_overdue)

        film_data = cursor.fetchall()
        if film_data:
            for row in film_data:
                rental_history_data.controls.append(
                    flet.Container(
                        expand=True,
                        padding=10,
                        content=flet.Column([
                            flet.Row([
                                flet.Image(src=f"{tmdb_api_image}{row[3]}",width=60, height=90),
                                flet.Text(row[2]),
                            ]),
                            flet.Divider(height=1),
                        ], spacing=20)
                    )
                )
        if rental_history_data.page:
            rental_history_data.update()
        conn.commit()
    except Exception as err:
        conn.rollback()
        print(f"Error : {err}")
    return flet.Column([
        flet.Row([flet.Text("Rental ID:"),view_rental_id,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Row([flet.Text("Customer:"),view_rental_name,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Divider(height=1),
        rental_history_data,
        flet.Divider(height=1),
        flet.Row([flet.Text("Rental Date:"),view_rental_date,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Row([flet.Text("Due Date:"),view_rental_due_date,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        flet.Row([flet.Text("Return Date:"),view_return_data,],
                 width=float('inf'), alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
        mat.details_btn("Return", disabled=return_btn_disabled, action=on_click_actions),
        mat.details_btn("Cancel", disabled=cancel_btn_disabled, action=on_click_actions),
    ], expand=True, width=250)

def view_open_history(e, page, conn, rental_history, history_container, connect_module_page, rental_id, customer_name):
    # print("open receipt")
    if not rental_id:
        return
    else:
        rental_history.visible = True
        history_container.content = history(page, conn, connect_module_page, rental_id, customer_name)
        if rental_history.page:
            rental_history.update()

def view_close_history(e, rental_history):
    # print("close receipt")
    rental_history.visible = False
    rental_history.update()

def build_rental_ui(index, initial_id, initial_value="", **kwargs):
    page = kwargs.get("page")
    store_id = kwargs.get("staff_store_id")
    conn = kwargs.get("conn")
    popup = Popup(page=page)
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
            view_table_rental_data(page, conn, rental_data, rental_id_data, connect_module, connect_module_count,
               connect_module_page, total_rental_data, page_num, select_page, rental_history, history_container)
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
            view_table_rental_data(page, conn, rental_data, rental_id_data, connect_module, connect_module_count,
               connect_module_page, overdue_data, page_num, select_page, rental_history, history_container)
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
            view_table_rental_data(page, conn, rental_data, rental_id_data, connect_module, connect_module_count,
               connect_module_page, due_today_data, page_num, select_page, rental_history, history_container)
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Rental error : {err}")

    # Search
    def rental_search_data_query(e, view_page, select_page, initial_value=None):
        connect_module_page = 0
        cart_rental_id = []
        connect_count = []
        try:
            cart_rental_id.append(int(input_rental.value))
            # print(f"Search Rental ID {int(input_rental.value)}")
        except:
            if initial_value:
                customer_name = f"%{initial_value}%"
                input_data = initial_value
            else:
                customer_name = f"%{input_rental.value.strip()}%"
                input_data = input_rental.value
                # print(f"Search Customer Name {input_rental.value}")
            cursor = conn.cursor()
            try:
                cursor.execute(Search.rental_search_name_query, (store_id, customer_name))
                customer_name_list = cursor.fetchall()
                if customer_name_list:
                    for row in customer_name_list:
                        cart_rental_id.append(row[0])
                else:
                    print(f"Customer not found or no Rental history at this location. : {input_data}")
                    popup.show_popup_open(
                        message=f"Customer not found or no Rental history at this location."
                    )
                    if not initial_value:
                        input_rental.focus()
                    return
                conn.commit()
            except Exception as err:
                conn.rollback()
                print(f"Error. Customer Name Search : {err}")
        cursor = conn.cursor()
        if cart_rental_id:
            connect_module_count.clear()
            cursor.execute(Search.rental_search_count_query, (store_id, cart_rental_id,))
            connect_count.append(cursor.fetchone())
            for count in connect_count:
                connect_module_count.append(int(count[0]))
        try:
            cursor = conn.cursor()
            cursor.execute(Search.rental_search_id_query, (store_id, cart_rental_id, view_page,))
            rental_id_data = cursor.fetchall()
            if not rental_id_data:
                print(f"Rental ID Not Found : {input_rental.value}")
                input_rental.focus()
                popup.show_popup_open(
                    message=f"Rental ID Not Found [{input_rental.value}]"
                )
            view_table_rental_data(page, conn, rental_data, rental_id_data, connect_module, connect_module_count,
               connect_module_page, connect_module_count[0], page_num, select_page, rental_history, history_container)
            conn.commit()
        except Exception as err:
            conn.rollback()
            print(f"Search Rental error {err}")

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

    input_rental = mat.input_text(
        " Rental ID or Customer Name ↵", value=initial_value,
        on_submit=lambda e:rental_search_data_query(None, view_page, 0),
        hint_text=" Press Enter to Search"
    )

    page_num = flet.CupertinoSlidingSegmentedButton(
        visible=False, # True = 표시, False = 숨김
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

    history_container = flet.Container(
        content=history(page, conn),
        expand=True,
        padding=10,
        border_radius=5,
        border=flet.border.all(color=flet.Colors.BLACK),
    )

    rental_history = flet.Row([
        flet.VerticalDivider(width=1),
        flet.Column(
            controls=[
                flet.Row([
                    flet.Container(
                        expand=3,
                        alignment=flet.alignment.center_left,
                        padding=flet.padding.only(left=10),
                        content=flet.Text("Rental Details", style=flet.TextThemeStyle.TITLE_LARGE,
                                          weight=flet.FontWeight.BOLD),
                    ), flet.Container(
                        expand=1,
                        alignment=flet.alignment.center_right,
                        content=flet.IconButton(
                            icon=flet.Icons.CLOSE_ROUNDED,
                            on_click=lambda e: view_close_history(None, rental_history)
                        ),
                    ),
                ], height=40, spacing=0,
                ), history_container
            ], width=250,
        )
    ], spacing=20, visible=False, )


    view_rental = flet.Column(
        expand=True,
        spacing=5,
        controls=[view_header(), rental_data, page_row]
    )

    if initial_value:
        if index == 0:
            if initial_id:
                rental_search_data_query(None, 0, 0, initial_value)
                if not rental_history.visible:
                    rental_history.visible = True
                history_container.content = history(page=page, conn=conn, rental_id=initial_id)
                if rental_history.page:
                    rental_history.update()
                input_rental.autofocus = False
        else:
            rental_search_data_query(None, 0, 0, initial_value)
            input_rental.autofocus = False
    else:
        if index:
            if index == 0:
                rental_search_data_query(None, 0, 0)
            elif index == 1:
                rental_search_total_query(None, 0, 0)
            elif index == 2:
                rental_search_overdue_query(None, 0, 0)
            elif index == 3:
                rental_search_due_today_query(None, 0, 0)
            if initial_id:
                if not rental_history.visible:
                    rental_history.visible = True
                history_container.content = history(page, conn, index, initial_id)
                if rental_history.page:
                    rental_history.update()
                input_rental.autofocus = False
        else:
            rental_search_total_query(None, 0,0)


    return total_rentals, overdue, due_today, input_rental, view_rental, rental_history