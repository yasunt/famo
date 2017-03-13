from django.db import models
from django.contrib.auth.models import AbstractUser

sex = {'female': 0, 'male': 1, 'other': 2}
relation = {'child': 11, 'husband': 12, 'wife': 13, 'lover': 14}

class FamoUser(AbstractUser):
    birth_date = models.DateField(null=True)
    registered_date = models.DateField(auto_now_add=True, null=True)
    sex = models.IntegerField(null=True)    # add a limit_choices_to
    job = models.IntegerField(null=True)    # add a limit_choices_to
    introduction = models.TextField(default='')
    follows = models.ManyToManyField('self', symmetrical=None)

class Person(models.Model):
    birth_date = models.DateField(null=True)
    sex = models.IntegerField(null=True)
    job = models.IntegerField(null=True)
    family = models.ForeignKey(FamoUser)
    relation = models.IntegerField(default=0)   # add a limit_choices_to
