# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import tkinter
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

def search_customer_frame(main):
    global current_search_customer
    if current_search_customer is not None:
        current_search_customer.lift()
        return
    # -- Frame --
    search_customer_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    search_customer_frame.place(x=30, y=30)
    current_search_customer = search_customer_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_search_customer, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Customer", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_customer_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_search_customer, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_search_customer.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_search_customer.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e:start_move(e, current_search_customer))
    title_bar.bind("<B1-Motion>", lambda e:on_drag(e, current_search_customer))
    title_label.bind("<Button-1>", lambda e:start_move(e, current_search_customer))
    title_label.bind("<B1-Motion>", lambda e:on_drag(e, current_search_customer))
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
    search_inventory_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    search_inventory_frame.place(x=30, y=30)
    current_search_inventory = search_inventory_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_search_inventory, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Inventory", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_search_inventory.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_inventory_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_search_inventory, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
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
    search_film_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    search_film_frame.place(x=30, y=30)
    current_search_film = search_film_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_search_film, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Film", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_search_film.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_film_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_search_film, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
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
    search_rental_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    search_rental_frame.place(x=30, y=30)
    current_search_rental = search_rental_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_search_rental, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Rental", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_search_rental.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_rental_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_search_rental, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
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
    search_payment_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    search_payment_frame.place(x=30, y=30)
    current_search_payment = search_payment_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_search_payment, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Payment", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_search_payment.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_search_payment_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_search_payment, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_search_payment.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_search_payment.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_search_payment))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_search_payment))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_search_payment))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_search_payment))