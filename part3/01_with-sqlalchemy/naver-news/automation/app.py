from datetime import datetime
import platform

from automation import crud
from automation.crawl import naver_news
# from automation.utils import cls, getch

import click


@click.command()
@click.pass_context
def cli(ctx) -> None:
    """
    CLI를 관장하는 메인 함수입니다.
    """
    while True:
        click.clear()

        click.echo(click.style("[ 네이버 뉴스 관리 프로그램 ]", fg="yellow", bold=True))
        click.echo()
        click.echo("1. 카테고리 조회")
        click.echo("2. 카테고리 등록")
        click.echo("3. 뉴스 조회")
        click.echo("4. 뉴스 업데이트")
        click.echo("5. 뉴스 삭제")
        click.echo("0. 종료")
        click.echo()

        try:
            choice = click.prompt("메뉴를 선택하세요", type=int, default=0)
        except Exception as e:
            continue

        if choice == 1:
            ctx.invoke(list_all_category)
        elif choice == 2:
            ctx.invoke(add_new_category)
        elif choice == 3:
            ctx.invoke(list_news)
        elif choice == 4:
            ctx.invoke(fetch_news_list)
        elif choice == 5:
            ctx.invoke(delete_news_list)
        elif choice == 0:
            click.echo("종료합니다.")
            break
        else:
            continue

@click.command()
@click.pass_context
def list_all_category(ctx) -> None:
        """
        ### 현재 등록된 카테고리 목록을 출력합니다.
        """
        click.clear()

        click.echo(click.style("[ 현재 카테고리 목록 ]", fg="green", bold=True))
        for category in crud.get_all_category_list():
            click.echo(f"{category.id}: {category}")
        click.echo()

        click.echo("계속하려면 아무 키나 누르세요...")
        click.getchar()




@click.command()
@click.pass_context
def add_new_category(ctx) -> None:
    """
    ### 새로운 카테고리를 등록합니다.
    """

    click.clear()

    click.echo()
    click.echo(click.style("[ 새로운 카테고리 등록 ]", fg="green", bold=True))
    main_section = click.prompt("대분류 섹션(sid1)")

    sub_section = click.prompt("소분류 섹션(sid2)")

    category_name = click.prompt("카테고리 이름 입력")

    click.echo()
    click.echo(click.style("[입력 정보 확인]", fg="red"))
    click.echo(f"대분류 섹션: {main_section}")
    click.echo(f"소분류 섹션: {sub_section}")
    click.echo(f"카테고리 이름: {category_name}")
    click.echo()
    
    confirm: str = click.prompt("입력하신 정보가 맞습니까? (y/n)", type=str)
    
    if confirm.upper() != "Y":
        return

    new_category = crud.create_new_category(main_section, sub_section, category_name)
        
    click.echo(f"새로운 카테고리[{new_category}]가 등록되었습니다.", color="green")

    click.echo("계속하려면 아무 키나 누르세요...")
    click.getchar()


@click.command()
@click.pass_context
def list_news(ctx) -> None:
    """
    ### 현재 등록된 뉴스 목록을 출력합니다.
    """
    
    start_page = 1

    # listing process loop
    while True:
        # category selection loop
        while True:
            click.clear()

            click.echo(click.style("[ 뉴스 조회 ]", fg="green", bold=True))
            click.echo(click.style("[ 현재 카테고리 목록 ]", fg="green"))
            for category in crud.get_all_category_list():
                click.echo(f"{category.id}: {category}")
            click.echo()

            try:
                category_id = click.prompt("조회할 카테고리의 번호를 입력하세요", type=int, default=0)
            except Exception as e:
                continue

            if category_id == 0:
                break

            search_category = crud.get_category_by_id(category_id)

            if not search_category:
                click.echo("해당하는 카테고리가 없습니다.")
                continue

            break

        if category_id == 0:
            break

        news_list = crud.get_all_news_list_by_category_id(category_id)

        if not news_list:
            click.prompt("해당 카테고리에 해당하는 뉴스가 없습니다.\n카테고리 선택으로 돌아가기...", default=0, show_default=False)
            continue

        for news in news_list:
            click.echo(click.style(news, fg="black", bold=True))

        click.echo("계속하려면 아무 키나 누르세요...")
        click.getchar()

