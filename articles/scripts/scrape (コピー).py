import re
import json
import time
import datetime

from urllib import request, parse


class MovieWalkerCroller(object):
    def __init__(self):
        self.domain = 'http://movie.walkerplus.com'
        self.base_url = parse.urljoin(self.domain, 'list/index.cgi')
        self.title_pattern = re.compile(r'<div class=\"moviePhoto\"><a href=\"/mv\d+/\"><img src=\"(?P<img_path>\S+?.jpg)\" width=\"\d+\" height=\"\d+\" alt=\"(?P<title>.+?)\"></a></div>')
        self.date_pattern = re.compile(r'<dl class=\"movieDate\">\s*?<dt>(?P<year>\d*?)年*(?P<month>\d+?)月(?P<day>\d+?)日')
        self.params = ['genre', 'page']
        self.genre_map = {1: 'action', 2: 'suspense', 3: 'horror', 4: 'Fantasy', 5: 'comedy', 6: 'love', 7: 'drama', 8: 'documentary', 9: 'animation', 12: 'musical'}

    def croll(self):
        i_limit = 13
        j_limit = 20
        for i in range(1, i_limit):
            try:
                genre = self.genre_map[i]
            except KeyError:
                genre = ''
            for j in range(1, j_limit):
                objs = self.scrape(self.urljoin(dict({self.params[0]: i, self.params[1]: j})))
                if not objs:
                    break
                else:
                    time.sleep(10)
                    for obj in objs:
                        obj.append(genre)
                        yield obj

    def urljoin(self, params):
        return '?'.join([self.base_url, parse.urlencode(params)])

    def scrape(self, url):
        movie_objs = []
        print(url)
        try:
            res = request.urlopen(url)
        except:
            return None
        content = res.read().decode('utf-8')
        date_objs = re.findall(self.date_pattern, content)
        title_objs = re.findall(self.title_pattern, content)
        for title_obj, date_obj in zip(title_objs, date_objs):
            if not date_obj[0]:
                date_obj = list(date_obj)
                date_obj[0] = datetime.datetime.today().year
            year, month, day = tuple(map(int, date_obj))
            date_obj = datetime.date(year, month, day)
            movie_objs.append([title_obj[0], title_obj[1], date_obj])
        return movie_objs ##((img_url, title, (year, month, day)), ...)

class MovieImageScraper(object):
    def __init__(self):
        self.APIKEY = 'AIzaSyCDolzaxZwoB0BU2HqRZSc4YB4G4SiSkAE'
        self.SEARCH_ENGINE_ID = '010256990270467054379:nzfnnq419ds'

    def make_request(self, title):
        query = ' '.join(['映画', title])
        params = {'key': self.APIKEY, 'cx': self.SEARCH_ENGINE_ID,
                    'searchType': 'image', 'num': '1', 'q': query}
        request_url = '?'.join(['https://www.googleapis.com/customsearch/v1', parse.urlencode(params)])
        return request_url

    def execute(self, title):
        request_url = self.make_request(title)
        try:
            response = request.urlopen(request_url).read().decode('utf-8')
        except:
            return ''
        result = json.loads(response)['items'][0]['link']
        return result

if __name__ == '__main__':
    pass
