
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.parse import urlparse

from bs4 import BeautifulSoup

__author__ = 'Luke'

#名人
class Celebrity:
    def __init__(self, bs_celebrity_element):
        self.name = bs_celebrity_element.string
        self.id = bs_celebrity_element['href']

    def __str__(self):
        return "Celebrity: %s, %s" % (self.name, self.id)

class AwardInfo:
    def __init__(self, award_url):
        html = urlopen(award_url)
        bs_html = BeautifulSoup(html.read(), "html.parser")
        bs_award_list = bs_html.find_all("div", attrs={"class": "awards"})
        awards = []
        for bs_award in bs_award_list:
            award = Award(bs_award)
            if award is not None:
                awards.append(award)

        self.awards = awards


class Award:
    def __init__(self,bs_award):
        title_list = list(bs_award.select_one("div > h2").children)
        self.name = title_list[0]
        self.yeal = title_list[1].get_text(strip=True)

        bs_award_uls = bs_award.find_all("ul", attrs={"class": "award"})

        award_categories = []
        for bs_award_ul in bs_award_uls:
            award_category = AwardCategory(bs_award_ul)
            if award_category is not  None:
                award_categories.append(award_category)
        self.award_categories = award_categories

class AwardCategory:
    def __init__(self, bs_award_ul):
        bs_award_lis = bs_award_ul.find_all("li")
        if len(bs_award_lis) >= 1:
            self.name = bs_award_lis[0].get_text(strip=True)
        if len(bs_award_lis) >= 2:
            bs_celebrities = bs_award_lis[1]
            bs_celebrity_as = bs_celebrities.find_all("a")
            celebrities = []
            for bs_celebrity_a in bs_celebrity_as:
                celebrity = Celebrity(bs_celebrity_a)
                if celebrity is not None:
                    celebrities.append(celebrity)
            self.celebrities = celebrities

class PosterLibrary:
    def __init__(self, movie_url):
        poster_url = urljoin(movie_url,"photos?type=R")
        html = urlopen(poster_url)
        bs_html = BeautifulSoup(html.read(), "html.parser")
        bs_poster_list = bs_html.select_one("#content > div > div.article > ul")
        bs_poster_items = bs_poster_list.find_all("li")
        poster_ids = []
        for bs_poster in bs_poster_items:
            if bs_poster.has_attr("data-id"):
                poster_id = bs_poster['data-id']
                poster_ids.append(poster_id)

        self.poster_ids = poster_ids


#电影
class Movie:

    def __init__(self, url):
        self.url = url
        self.id = list(filter(None, urlparse(url).path.split("/")))[-1]

        html = urlopen(url)
        bs_html = BeautifulSoup(html.read(), "html.parser")
        self.name = bs_html.select_one("#content > h1 > span:nth-of-type(1)").string

        bs_info = bs_html.select_one("#info")

        bs_directors = bs_info.find_all(rel = "v:directedBy")
        directors = []
        for bs_director in bs_directors:
            director = Celebrity(bs_director)
            directors.append(director)

        self.directors = directors

        bs_screenwriters = bs_info.find(text = "编剧").parent.find_next_sibling("span").find_all("a")
        screenwriters = []
        for bs_screenwriter in bs_screenwriters:
            screenwriter = Celebrity(bs_screenwriter)
            screenwriters.append(screenwriter)

        self.screenwriters = screenwriters

        bs_actors = bs_info.find_all(rel = "v:starring")
        actors = []
        for bs_actor in bs_actors:
            actor = Celebrity(bs_actor)
            actors.append(actor)

        self.actors = actors

        bs_genres = bs_info.find_all(property = "v:genre")
        genres = []
        for bs_genre in bs_genres:
            genre = bs_genre.string
            genres.append(genre)

        self.genres = genres

        bs_website_text = bs_info.find(text = "官方网站:")
        if bs_website_text is not None:
            self.website = bs_website_text.parent.find_next_sibling("a")['href']
        self.country = bs_info.find(text = "制片国家/地区:").parent.next_sibling.string
        self.language = bs_info.find(text = "语言:").parent.next_sibling.string

        bs_release_dates = bs_info.find_all(property = "v:initialReleaseDate")
        release_dates = []
        for bs_release_date in bs_release_dates:
            release_date = bs_release_date.string
            release_dates.append(release_date)

        self.release_dates = release_dates
        bs_runtime = bs_info.find(property = "v:runtime")
        if bs_runtime is not None:
            self.runtime = bs_runtime.string
        else:
            bs_runtime_text = bs_info.find(text = "单集片长:")
            if bs_runtime_text is not None:
                self.runtime = bs_runtime_text.parent.next_sibling.string

        bs_episodes_text = bs_info.find(text = "集数:")
        if bs_episodes_text is not None:
            self.is_tv = True
            self.episodes = bs_episodes_text.parent.next_sibling.string

        self.alias = bs_info.find(text = "又名:").parent.next_sibling.string
        self.imdb_link = bs_info.find(text = "IMDb链接:").parent.find_next_sibling("a")['href']

        self.summary = bs_html.find(property = "v:summary").get_text(strip=True)

        bs_interest_sectl = bs_html.select_one("#interest_sectl")
        self.rating_num = bs_interest_sectl.select_one("div.rating_wrap.clearbox > div.rating_self").string
        self.votes = bs_interest_sectl.find(property = "v:votes").string

        self.award_info = AwardInfo(urljoin(self.url,"awards"))


        self.poster_library = PosterLibrary(self.url)






m = Movie("http://movie.douban.com/subject/3541415/")

print(m.language)