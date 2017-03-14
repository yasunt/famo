from django.db import models
from accounts.models import FamoUser


class Post(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(FamoUser)
    hits = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Question(Post):
    pass

class Answer(Post):
    question = models.ForeignKey(Question)
    value = models.IntegerField(default=0)

class Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=10)
    posts = models.ManyToManyField(Question)
