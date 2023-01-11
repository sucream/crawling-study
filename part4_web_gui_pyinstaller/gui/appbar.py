import flet as ft


app_bar = ft.AppBar(
    leading=ft.Icon(ft.icons.NEWSPAPER),
    leading_width=40,
    title=ft.Text('네이버 뉴스 크롤러'),
    bgcolor='black54',
    actions=[
        ft.IconButton(ft.icons.SETTINGS)
    ]
)