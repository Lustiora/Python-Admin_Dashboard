# ---------------------------------------------------------
# Import Package
# ---------------------------------------------------------
import tkinter
from window import start_move, on_drag
# ---------------------------------------------------------
# Variable
# ---------------------------------------------------------
current_add_customer = None
current_add_inventory = None
current_add_film = None
current_add_actor = None
current_add_category = None
# ---------------------------------------------------------
# Sub Frame (add_Customer)
# ---------------------------------------------------------
def close_add_customer_frame(event=None):
    global current_add_customer
    current_add_customer.destroy()
    current_add_customer = None

def add_customer_frame(main):
    global current_add_customer
    if current_add_customer is not None:
        current_add_customer.lift()
        return
    # -- Frame --
    add_customer_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    add_customer_frame.place(x=30, y=30)
    current_add_customer = add_customer_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_add_customer, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Customer", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_add_customer_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_add_customer, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_add_customer.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_add_customer.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e:start_move(e, current_add_customer))
    title_bar.bind("<B1-Motion>", lambda e:on_drag(e, current_add_customer))
    title_label.bind("<Button-1>", lambda e:start_move(e, current_add_customer))
    title_label.bind("<B1-Motion>", lambda e:on_drag(e, current_add_customer))
# ---------------------------------------------------------
# Sub Frame (add_Inventory)
# ---------------------------------------------------------
def close_add_inventory_frame(event=None):
    global current_add_inventory
    current_add_inventory.destroy()
    current_add_inventory = None

def add_inventory_frame(main):
    global current_add_inventory
    if current_add_inventory is not None:
        current_add_inventory.lift()
        return
    # -- Frame --
    add_inventory_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    add_inventory_frame.place(x=30, y=30)
    current_add_inventory = add_inventory_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_add_inventory, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Inventory", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_add_inventory.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_add_inventory_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_add_inventory, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_add_inventory.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_add_inventory.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_add_inventory))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_add_inventory))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_add_inventory))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_add_inventory))
# ---------------------------------------------------------
# Sub Frame (add_Film)
# ---------------------------------------------------------
def close_add_film_frame(event=None):
    global current_add_film
    current_add_film.destroy()
    current_add_film = None

def add_film_frame(main):
    global current_add_film
    if current_add_film is not None:
        current_add_film.lift()
        return
    # -- Frame --
    add_film_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    add_film_frame.place(x=30, y=30)
    current_add_film = add_film_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_add_film, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Film", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_add_film.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_add_film_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_add_film, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_add_film.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_add_film.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_add_film))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_add_film))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_add_film))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_add_film))
# ---------------------------------------------------------
# Sub Frame (add_actor)
# ---------------------------------------------------------
def close_add_actor_frame(event=None):
    global current_add_actor
    current_add_actor.destroy()
    current_add_actor = None

def add_actor_frame(main):
    global current_add_actor
    if current_add_actor is not None:
        current_add_actor.lift()
        return
    # -- Frame --
    add_actor_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    add_actor_frame.place(x=30, y=30)
    current_add_actor = add_actor_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_add_actor, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Actor", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_add_actor.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_add_actor_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_add_actor, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_add_actor.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_add_actor.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_add_actor))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_add_actor))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_add_actor))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_add_actor))
# ---------------------------------------------------------
# Sub Frame (add_category)
# ---------------------------------------------------------
def close_add_category_frame(event=None):
    global current_add_category
    current_add_category.destroy()
    current_add_category = None

def add_category_frame(main):
    global current_add_category
    if current_add_category is not None:
        current_add_category.lift()
        return
    # -- Frame --
    add_category_frame = tkinter.Frame(main, width=300, height=300, bg="white", relief="raised", bd=3)
    add_category_frame.place(x=30, y=30)
    current_add_category = add_category_frame
    # -- Title Bar --
    title_bar = tkinter.Frame(current_add_category, bg="#2c3e50", height=30)
    title_bar.pack(fill="x", side="top")
    title_label = tkinter.Label(title_bar, text="Category", bg="#2c3e50", fg="white", font=("Arial", 11, "bold"))
    title_label.pack(side="left", padx=5)
    title_label.bind("<Button-1>", current_add_category.lift)
    # -- Close --
    close_btn = tkinter.Label(title_bar, text="X", bg="#e74c3c", fg="white", width=4)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", close_add_category_frame)
    # -- Body --
    content_frame = tkinter.Frame(current_add_category, bg="white")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tkinter.Label(content_frame, text="회원 번호 입력:", bg="white").pack(pady=5)
    tkinter.Entry(content_frame).pack(pady=5)
    tkinter.Button(content_frame, text="검색").pack(pady=5)
    # -- Click Event --
    content_frame.bind("<Button-1>", lambda e: current_add_category.lift())
    for widget in content_frame.winfo_children():
        widget.bind("<Button-1>", lambda e: current_add_category.lift(), add="+")
    title_bar.bind("<Button-1>", lambda e: start_move(e, current_add_category))
    title_bar.bind("<B1-Motion>", lambda e: on_drag(e, current_add_category))
    title_label.bind("<Button-1>", lambda e: start_move(e, current_add_category))
    title_label.bind("<B1-Motion>", lambda e: on_drag(e, current_add_category))