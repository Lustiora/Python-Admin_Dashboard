# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import customtkinter
from tkinter import messagebox
from window import start_move, on_drag, Colors

# ---------------------------------------------------------
# Variable
# ---------------------------------------------------------
current_search_customer = None
current_search_inventory = None
current_search_film = None
current_search_rental = None
current_search_payment = None


# ---------------------------------------------------------
# Sub Frame (Search_Customer)
# ---------------------------------------------------------
def close_search_customer_frame(event=None):
    global current_search_customer
    current_search_customer.destroy()
    current_search_customer = None


def search_customer(main, conn, customer):
    global current_search_customer
    cursor = conn.cursor()
    cursor.execute("""
                   select c.customer_id,
                          c.first_name || ' ' || c.last_name as Name,
                          c.email,
                          r.rental_date,
                          f.title,
                          r.return_date
                   from customer c
                            inner join rental r
                                       on c.customer_id = r.customer_id
                            inner join inventory i
                                       on r.inventory_id = i.inventory_id
                            inner join film f
                                       on i.film_id = f.film_id
                   where c.customer_id = %s""", (customer,))
    customer_data = cursor.fetchone()
    if customer_data:
        # [변환] 결과 팝업창
        search_customer = customtkinter.CTkFrame(main, width=300, height=300,
                                                 fg_color=Colors.background,
                                                 border_width=2, border_color=Colors.primary)
        search_customer.place(x=30, y=30)
        current_customer = search_customer
    else:
        current_search_customer = None
        print("Customer ID not found.")
        messagebox.showerror("Error", "Customer ID not found")


def search_customer_frame(main):
    global current_search_customer
    if current_search_customer is not None:
        current_search_customer.lift()
        return
    # -- Frame --
    # [변환] 메인 프레임 (Raised 효과를 border로 대체)
    search_customer_frame = customtkinter.CTkFrame(main, width=300, height=300,
                                                   fg_color=Colors.background,
                                                   border_width=2, border_color=Colors.primary)
    search_customer_frame.place(x=30, y=30)
    current_search_customer = search_customer_frame

    # -- Title Bar --
    # [변환] corner_radius=0 으로 직각 처리
    title_bar = customtkinter.CTkFrame(current_search_customer, fg_color=Colors.primary, height=30, corner_radius=0)
    title_bar.pack(fill="x", side="top")

    # [변환] 타이틀 라벨
    title_label = customtkinter.CTkLabel(title_bar, text="Customer",
                                         fg_color=Colors.primary, text_color=Colors.title_text,
                                         font=("Arial", 14, "bold"))
    title_label.pack(side="left", padx=10)

    # -- Close --
    # [변환] 닫기 버튼 (Label 유지, hover 효과를 원하면 CTkButton 권장하지만 기존 로직 유지)
    close_btn = customtkinter.CTkLabel(title_bar, text=" X ",
                                       fg_color=Colors.alert, text_color="white",
                                       width=30)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_customer_frame)

    # -- Body --
    content_frame = customtkinter.CTkFrame(current_search_customer, fg_color=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # [변환] 내부 위젯들
    customtkinter.CTkLabel(content_frame, text="회원 번호 입력:",
                           fg_color=Colors.background, text_color=Colors.text).pack(pady=5)

    customtkinter.CTkEntry(content_frame).pack(pady=5)

    customtkinter.CTkButton(content_frame, text="검색",
                            fg_color=Colors.action, text_color="white",
                            hover_color=Colors.primary).pack(pady=5)

    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_search_customer.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_search_customer.lift(), add="+")

    title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_customer))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_customer))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_search_customer))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_customer))


# ---------------------------------------------------------
# Sub Frame (Search_Inventory)
# ---------------------------------------------------------
def close_search_inventory_frame(event=None):
    global current_search_inventory
    current_search_inventory.destroy()
    current_search_inventory = None


def search_inventory_frame(main):
    global current_search_inventory
    if current_search_inventory is not None:
        current_search_inventory.lift()
        return
    # -- Frame --
    search_inventory_frame = customtkinter.CTkFrame(main, width=300, height=300,
                                                    fg_color=Colors.background,
                                                    border_width=2, border_color=Colors.primary)
    search_inventory_frame.place(x=30, y=30)
    current_search_inventory = search_inventory_frame

    # -- Title Bar --
    title_bar = customtkinter.CTkFrame(current_search_inventory, fg_color=Colors.primary, height=30, corner_radius=0)
    title_bar.pack(fill="x", side="top")

    title_label = customtkinter.CTkLabel(title_bar, text="Inventory",
                                         fg_color=Colors.primary, text_color=Colors.title_text,
                                         font=("Arial", 14, "bold"))
    title_label.pack(side="left", padx=10)
    title_label.bind("<Button-1>", lambda e: current_search_inventory.lift())

    # -- Close --
    close_btn = customtkinter.CTkLabel(title_bar, text=" X ",
                                       fg_color=Colors.alert, text_color="white",
                                       width=30)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_inventory_frame)

    # -- Body --
    content_frame = customtkinter.CTkFrame(current_search_inventory, fg_color=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    customtkinter.CTkLabel(content_frame, text="재고 번호 입력:",
                           fg_color=Colors.background, text_color=Colors.text).pack(pady=5)

    customtkinter.CTkEntry(content_frame).pack(pady=5)

    customtkinter.CTkButton(content_frame, text="검색",
                            fg_color=Colors.action, text_color="white",
                            hover_color=Colors.primary).pack(pady=5)

    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_search_inventory.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_search_inventory.lift(), add="+")

    title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_inventory))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_inventory))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_search_inventory))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_inventory))


# ---------------------------------------------------------
# Sub Frame (Search_Film)
# ---------------------------------------------------------
def close_search_film_frame(event=None):
    global current_search_film
    current_search_film.destroy()
    current_search_film = None


