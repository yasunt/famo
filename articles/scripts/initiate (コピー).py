import time
import os
import datetime
import hmac
from urllib import parse, request
from base64 import b64decode
from django.core.files.base import ContentFile
from django.conf import settings

from curation.croller.feed import HatenabAPIController, ReadabilityExtractor
from curation.croller.scrape import MovieWalkerCroller, MovieImageScraper
from curation.models import Movie, Article, Domain


class DailyScheduledCroller(object):

    MOVIE_IMAGES_FIELD_PATH = 'curation/images/movie_images/'
    MOVIE_IMAGES_TARGET_PATH = os.path.join('curation/static/', MOVIE_IMAGES_FIELD_PATH)

    def __init__(self, title_croller, feed_croller,
                    extractor, movie_img_croller):
        self.title_croller = title_croller()
        self.feed_crollers = []
        self.feed_crollers.append(feed_croller())
        self.extractor = extractor()
        self.movie_img_croller = movie_img_croller()
        self.movie_objs = Movie.objects.all()
        self.article_objs = Article.objects.all()
        self.domain_objs = Domain.objects.all()
        self.movie_img_dir = ''

    def append_new_titles(self):
        new_movie_count = 0
        for movie_info in self.title_croller.croll():
            if movie_info:
                img_url, movie_title, date, genre = list(movie_info)
                print(movie_title, date, genre)
                try:
                    self.movie_objs.get(title=movie_title)
                    continue
                except:
                    pass
                movie_img_path = self.retrieve_movie_img(movie_title)
                movie_obj = Movie(title=movie_title, date=date, genre=genre, image=movie_img_path)
                movie_obj.save()
                new_movie_count += 1
            else:
                continue
        return new_movie_count

    def retrieve_movie_img(self, title):
        img_url = self.movie_img_croller.execute(title)
        if not img_url:
            return ''
        print(img_url)
        suffix = 'jpg'
        filename = '.'.join([hmac.new(bytes(str(datetime.datetime.now()), encoding='utf-8')).hexdigest(), suffix])
        try:
            result = request.urlretrieve(img_url, os.path.join(self.MOVIE_IMAGES_TARGET_PATH, filename))
        except:
            return ''
        return os.path.join(self.MOVIE_IMAGES_FIELD_PATH, filename) ## value of ImageField.

    def make_keywords(self, movie_objs):
        titles = [m.title for m in movie_objs]
        return titles

    def get_new_image(self, movie_obj):
        img_path = self.retrieve_movie_img(movie_obj.title)
        if img_path:
            movie_obj.image = img_path
            movie_obj.save()
            return True
        else:
            return False

    def update_images(self):
        updated_count = 0
        movie_objs = Movie.objects.filter(image='')
        for movie_obj in movie_objs:
            if self.get_new_image(movie_obj):
                updated_count += 1
            else:
                continue
        return updated_count

    def check_image(self, obj):
        if not obj.image:
            return False
        full_path = os.path.join(settings.BASE_DIR, 'curation/static/', obj.image)
        if os.path.exists(full_path):
            return True
        else:
            return False

    def fix_images(self):
        fixed_count = 0
        for movie_obj in Movie.objects.all():
            if self.check_image(movie_obj):
                continue
            else:
                if self.get_new_image(movie_obj):
                    fixed_count += 1
                else:
                    continue
        return fixed_count

    def append_new_feeds(self):
        new_article_count = 0
        keywords = self.make_keywords(self.movie_objs.filter(date__range=[datetime.datetime.today()-datetime.timedelta(days=50), datetime.datetime.today()]))
        for feed_croller in self.feed_crollers:
            for keyword in keywords:
                time.sleep(5)
                for feed_info in feed_croller.yield_feed(keyword):
                    if feed_info:
                        article_title, url = feed_info
                    else:
                        continue
                    article_obj = None
                    try:
                        article_obj = self.article_objs.get(url=url)
                    except:
                        pass
                    if article_obj:
                        continue
                    domain = parse.urlsplit(url).netloc
                    domain_obj = None
                    try:
                        self.domain_objs.get(name=domain)
                    except:
                        pass
                    if not domain_obj:
                        domain_obj = Domain(name=domain)
                        domain_obj.save()
                    try:
                        movie_obj = Movie.objects.get(title=keyword)
                    except:
                        print('Movie: {0} does not exist.'.format(keyword))
                        continue
                    try:
                        html = request.urlopen(url).read()
                    except:
                        continue
                    preface, img_url = self.extractor.digest(html)
                    article_obj = Article(title=article_title, url=url, movie=movie_obj,
                                            domain=domain_obj, preface=preface, img_url=img_url)
                    article_obj.save()
                    new_article_count += 1
        return new_article_count

def run_daily_schedule(update_titles=True, update_feeds=True, update_images=True, fix_images=False):
    dsc = DailyScheduledCroller(MovieWalkerCroller, HatenabAPIController, ReadabilityExtractor, MovieImageScraper)
    if update_titles:
        new_titles_count = dsc.append_new_titles()
        print('{0} titles added.'.format(new_titles_count))
    if update_feeds:
        new_articles_count = dsc.append_new_feeds()
        print('{0} articles added.'.format(new_articles_count))
    if update_images:
        counts_of_new_images = dsc.update_images()
        print('{0} images updated.'.format(counts_of_new_images))
    if fix_images:
        counts_of_fixed_images = dsc.fix_images()
        print('{0} images fixed.'.format(counts_of_fixed_images))


if __name__ == '__main__':
    pass
