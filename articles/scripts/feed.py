import re
from urllib import request, parse
from bs4 import BeautifulSoup
from readability import readability
from django.conf import settings
import time


class Extractor(object):
    def __init__(self, extractor):
        self.extractor = extractor

    def digest(html):
        pass

class ReadabilityExtractor(object):
    def __init__(self, extractor=readability.Document):
        self.extractor = extractor
        self.img_pattern = re.compile('<img.+?src=\"(?P<img_url>\S+?.jpg)\"')

    def digest(self, html, length=80):
        main_content = self.extractor(html).summary()
        preface = ''.join([BeautifulSoup(main_content, 'lxml').get_text()[:length], '...'])
        result = re.search(self.img_pattern, main_content)
        if result:
            img_url = result.group('img_url')
        else:
            img_url = ''
        return preface, img_url

class Croller(object):
    def __init__(self, extractor=ReadabilityExtractor):
        self.extractor = extractor()
        self.protocol = 'https://'

    def get_target_html(self, url):
        try:
            res = request.urlopen(url)
        except:
            return None
        content = res.read().decode('utf-8')
        return content

    def get_soup(self):
        content = self.get_target_html(self.url)
        if content:
            return BeautifulSoup(content, 'html.parser')
        else:
            return None

    def yield_elements(self, soup): # yield (title, link)
        pass

    def feed(self):
        soup = self.get_soup()
        for title, link in self.yield_elements(soup):
            try:
                preface, img_url = self.extractor.digest(request.urlopen(''.join([self.protocol, link])).read(), 200)
            except:
                continue
            if img_url:
                if not parse.urlparse(img_url).scheme:
                    img_url = ''.join([self.domain, img_url])
            yield title, link, preface, img_url

class AsahiCroller(Croller):
    def __init__(self):
        super().__init__()
        self.url = 'http://www.asahi.com/edu/list/kosodate.html'
        self.domain = 'www.asahi.com'

    def yield_elements(self, soup):
        article_division = soup.find('div', class_='Section SectionFst')
        for elem in article_division.find_all('a'):
            yield elem.contents[0], ''.join([self.domain, elem.get('href')])

class NikkeiDualCroller(Croller):
    def __init__(self):
        super().__init__()
        self.url = 'http://dual.nikkei.co.jp/education/'
        self.domain = 'dual.nikkei.co.jp'

    def yield_elements(self, soup):
        article_elements = soup.find_all('a', class_='entry_list')
        for article in article_elements:
            yield article.h1.contents[0], ''.join([self.domain, article.get('href')])

class NikkeiDualCrollerb(NikkeiDualCroller):
    def __init__(self):
        super().__init__()
        self.url = 'http://dual.nikkei.co.jp/list.aspx?mid=229'

class KosodateHackCroller(Croller):
    def __init__(self):
        super().__init__()
        self.url = 'https://192abc.com/parenting'
        self.domain = '192abc.com'
        self.protocol = ''

    def yield_elements(self, soup):
        titles = soup.find_all('h2', class_= "list-article__title entry-title")
        links = soup.find_all('a', class_='list-article__link')
        if len(titles) != len(links):
            raise ValueError
        for title, link in zip(titles, links):
            yield title.string, link.get('href')

class KosodateHackCrollerb(KosodateHackCroller):
    def __init__(self):
        super().__init__()
        self.url = 'https://192abc.com/trying-to-conceive'
        self.domain = '192abc.com'
        self.protocol = ''

class KosodateHackCrollerc(KosodateHackCroller):
    def __init__(self):
        super().__init__()
        self.url = 'https://192abc.com/pregnancy'
        self.domain = '192abc.com'
        self.protocol = ''

class ConobieCroller(Croller):
    def __init__(self):
        super().__init__()
        self.url = 'https://conobie.jp/article/ranking/pregnancy'
        self.domain = 'https://conobie.jp/'

    def yield_elements(self, soup):
        pass

class AllAboutCroller(Croller):
    def __init__(self):
        super().__init__()
        self.url = 'https://allabout.co.jp/gm/latest/1212/'
        self.protocol = ''

    def yield_elements(self, soup):
        article_divisions = soup.find_all('li', class_='aa_media aa_media-l aa_media-reverse aa_media-border')
        for article_division in article_divisions:
            title = article_division.find('h2', class_='aa_media-title-l text-bold link-blue').string
            link = article_division.find('a', class_='block-link').get('href')
            yield title, link

class AllAboutCrollerb(AllAboutCroller):
    def __init__(self):
        super().__init__()
        self.url = 'https://allabout.co.jp/gm/latest/1215/'

class AllAboutCrollerc(AllAboutCroller):
    def __init__(self):
        super().__init__()
        self.url = 'https://allabout.co.jp/ch_pregnancy/latest/'


CROLLERS = [AsahiCroller, NikkeiDualCroller, NikkeiDualCrollerb, KosodateHackCroller, KosodateHackCrollerb, KosodateHackCrollerc,
    AllAboutCroller, AllAboutCrollerb, AllAboutCrollerc,
]

def test():
    c = AllAboutCrollerb()
    for i, e in enumerate(c.feed()):
        print(e)
        if i > 8:
            break
        time.sleep(5)

if __name__ == '__main__':
    test()
