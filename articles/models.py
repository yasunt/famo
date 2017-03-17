from django.db import models
from accounts.models import FamoUser

class Article(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(default='', max_length=100)
    url = models.URLField(default='')
    preface = models.CharField(default='', max_length=300)
    img_url = models.URLField(null=True)
    hits = models.IntegerField(default=0)
    registered_date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.CharField(default=0, max_length=500)
    user = models.ForeignKey(FamoUser)
    good_rators = models.ManyToManyField(FamoUser, related_name='comments')
    article = models.ForeignKey(Article)
