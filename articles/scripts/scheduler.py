from articles.models import Article
from articles.scripts import feed
import time

def run_dayily_schedule(crollers):
    count = 0
    for croller in crollers:
        croller = croller()
        for title, url, preface, img_url in croller.feed():
            if Article.objects.filter(url=url).exists():
                continue
            article = Article(title=title, url=url, preface=preface, img_url=img_url)
            print(vars(article))
            article.save()
            count += 1
            time.sleep(10)
    print('{0} articles registered.'.format(count))

if __name__ == '__main__':
    run_dayily_schedule(feed.CROLLERS)
