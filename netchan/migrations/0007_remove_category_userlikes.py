# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 18:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netchan', '0006_auto_20161207_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='userLikes',
        ),
    ]