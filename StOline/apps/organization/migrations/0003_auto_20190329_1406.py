# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-29 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20190329_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='student',
            field=models.IntegerField(default=0, verbose_name='学习人数'),
        ),
    ]
