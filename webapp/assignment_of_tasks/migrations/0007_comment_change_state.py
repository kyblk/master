# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_of_tasks', '0006_auto_20171016_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='change_state',
            field=models.BooleanField(default=False),
        ),
    ]