def search_film_frame(main):
    global current_search_film
    if current_search_film is not None:
        current_search_film.lift()
        return
    # -- Frame --
    search_film_frame = customtkinter.CTkFrame(main, width=300, height=300,
                                               fg_color=Colors.background,
                                               border_width=2, border_color=Colors.primary)
    search_film_frame.place(x=30, y=30)
    current_search_film = search_film_frame

    # -- Title Bar --
    title_bar = customtkinter.CTkFrame(current_search_film, fg_color=Colors.primary, height=30, corner_radius=0)
    title_bar.pack(fill="x", side="top")

    title_label = customtkinter.CTkLabel(title_bar, text="Film",
                                         fg_color=Colors.primary, text_color=Colors.title_text,
                                         font=("Arial", 14, "bold"))
    title_label.pack(side="left", padx=10)
    title_label.bind("<Button-1>", lambda e: current_search_film.lift())

    # -- Close --
    close_btn = customtkinter.CTkLabel(title_bar, text=" X ",
                                       fg_color=Colors.alert, text_color="white",
                                       width=30)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_film_frame)

    # -- Body --
    content_frame = customtkinter.CTkFrame(current_search_film, fg_color=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    customtkinter.CTkLabel(content_frame, text="영화 번호 입력:",
                           fg_color=Colors.background, text_color=Colors.text).pack(pady=5)

    customtkinter.CTkEntry(content_frame).pack(pady=5)

    customtkinter.CTkButton(content_frame, text="검색",
                            fg_color=Colors.action, text_color="white",
                            hover_color=Colors.primary).pack(pady=5)

    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_search_film.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_search_film.lift(), add="+")

    title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_film))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_film))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_search_film))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_film))


# ---------------------------------------------------------
# Sub Frame (Search_Rental)
# ---------------------------------------------------------
def close_search_rental_frame(event=None):
    global current_search_rental
    current_search_rental.destroy()
    current_search_rental = None


def search_rental_frame(main):
    global current_search_rental
    if current_search_rental is not None:
        current_search_rental.lift()
        return
    # -- Frame --
    search_rental_frame = customtkinter.CTkFrame(main, width=300, height=300,
                                                 fg_color=Colors.background,
                                                 border_width=2, border_color=Colors.primary)
    search_rental_frame.place(x=30, y=30)
    current_search_rental = search_rental_frame

    # -- Title Bar --
    title_bar = customtkinter.CTkFrame(current_search_rental, fg_color=Colors.primary, height=30, corner_radius=0)
    title_bar.pack(fill="x", side="top")

    title_label = customtkinter.CTkLabel(title_bar, text="Rental",
                                         fg_color=Colors.primary, text_color=Colors.title_text,
                                         font=("Arial", 14, "bold"))
    title_label.pack(side="left", padx=10)
    title_label.bind("<Button-1>", lambda e: current_search_rental.lift())

    # -- Close --
    close_btn = customtkinter.CTkLabel(title_bar, text=" X ",
                                       fg_color=Colors.alert, text_color="white",
                                       width=30)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_rental_frame)

    # -- Body --
    content_frame = customtkinter.CTkFrame(current_search_rental, fg_color=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    customtkinter.CTkLabel(content_frame, text="대여 번호 입력:",
                           fg_color=Colors.background, text_color=Colors.text).pack(pady=5)

    customtkinter.CTkEntry(content_frame).pack(pady=5)

    customtkinter.CTkButton(content_frame, text="검색",
                            fg_color=Colors.action, text_color="white",
                            hover_color=Colors.primary).pack(pady=5)

    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_search_rental.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_search_rental.lift(), add="+")

    title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_rental))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_rental))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_search_rental))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_rental))


# ---------------------------------------------------------
# Sub Frame (Search_Payment)
# ---------------------------------------------------------
def close_search_payment_frame(event=None):
    global current_search_payment
    current_search_payment.destroy()
    current_search_payment = None


def search_payment_frame(main):
    global current_search_payment
    if current_search_payment is not None:
        current_search_payment.lift()
        return
    # -- Frame --
    search_payment_frame = customtkinter.CTkFrame(main, width=300, height=300,
                                                  fg_color=Colors.background,
                                                  border_width=2, border_color=Colors.primary)
    search_payment_frame.place(x=30, y=30)
    current_search_payment = search_payment_frame

    # -- Title Bar --
    title_bar = customtkinter.CTkFrame(current_search_payment, fg_color=Colors.primary, height=30, corner_radius=0)
    title_bar.pack(fill="x", side="top")

    title_label = customtkinter.CTkLabel(title_bar, text="Payment",
                                         fg_color=Colors.primary, text_color=Colors.title_text,
                                         font=("Arial", 14, "bold"))
    title_label.pack(side="left", padx=10)
    title_label.bind("<Button-1>", lambda e: current_search_payment.lift())

    # -- Close --
    close_btn = customtkinter.CTkLabel(title_bar, text=" X ",
                                       fg_color=Colors.alert, text_color="white",
                                       width=30)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_payment_frame)

    # -- Body --
    content_frame = customtkinter.CTkFrame(current_search_payment, fg_color=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    customtkinter.CTkLabel(content_frame, text="결제 번호 입력:",
                           fg_color=Colors.background, text_color=Colors.text).pack(pady=5)

    customtkinter.CTkEntry(content_frame).pack(pady=5)

    customtkinter.CTkButton(content_frame, text="검색",
                            fg_color=Colors.action, text_color="white",
                            hover_color=Colors.primary).pack(pady=5)

    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_search_payment.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_search_payment.lift(), add="+")

    title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_payment))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_payment))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_search_payment))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_payment))