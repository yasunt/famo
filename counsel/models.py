from django.db import models
from datetime import datetime
from accounts.models import FamoUser


class Post(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(FamoUser)
    updated_date = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)
    class Meta:
        abstract = True

class Question(Post):
    hits = models.IntegerField(default=0)
    last_accessed_date = models.DateTimeField(default=datetime.now())

class Answer(Post):
    def get_good_points(self):
        pass
    question = models.ForeignKey(Question)
    good_rators = models.ManyToManyField(FamoUser, related_name='good_answers')
    bad_rators = models.ManyToManyField(FamoUser, related_name='bad_anwers')

class Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=10)
    posts = models.ManyToManyField(Question)
