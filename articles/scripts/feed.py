import re
from urllib import request, parse
from bs4 import BeautifulSoup
from readability import readability
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

class APIController(object):
    def __init__(self):
        pass

    def feed(self):
        pass

class AsahiCroller(object):
    def __init__(self):
        self.url = 'http://www.asahi.com/edu/list/kosodate.html'
        self.root_url = 'www.asahi.com'

    def get_target_html(self, url):
        try:
            res = request.urlopen(url)
        except:
            return None
        content = res.read().decode('utf-8')
        return content

    def yield_feed(self):
        content = self.get_target_html(self.url)
        if not content:
            return None
        soup = BeautifulSoup(content, 'html.parser')
        article_division = soup.find('div', class_='Section SectionFst')
        for elem in article_division.find_all('a'):
            yield elem.contents[0], ''.join([self.root_url, elem.get('href')])

def test():
    ac = AsahiCroller()
    re = ReadabilityExtractor()
    for x in ac.yield_feed():
        print(re.digest(request.urlopen(''.join(['http://', x[1]])).read(), 200))
        time.sleep(5)

test()
