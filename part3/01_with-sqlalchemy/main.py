from automation.init import init
from automation.crud import *

def add_image():
    print("[ 이미지 등록 ]")
    print("키워드 입력: ", end="")
    keyword = input()

    try:
        keyword_item = create_keyword(keyword)
    except Exception as e:
        print(e)
        print("키워드 등록에 실패했습니다.")
        return

    for i in range(1, 10):
        print(f"{i}. 이미지 {i}")
        try:
            image_item = create_image(f'https://test.com/{keyword}/{i}', keyword_item.id)
        except Exception as e:
            print(e)
            print(f"{keyword}/{i} 이미지 등록에 실패했습니다.")
            continue
        print(image_item)

    return


def list_image():
    print("[ 이미지 목록 ]")
    print("키워드 입력: ", end="")
    keyword = input()

    try:
        keyword_item = get_keyword_by_keyword(keyword)
    except Exception as e:
        print(e)
        print("키워드 조회에 실패했습니다.")
        return

    if keyword_item is None:
        print("키워드가 존재하지 않습니다.")
        return

    print(keyword_item)

    image_list = get_images_by_keyword_id(keyword_item.id)
    for image_item in image_list:
        print(image_item)

    return



def print_menu():
    print("1. 이미지 등록")
    print("2. 이미지 목록")
    print("3. 이미지 삭제")
    print("4. 종료")
    print("메뉴를 선택하세요: ", end="")
    return input()

def main():
    init()

    while True:
        menu = print_menu()
        if menu == "1":
            add_image()
        elif menu == "2":
            list_image()
        elif menu == "3":
            pass
        elif menu == "4":
            break
        else:
            print("잘못된 메뉴입니다.")

        print()


if __name__ == "__main__":
    main()