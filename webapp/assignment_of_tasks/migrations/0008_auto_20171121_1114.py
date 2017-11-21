# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 08:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment_of_tasks', '0007_comment_change_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='new_assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_responsible', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='new_status',
            field=models.CharField(choices=[('new', 'Новая задача'), ('in_process', 'В процессе'), ('completed', 'Завершена')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='old_assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='old_responsible', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='old_status',
            field=models.CharField(choices=[('new', 'Новая задача'), ('in_process', 'В процессе'), ('completed', 'Завершена')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='change_state',
            field=models.CharField(choices=[('Y', 'Изменить'), ('N', 'Не изменять')], default='N', max_length=1),
        ),
    ]
