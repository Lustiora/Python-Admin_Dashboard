# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import tkinter
from window import start_move, on_drag, Colors
# ---------------------------------------------------------
# Variable
# ---------------------------------------------------------
current_delete_customer = None
current_delete_inventory = None
current_delete_film = None
current_delete_rental = None
current_delete_payment = None
# ---------------------------------------------------------
# Sub Frame (Delete_Customer)
# ---------------------------------------------------------
def close_delete_customer_frame(event=None):
    global current_delete_customer
    current_delete_customer.destroy()
    current_delete_customer = None

def delete_customer_frame(main):
    global current_delete_customer
    if current_delete_customer is not None:
        current_delete_customer.lift()
        return
    # -- Frame --
    delete_customer_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    delete_customer_frame.place(x=30, y=30)
    current_delete_customer = delete_customer_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_delete_customer, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Customer", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_delete_customer_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_delete_customer, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_delete_customer.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_delete_customer.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e:start_move(e, current_delete_customer))
    title_bar.bind("<B1-Motion>", lambda e:on_drag(e, current_delete_customer))
    title_label.bind("<Button-1>", lambda e:start_move(e, current_delete_customer))
    title_label.bind("<B1-Motion>", lambda e:on_drag(e, current_delete_customer))
# ---------------------------------------------------------
# Sub Frame (Delete_Inventory)
# ---------------------------------------------------------
def close_delete_inventory_frame(event=None):
    global current_delete_inventory
    current_delete_inventory.destroy()
    current_delete_inventory = None

def delete_inventory_frame(main):
    global current_delete_inventory
    if current_delete_inventory is not None:
        current_delete_inventory.lift()
        return
    # -- Frame --
    delete_inventory_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    delete_inventory_frame.place(x=30, y=30)
    current_delete_inventory = delete_inventory_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_delete_inventory, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Inventory", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_delete_inventory.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_delete_inventory_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_delete_inventory, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_delete_inventory.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_delete_inventory.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_delete_inventory))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_delete_inventory))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_delete_inventory))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_delete_inventory))
# ---------------------------------------------------------
# Sub Frame (Delete_Film)
# ---------------------------------------------------------
def close_delete_film_frame(event=None):
    global current_delete_film
    current_delete_film.destroy()
    current_delete_film = None

def delete_film_frame(main):
    global current_delete_film
    if current_delete_film is not None:
        current_delete_film.lift()
        return
    # -- Frame --
    delete_film_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    delete_film_frame.place(x=30, y=30)
    current_delete_film = delete_film_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_delete_film, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Film", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_delete_film.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_delete_film_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_delete_film, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_delete_film.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_delete_film.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_delete_film))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_delete_film))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_delete_film))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_delete_film))
# ---------------------------------------------------------
# Sub Frame (Delete_Rental)
# ---------------------------------------------------------
def close_delete_rental_frame(event=None):
    global current_delete_rental
    current_delete_rental.destroy()
    current_delete_rental = None

def delete_rental_frame(main):
    global current_delete_rental
    if current_delete_rental is not None:
        current_delete_rental.lift()
        return
    # -- Frame --
    delete_rental_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    delete_rental_frame.place(x=30, y=30)
    current_delete_rental = delete_rental_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_delete_rental, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Rental", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_delete_rental.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_delete_rental_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_delete_rental, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_delete_rental.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_delete_rental.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_delete_rental))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_delete_rental))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_delete_rental))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_delete_rental))
# ---------------------------------------------------------
# Sub Frame (Delete_Payment)
# ---------------------------------------------------------
def close_delete_payment_frame(event=None):
    global current_delete_payment
    current_delete_payment.destroy()
    current_delete_payment = None

def delete_payment_frame(main):
    global current_delete_payment
    if current_delete_payment is not None:
        current_delete_payment.lift()
        return
    # -- Frame --
    delete_payment_frame = tkinter.Frame(main, width=300, height=300, bg=Colors.background, relief="raised", bd=3)
    delete_payment_frame.place(x=30, y=30)
    current_delete_payment = delete_payment_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_delete_payment, bg=Colors.primary, height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Payment", bg=Colors.primary, fg=Colors.title_text, font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_delete_payment.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg=Colors.alert, fg=Colors.background, width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_delete_payment_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_delete_payment, bg=Colors.background)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg=Colors.background, fg=Colors.text).pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색",
                   bg=Colors.action, fg="white",
                   activebackground=Colors.primary, activeforeground="white",
                   relief="flat").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_delete_payment.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_delete_payment.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_delete_payment))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_delete_payment))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_delete_payment))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_delete_payment))