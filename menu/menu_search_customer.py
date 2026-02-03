import flet
from window import Font, Ratios

def build_customer_ui(page, store_id, conn):
    customer_id_data = flet.ListView(expand=True, spacing=0)
    def query_customer(e):
        cart_customer_id = [] # ID 상자
        def close_pop(e):
            page.close(error_quit)
        error_quit = flet.AlertDialog(
            title=flet.Text("Customer"),
            content=flet.Text(f"Customer Name Not Found [{input_customer.value}]"),
            actions=[flet.TextButton("OK", on_click=close_pop, autofocus=True)
                     ], actions_alignment=flet.MainAxisAlignment.END)
        try:
            cart_customer_id.append(int(input_customer.value)) # ANY(%s) 조회를 위해 상자 보관
            # cart_customer_id = int(input_customer.value) -> ID 상자를 만들지 않는 경우 사용가능 | ANY(%s) -> ERROR
            print(f"Search Customer ID : {int(input_customer.value)}")
        except:
            str_customer_name = f"%{input_customer.value}%"
            print("Not ID -> Name Search")
            cursor = conn.cursor()
            try:
                cursor.execute( """ select customer_id
                                    from customer
                                    where first_name ilike %s 
                                        or last_name ilike %s """,(str_customer_name,str_customer_name,))
                customer_name_id = cursor.fetchall()
                if customer_name_id:
                    print(f"Name Check : {input_customer.value}")
                    for row in customer_name_id: # 검색어에 해당하는 ID 값들을 상자에 보관하기 위한 반복
                        cart_customer_id.append(row[0]) # .append로 상자에 보관
                    print(f"List Check : {cart_customer_id}")
                else:
                    print(f"Not Customer Name {input_customer.value}")
                    page.open(error_quit)
                    return # 조회 실패시 쿼리 실행 방지
            except:
                print(f"Error. Not Customer Name {input_customer.value}")
                page.open(error_quit)
                return # 조회 실패시 쿼리 실행 방지
        cursor = conn.cursor()
        try:
            cursor.execute(
                """ select
                        case when c.store_id = 1 then '🇨🇦 Lethbridge' else '🇦🇺 Woodridge' end as store ,
                        c.customer_id ,
                        c.first_name || ' ' || c.last_name as name,
                        c.email,
                        a.address,
                        c.create_date ,
                        case when n.customer_id is not null then 'Overdue' else 'Normal' end as status ,
                        c.store_id
                    from customer c
                    inner join address a
                        on c.address_id = a.address_id
                    left join not_return_customer n
                        on n.customer_id = c.customer_id
                    where c.activebool is true
                        and c.customer_id = ANY(%s) """,(cart_customer_id,)) # ANY(%s) : 상자에 담겨있는 ID들을 전부 비교
            customer_data = cursor.fetchall()
            if customer_data:
                customer_id_data.controls.clear()
                for row in customer_data:
                    status_color = flet.Colors.BLACK
                    store_color = flet.Colors.BLACK
                    if row[6] == 'Overdue':
                        status_color = flet.Colors.RED_ACCENT
                    if row[7] == store_id:
                        if row[0] == '🇦🇺 Woodridge':
                            store_color = flet.Colors.ORANGE
                        if row[0] == '🇨🇦 Lethbridge':
                            store_color = flet.Colors.BLUE
                    else:
                        store_color = flet.Colors.RED_ACCENT
                    customer_id_data.controls.append(
                        flet.Container(
                            content=flet.Row(
                                controls=[
                                    flet.Text(
                                        row[0], expand=Ratios.store, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[0], color=store_color),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[1]), expand=Ratios.id, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[1])),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[2], expand=Ratios.name, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[2]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[3], expand=Ratios.email, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[3]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[4], expand=Ratios.address, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[4]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        str(row[5])[:10], expand=Ratios.date, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=str(row[5])[:10]),
                                    flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                                    flet.Text(
                                        row[6], expand=Ratios.status, text_align="center",
                                        no_wrap=True, overflow=flet.TextOverflow.ELLIPSIS, tooltip=row[6], color=status_color),
                                ], alignment=flet.MainAxisAlignment.START, spacing=5
                            ), padding=10, border_radius=5, height=40, expand=True # height=40 -> VerticalDivider 사용을 위해 필요
                        )
                    )
                customer_id_data.update()
            else:
                print(f"Not Customer ID : {int(input_customer.value)}")
                page.open(error_quit)
        except Exception as err:
            print(f"Search Customer error : {err}")
    input_customer = flet.TextField(hint_text=" ID or Name",
        text_size=Font.big_fontsize, expand=Ratios.id, content_padding=10, max_length=20, autofocus=True)
    search_customer = flet.Button(
        "Search", on_click=query_customer, width=120, height=40,
        style=flet.ButtonStyle(shape=(flet.RoundedRectangleBorder(radius=5))))
    header = flet.Container(
        content = flet.Row(
            controls=[
                flet.Text("Store", expand=Ratios.store, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("ID", expand=Ratios.id, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Name", expand=Ratios.name, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Email", expand=Ratios.email, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Address", expand=Ratios.address, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Create Date", expand=Ratios.date, text_align="center"),
                flet.VerticalDivider(width=1, color=flet.Colors.PRIMARY),
                flet.Text("Status", expand=Ratios.status, text_align="center"),
            ], alignment=flet.MainAxisAlignment.START, spacing=5
        ), padding=10, border_radius=5, bgcolor=flet.Colors.PRIMARY_CONTAINER, height=40
    )
    view_customer = flet.Column(
        controls=[
            header, customer_id_data
        ],
        expand=True, spacing=5
    )
    return input_customer, search_customer, view_customer