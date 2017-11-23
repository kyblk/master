#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms



task_statuses = (
        ('new', 'Новая задача'),
        ('in_process', 'В процессе'),
        ('completed', 'Завершена'),
    )

class Statuses(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name=u'Название статуса')
    ended = models.BooleanField(verbose_name=u'Закрывает ли статус задачу?')
    sort = models.IntegerField(default=100, null=False, blank=False, verbose_name=u'Вес для сортировки')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['sort']
        verbose_name = 'statuses'
        verbose_name_plural = 'Статусы'


class Task(models.Model):
    author = models.ForeignKey('auth.User', related_name='creator')
    assigned_to = models.ForeignKey('auth.User', related_name='responsible')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    last_update_date = models.DateTimeField(
            default=timezone.now)
    status = models.ForeignKey('assignment_of_tasks.Statuses', on_delete=models.CASCADE)

    def __str__(self):
        return 'id:' + str(self.pk) + '_' + self.title

    class Meta:
        verbose_name = 'tasks'
        verbose_name_plural = 'Задачи'

class Comment(models.Model):
    yes_or_no = (
        ('Y', 'Изменить'),
        ('N', 'Не изменять'),
    )
    task = models.ForeignKey('assignment_of_tasks.Task', related_name='comments')
    author = models.ForeignKey('auth.User', related_name='participant')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    change_state = models.CharField(
                                        max_length=1,
                                        choices=yes_or_no,
                                        default='N'
                                     )
    old_assigned_to = models.ForeignKey('auth.User', related_name='old_responsible', null=True, blank = True)
    new_assigned_to = models.ForeignKey('auth.User', related_name='new_responsible', null=True, blank = True)
    old_status = models.CharField(
                                        max_length=20,
                                        #choices=task_statuses,
                                        null=True,
                                        blank=True
                                     )
    new_status = models.CharField(
                                        max_length=20,
                                        #choices=task_statuses,
                                        null=True,
                                        blank=True
                                     )



    def __str__(self):
        return 'id:' + str(self.pk) + '_' + self.text