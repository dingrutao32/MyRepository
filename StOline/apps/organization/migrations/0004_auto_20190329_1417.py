# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-29 14:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20190329_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='student',
            new_name='students',
        ),
    ]