@click.command()
@click.pass_context
def fetch_news_list(ctx) -> None:
    """
    ### 뉴스 목록을 가져옵니다.
    """
    click.clear()

    while True:
        while True:
            click.clear()

            click.echo(click.style("[ 뉴스 업데이트 ]", fg="green", bold=True))
            click.echo(click.style("[ 현재 카테고리 목록 ]", fg="green"))
            for category in crud.get_all_category_list():
                click.echo(f"{category.id}: {category}")
            click.echo()

            try:
                category_id = click.prompt("업데이트할 카테고리의 번호를 입력하세요", type=int, default=0)
            except Exception as e:
                continue

            if category_id == 0:
                break

            search_category = crud.get_category_by_id(category_id)

            if not search_category:
                click.echo("해당하는 카테고리가 없습니다.")
                continue

            break

        if category_id < 1:
            break

        category = crud.get_category_by_id(category_id)
        if not category:
            click.echo("해당하는 카테고리가 없습니다.")
            return

        while True:
            click.echo("날짜를 입력하세요. (예: 20220101)(기본값: 오늘)")
            date = click.prompt("날짜 입력: ", type=str, default=datetime.today().strftime("%Y%m%d"))

            try:
                datetime.strptime(date, '%Y%m%d')
            except ValueError:
                click.prompt("날짜 형식이 잘못되었습니다. (예: 20220101)")
                continue

            if datetime.strptime(date, '%Y%m%d') > datetime.today():
                click.prompt("날짜가 잘못되었습니다. (오늘 이후의 날짜는 입력할 수 없습니다.)")
                continue

            break

        page_num = 1
        while True:
            break_flag = False
            news_list = naver_news.get_news_list(category.main_section, category.sub_section, date, page_num)

            if not news_list:
                click.echo(click.style("뉴스 목록을 가져오는데 실패했습니다.", fg="red"))

            for news in news_list:
                try:
                    crud.create_new_news(category_id, news['title'], None, news['url'], news['date'])
                except Exception as e:
                    click.echo(click.style(f"{news['title']} 뉴스를 저장하는데 실패했습니다.", fg="red"))
                    click.echo(str(e))
                    break_flag = True
                    break
                else:
                    click.echo(click.style(f"{news['title']} 뉴스를 저장했습니다.", fg="green"))

            if break_flag:
                break

            click.echo(click.style(f"{page_num} 페이지 뉴스 목록을 가져왔습니다.", fg="blue"))
            page_num += 1

            click.echo('아무 키나 누르면 다음 페이지로 넘어갑니다.')
            click.getchar()

        click.echo('계속하려면 아무 키나 누르세요...')
        click.getchar()


@click.command()
@click.pass_context
def delete_news_list(ctx) -> None:
    while True:
        click.clear()
        click.echo(click.style("[ 뉴스 삭제 ]", fg="red", bold=True))
        click.echo(click.style("[ 현재 카테고리 목록 ]", fg="green"))
        for category in crud.get_all_category_list():
            click.echo(f"{category.id}: {category}")
        click.echo()

        try:
            category_id = click.prompt("조회할 카테고리의 번호를 입력하세요", type=int, default=0)
        except Exception as e:
            continue

        if category_id == 0:
            break

        search_category = crud.get_category_by_id(category_id)

        if not search_category:
            click.echo("해당하는 카테고리가 없습니다.")
            continue

        break

    if category_id == 0:
        return

    click.echo()
    if not click.confirm("해당 카테고리의 뉴스를 삭제하시겠습니까?"):
        return

    crud.delete_news_by_category_id(search_category.id)

    click.echo("<뉴스가 삭제되었습니다.>")
    click.getchar()