from appbar import app_bar
from views.index import MainView
from components.FormContainer import FormContainer
from automation import crud, schemas

import flet as ft


class MainContainer(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Container(
            width=275,
            height=60,
            content=ft.Column(
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value='Modern Dropdown Control Example',
                        size=10,
                        weight='w400',
                        color='white54',
                    ),
                    ft.Text(
                        value='Line Indent',
                        size=30,
                        weight='bold',
                    )
                ]
            )
        )

class DropDownContainer(ft.UserControl):
    def __init__(self):
        super().__init__()
    
    def build(self):
        return ft.Container(

        )

def main(page: ft.Page):
    
    # 디버깅을 위한 키보드 이벤트 핸들러
    def on_keyboard(e: ft.KeyboardEvent):
        # print(e)
        if e.key == "S" and e.ctrl:
            page.show_semantics_debugger = not page.show_semantics_debugger
            page.update()

    page.on_keyboard_event = on_keyboard


    def add_category(e):
        """
        카테고리 생성 버튼 클릭 이벤트 핸들러
        """
        print('category_name:', category_name_ref.current.value)
        print('main_section:', main_section_ref.current.value)
        print('sub_section:', sub_section_ref.current.value)

        try:
            category_obj = schemas.CategoryCreate(
                category_name=category_name_ref.current.value,
                main_section=main_section_ref.current.value,
                sub_section=sub_section_ref.current.value
            )
            new_category = crud.create_new_category(category_obj)
        except Exception as e:
            print(e)
        else:
            main_view.refresh()

        bottom_sheet.close()

    

    # 타이틀 설정
    page.title = '네이버 뉴스 크롤러'

    # 앱바
    page.appbar = app_bar

    # 카테고리 추가 폼에서 사용할 데이터
    category_name_ref = ft.Ref[ft.TextField]()
    main_section_ref = ft.Ref[ft.TextField]()
    sub_section_ref = ft.Ref[ft.TextField]()

    main_view = MainView()

    bottom_sheet = FormContainer(category_name_ref, main_section_ref, sub_section_ref, add_category)

    page.add(main_view)
    page.add(bottom_sheet)
    page.add(ft.FloatingActionButton(
            icon=ft.icons.ADD,
            tooltip="새로운 카테고리 추가",
            on_click=bottom_sheet.show,
        )
    )

    page.scroll = ft.ScrollMode.ADAPTIVE

    # DEBUG
    # page.show_semantics_debugger = True

    page.update()
    


if __name__ == '__main__':
    ft.app(target=main)