from typing import Callable

import flet as ft


class FormContainer(ft.UserControl):
    """
    카테고리 추가 폼 컨테이너
    """
    def __init__(self, category_name_ref: ft.Ref[ft.TextField], main_section_ref: ft.Ref[ft.TextField], sub_section_ref: ft.Ref[ft.TextField], add_category_handler: Callable[[ft.Event], None]):
        """
        카테고리 추가 폼 컨테이너 생성자

        Parameters
        ----------
        category_name_ref : ft.Ref[ft.TextField]
            카테고리 이름 레퍼런스
        main_section_ref : ft.Ref[ft.TextField]
            메인 섹션 레퍼런스
        sub_section_ref : ft.Ref[ft.TextField]
            서브 섹션 레퍼런스
        add_category_handler : Callable[[ft.Event], None]
            카테고리 추가 버튼 클릭 이벤트 핸들러
        """

        super().__init__()
        self.bottom_sheet = ft.BottomSheet()
        self.category_name_ref = category_name_ref
        self.main_section_ref = main_section_ref
        self.sub_section_ref = sub_section_ref
        self.add_category_handler = add_category_handler

    def show(self, e: ft.Event=None):
        self.bottom_sheet.open = True
        self.bottom_sheet.update()

    def close(self, e: ft.Event=None):
        self.bottom_sheet.open = False
        self.bottom_sheet.update()

    def build(self):
        self.bottom_sheet.content = ft.Container(
            width=300,
            height=300,
            padding=ft.padding.all(20),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.TextField(ref=self.category_name_ref, label="카테고리 이름", hint_text="카테고리 이름을 입력해주세요"),
                    ft.TextField(ref=self.main_section_ref, label="메인 섹션", hint_text="메인 섹션을 입력해주세요"),
                    ft.TextField(ref=self.sub_section_ref, label="서브 섹션", hint_text="서브 섹션을 입력해주세요"),
                    ft.ElevatedButton(text="추가", on_click=self.add_category_handler),
                ]
            )
        )

        return self.bottom_sheet