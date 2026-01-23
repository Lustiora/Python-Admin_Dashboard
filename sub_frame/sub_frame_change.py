# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import tkinter
from window import start_move, on_drag
# ---------------------------------------------------------
# Variable
# ---------------------------------------------------------
current_change_customer = None
current_change_inventory = None
current_change_film = None
current_change_rental = None
current_change_payment = None
# ---------------------------------------------------------
# Sub Frame (change_Customer)
# ---------------------------------------------------------
def close_change_customer_frame(event=None):
    global current_change_customer
    current_change_customer.destroy()
    current_change_customer = None

def change_customer_frame(main):
    global current_change_customer
    if current_change_customer is not None:
        current_change_customer.lift()
        return
    # -- Frame --
    change_customer_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    change_customer_frame.place(x=30, y=30)
    current_change_customer = change_customer_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_change_customer, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Customer", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_change_customer_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_change_customer, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_change_customer.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_change_customer.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e:start_move(e, current_change_customer))
    title_bar.bind("<B1-Motion>", lambda e:on_drag(e, current_change_customer))
    title_label.bind("<Button-1>", lambda e:start_move(e, current_change_customer))
    title_label.bind("<B1-Motion>", lambda e:on_drag(e, current_change_customer))
# ---------------------------------------------------------
# Sub Frame (change_Inventory)
# ---------------------------------------------------------
def close_change_inventory_frame(event=None):
    global current_change_inventory
    current_change_inventory.destroy()
    current_change_inventory = None

def change_inventory_frame(main):
    global current_change_inventory
    if current_change_inventory is not None:
        current_change_inventory.lift()
        return
    # -- Frame --
    change_inventory_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    change_inventory_frame.place(x=30, y=30)
    current_change_inventory = change_inventory_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_change_inventory, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Inventory", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_change_inventory.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_change_inventory_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_change_inventory, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_change_inventory.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_change_inventory.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_change_inventory))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_change_inventory))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_change_inventory))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_change_inventory))
# ---------------------------------------------------------
# Sub Frame (change_Film)
# ---------------------------------------------------------
def close_change_film_frame(event=None):
    global current_change_film
    current_change_film.destroy()
    current_change_film = None

def change_film_frame(main):
    global current_change_film
    if current_change_film is not None:
        current_change_film.lift()
        return
    # -- Frame --
    change_film_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    change_film_frame.place(x=30, y=30)
    current_change_film = change_film_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_change_film, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Film", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_change_film.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_change_film_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_change_film, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_change_film.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_change_film.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_change_film))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_change_film))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_change_film))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_change_film))
# ---------------------------------------------------------
# Sub Frame (change_Rental)
# ---------------------------------------------------------
def close_change_rental_frame(event=None):
    global current_change_rental
    current_change_rental.destroy()
    current_change_rental = None

def change_rental_frame(main):
    global current_change_rental
    if current_change_rental is not None:
        current_change_rental.lift()
        return
    # -- Frame --
    change_rental_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    change_rental_frame.place(x=30, y=30)
    current_change_rental = change_rental_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_change_rental, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Rental", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_change_rental.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_change_rental_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_change_rental, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_change_rental.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_change_rental.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_change_rental))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_change_rental))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_change_rental))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_change_rental))
# ---------------------------------------------------------
# Sub Frame (change_Payment)
# ---------------------------------------------------------
def close_change_payment_frame(event=None):
    global current_change_payment
    current_change_payment.destroy()
    current_change_payment = None

def change_payment_frame(main):
    global current_change_payment
    if current_change_payment is not None:
        current_change_payment.lift()
        return
    # -- Frame --
    change_payment_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    change_payment_frame.place(x=30, y=30)
    current_change_payment = change_payment_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_change_payment, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Payment", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_change_payment.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_change_payment_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_change_payment, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_change_payment.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_change_payment.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_change_payment))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_change_payment))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_change_payment))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_change_payment))