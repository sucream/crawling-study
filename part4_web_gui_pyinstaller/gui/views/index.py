from components.Category import Category
from automation import crud

import flet as ft


class MainView(ft.UserControl):
    def __init__(self):
        super().__init__()

    def refresh(self):
        self.category_list.controls.clear()
        cat_list = crud.get_all_category_list()
        
        for cat in cat_list:
            self.category_list.controls.append(Category(cat.id, cat.category_name, cat.main_section, cat.sub_section))

        self.category_list.update()

    def build(self):
        self.category_list = ft.Column(
            # scroll=ft.ScrollMode.ALWAYS,
            spacing=10,
            controls=[],
        )

        cat_list = crud.get_all_category_list()
        
        for cat in cat_list:
            self.category_list.controls.append(Category(cat.id, cat.category_name, cat.main_section, cat.sub_section))

        return self.category_list