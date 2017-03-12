# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 03:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(null=True)),
                ('sex', models.IntegerField(null=True)),
                ('job', models.IntegerField(null=True)),
                ('relation', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='famouser',
            name='birth_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='famouser',
            name='introduction',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='famouser',
            name='job',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='famouser',
            name='registered_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='famouser',
            name='sex',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
