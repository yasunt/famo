from urllib import request
import re

class Croller(object):
    def __init__(self):
        self.title_pattern = re.compile('')
        self.url_pattern = re.compile('')
        return self

    def yield_article(self):


class AsahiCroller(Croller):
    def __init__(self):
        self.url = 'http://www.asahi.com/edu/list/kosodate.html'

    def yield_article(self):
        pass
