import flet

basic_content = flet.Container(
    content=flet.Text("Welcome Sakila"),
    alignment=flet.alignment.center,
    expand=True,
    border_radius=5,
    bgcolor=flet.Colors.AMBER_100
)
def navi(page: flet.Page):
    def on_nav_change(e):
        index = e.control.selected_index
        print(index)
        if index == 0:
            basic_content.content.value = "메뉴"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.SURFACE
        elif index == 1:
            basic_content.content.value = "조회"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BLUE
        elif index == 2:
            basic_content.content.value = "변경"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.BROWN_500
        elif index == 3:
            basic_content.content.value = "삭제"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.YELLOW_200
        elif index == 4:
            basic_content.content.value = "추가"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.LIGHT_BLUE_100
        elif index == 5:
            basic_content.content.value = "통계"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.DEEP_ORANGE_200
        elif index == 6:
            basic_content.content.value = "관리"
            basic_content.content.color = flet.Colors.ON_SURFACE
            basic_content.bgcolor = flet.Colors.CYAN_400
        basic_content.update()

    rail = flet.NavigationRail(
        selected_index=0,
        label_type=flet.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            flet.NavigationRailDestination(
                icon=flet.Icons.MENU,
                selected_icon=flet.Icons.MENU_ROUNDED,
                label="Menu"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.SCREEN_SEARCH_DESKTOP_ROUNDED,
                selected_icon=flet.Icons.SCREEN_SEARCH_DESKTOP_OUTLINED,
                label="Search"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.CHANGE_CIRCLE,
                selected_icon=flet.Icons.CHANGE_CIRCLE_OUTLINED,
                label="Change"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.DELETE,
                selected_icon=flet.Icons.DELETE_OUTLINE,
                label="Delete"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.ADD_BOX,
                selected_icon=flet.Icons.ADD_BOX_OUTLINED,
                label="Add"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.QUERY_STATS,
                selected_icon=flet.Icons.QUERY_STATS_ROUNDED,
                label="Statistic"
            ),
            flet.NavigationRailDestination(
                icon=flet.Icons.MANAGE_ACCOUNTS,
                selected_icon=flet.Icons.MANAGE_ACCOUNTS_OUTLINED,
                label="Manager"
            )
        ], on_change=on_nav_change,
    )
    page.add(
        flet.Row(
            [
                rail,
                flet.VerticalDivider(width=1),
                basic_content,
            ],
            expand=True,
        )
    )


flet.app(target=navi)