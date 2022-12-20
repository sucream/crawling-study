from automation.crawl.paperswithcode import get_paper_list
from automation.crawl.google import get_google_images


def paper():
    get_paper_list()


def google_images():
    get_google_images('cat', 100)


if __name__ == "__main__":
    # paper()
    google_images()
