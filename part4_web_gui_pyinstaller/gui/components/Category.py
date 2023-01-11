from automation import crud, schemas
from automation.crawl.naver_news import get_news_list


import flet as ft


class DropDownContainer(ft.UserControl):
    def __init__(self, category_id, category_name, main_section, sub_section):
        super().__init__()
        self.category_id = category_id
        self.category_name = category_name
        self.main_section = main_section
        self.sub_section = sub_section
        self.data_table = ft.Ref[ft.DataTable]()

    def ExpandContainer(self, e):
        """
        카테고리 영역 크기 조절 이벤트 핸들러
        """
        if self.controls[0].height != 300:
            self.controls[0].height = 300
            self.controls[0].update()
        else:
            self.controls[0].height = 100
            self.controls[0].update()

    def TopContainer(self):
        """
        카테고리 상단의 정보 영역
        """

        return ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_DROP_DOWN_CIRCLE_ROUNDED,
                        icon_size=20,
                        on_click=lambda e: self.ExpandContainer(e),
                    )
                )
            ]
        )

    def refresh_news(self, e):
        """
        뉴스 새로고침 버튼 클릭 이벤트 핸들러
        """
        print('refresh news')
        crud.delete_all_news_by_category_id(self.category_id)

        self.data_table.current.rows.clear()

        news_list = get_news_list(self.main_section, self.sub_section)

        for news in news_list:
            news_obj = schemas.NewsCreate(
                title=news['title'],
                url=news['url'],
                publisher=news['publisher'],
                date=news['date'],
                category_id=self.category_id,
            )
            created_news = crud.create_new_news(news_obj)

            self.data_table.current.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(value=created_news.title)),
                        ft.DataCell(ft.TextButton(text=created_news.url, on_click=self.open_url),),
                        ft.DataCell(ft.Text(value=created_news.publisher)),
                    ]
                )
            )

        self.data_table.current.update()

    def delete_news(self, e):
        """
        뉴스 삭제 버튼 클릭 이벤트 핸들러
        """
        print('delete news')
        crud.delete_all_news_by_category_id(self.category_id)

        self.data_table.current.rows.clear()
        self.data_table.current.update()

    def open_url(self, e):
        """
        브라우저에서 URL 열기
        """
        e.page.launch_url(e.control.text)

    def CategoryDataContainer(self):
        """
        카테고리 데이터 영역
        """
        # news_list = [{'title': f'타이틀{i}', 'url': f'URL{i}', 'publisher': f'신문사{i}'} for i in range(10)]
        news_list = crud.get_all_news_list_by_category_id(self.category_id)

        data_table = ft.DataTable(
            ref=self.data_table,
            columns=[
                ft.DataColumn(ft.Text(value="기사 제목")),
                ft.DataColumn(ft.Text(value="URL")),
                ft.DataColumn(ft.Text(value="신문사")),
            ],
            rows=[],
        )

        for news in news_list:
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(value=news.title)),
                        ft.DataCell(ft.TextButton(text=news.url, on_click=self.open_url)),
                        ft.DataCell(ft.Text(value=news.publisher)),
                    ]
                )
            )
        
        return ft.Container(
            alignment=ft.alignment.top_center,
            content=ft.Column(
                height=280,
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    data_table,
                ],
            )
        )
    
    def build(self):
        return ft.Container(
            # width=1000,
            height=100,
            bgcolor='white10',
            border_radius=11,
            animate=ft.animation.Animation(300, ft.AnimationCurve.DECELERATE),
            padding=ft.padding.only(left=10, right=10, top=10),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Stack(
                controls=[
                    self.CategoryDataContainer(),
                    self.TopContainer(),
                ]
            )
        )

class Category(ft.UserControl):
    def __init__(self, category_id: int, category_name: str, main_section: str, sub_section: str):
        """
        하나의 카테고리를 나타내는 컨트롤
        """

        super().__init__()
        self.category_id = category_id
        self.category_name = category_name
        self.main_section = main_section
        self.sub_section = sub_section
        self.drop_down_container = DropDownContainer(self.category_id, self.category_name, self.main_section, self.sub_section)

    def build(self):
        title_area = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                value=self.category_name,
                                size=20,
                                weight='bold',
                            ),
                            ft.Text(
                                value=f'{self.main_section} / {self.sub_section}',
                                size=10,
                                color='white54',
                            ),
                        ]
                    )
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text='갱신',
                            on_click=self.drop_down_container.refresh_news,
                        ),
                        ft.ElevatedButton(
                            text='삭제',
                            on_click=self.drop_down_container.delete_news,
                        ),
                    ]
                )
                
            ]
        )

        return ft.Container(
            padding=10,
            content=ft.Column(
                controls=[
                    title_area,
                    self.drop_down_container,
                    ft.Divider(),
                ]
            )
        )