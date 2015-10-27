from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup

__author__ = 'Luke'

class Author:
    def __init__(self, name, intro):
        self.name = name
        self.intro = intro

class Book:
    def __init__(self, url):
        self.url = url
        self.id = list(filter(None, urlparse(url).path.split("/")))[-1]

        html = urlopen(url)
        bs_html = BeautifulSoup(html.read(), "html.parser")
        self.name = bs_html.select_one("#wrapper > h1 > span").get_text()

        bs_info = bs_html.select_one("#info")
        bs_author_title = bs_info.find(text = " 作者")
        if bs_author_title is not None:
            self.author = bs_author_title.parent.find_next_sibling("a").get_text()

        bs_publisher_title = bs_info.find(text = "出版社:")
        if bs_publisher_title is not None:
            self.publisher = bs_publisher_title.parent.next_sibling.string

        bs_publish_date_title = bs_info.find(text = "出版年:")
        if bs_publish_date_title is not None:
            self.publish_date = bs_publish_date_title.parent.next_sibling.string

        bs_page_title = bs_info.find(text = "页数:")
        if bs_page_title is not None:
            self.page = bs_page_title.parent.next_sibling.string

        bs_price_title = bs_info.find(text = "定价:")
        if bs_price_title is not None:
            self.price = bs_price_title.parent.next_sibling.string

        bs_binding_title = bs_info.find(text = "装帧:")
        if bs_binding_title is not None:
            self.binding = bs_binding_title.parent.next_sibling.string

        bs_series_title = bs_info.find(text = "丛书:")
        if bs_series_title is not None:
            bs_series_a = bs_binding_title.parent.find_next_sibling("a")
            self.series = bs_series_a.get_text()
            self.series_url = bs_series_a["href"]

        bs_isbn_title = bs_info.find(text = "ISBN:")
        if bs_isbn_title is not None:
            self.isbn = bs_isbn_title.parent.next_sibling.string

        bs_mainpic = bs_html.select_one("#mainpic")
        if bs_mainpic is not None:
            self.cover = bs_mainpic.select_one("a")["href"]


        bs_article = bs_html.select_one("#content > div > div.article")
        bs_related_info = bs_article.select_one("div.related_info")

        bs_intro = bs_related_info.select_one("#link-report")
        bs_hidden_intro = bs_intro.select_one("span.all.hidden")
        if bs_hidden_intro is not None:
            self.intro = bs_hidden_intro.select_one("div > div").get_text()
        else:
            self.intro = bs_intro.find("div",attrs={"class": "intro"}).get_text()

        bs_author_intro_title = bs_related_info.find(text = "作者简介")
        if bs_author_intro_title is not  None:
            bs_author_intro = bs_author_intro_title.parent.parent.find_next_sibling("div").select_one("div > div.intro")
            if bs_author_intro is not None:
                self.author_intro = bs_author_intro.get_text()
            else:
                self.author_intro = bs_author_intro_title.parent.parent.find_next_sibling("div").select_one("span.all.hidden > div.intro").get_text()


        bs_catalog = bs_related_info.select_one("#dir_%s_full" % self.id)
        if bs_catalog is not None:
            self.catalog = bs_catalog.get_text().replace("· · · · · ·     (收起)", "")
        else:
            bs_catalog = bs_related_info.select_one("#dir_%s_short" % self.id)
            if bs_catalog is not None:
                self.catalog = bs_catalog.get_text()

b = Book("http://book.douban.com/subject/26278639/")
print(b.name)
