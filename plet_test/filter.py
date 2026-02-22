import flet
# Filter
filter_rental = flet.Row(
    controls=[
        flet.Dropdown(
            label="Filter",
            value="name_asc",
            bgcolor=flet.Colors.PRIMARY_CONTAINER,
            on_change="",
            options=[
                flet.DropdownOption(text="ID ▲", key="id_asc"),
                flet.DropdownOption(text="ID ▼", key="id_desc"),
                flet.DropdownOption(text="Name ▲", key="name_asc"),
                flet.DropdownOption(text="Name ▼", key="name_desc"),
                flet.DropdownOption(text="Rental Date ▲", key="rental_date_asc"),
                flet.DropdownOption(text="Rental Date ▼", key="rental_date_desc"),
                flet.DropdownOption(text="Due Date ▲", key="due_date_asc"),
                flet.DropdownOption(text="Due Date ▼", key="due_date_desc"),
                flet.DropdownOption(text="Over Due ▲", key="over_due_asc"),
                flet.DropdownOption(text="Over Due ▼", key="over_due_desc"),
            ]
        )
    ]
)