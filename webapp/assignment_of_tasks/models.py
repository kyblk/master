#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Statuses(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name=u'Название статуса')
    ended = models.BooleanField(verbose_name=u'Закрывает ли статус задачу?')
    sort = models.IntegerField(default=100, null=False, blank=False, verbose_name=u'Вес для сортировки')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['sort']
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Task(models.Model):
    author = models.ForeignKey('auth.User', related_name='creator', verbose_name=u'Автор')
    assigned_to = models.ForeignKey('auth.User', related_name='responsible', verbose_name=u'Назначена')
    title = models.CharField(max_length=200, verbose_name=u'Тема')
    text = models.TextField(verbose_name=u'Текст')
    created_date = models.DateTimeField(
            default=timezone.now, verbose_name=u'Дата создания')
    last_update_date = models.DateTimeField(
            default=timezone.now, verbose_name=u'Дата последней активности')
    status = models.ForeignKey('assignment_of_tasks.Statuses', on_delete=models.CASCADE, verbose_name=u'Статус')

    def __str__(self):
        return 'id:' + str(self.pk) + '_' + self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class Comment(models.Model):
    yes_or_no = (
        ('Y', 'Изменить'),
        ('N', 'Не изменять'),
    )
    task = models.ForeignKey('assignment_of_tasks.Task', related_name='comments', verbose_name=u'Комментарий к задаче:')
    author = models.ForeignKey('auth.User', related_name='participant', verbose_name=u'Автор')
    text = models.TextField(verbose_name=u'Текст')
    created_date = models.DateTimeField(default=timezone.now, verbose_name=u'Дата создания')

    change_state = models.CharField(
                                        max_length=1,
                                        choices=yes_or_no,
                                        default='N',
                                        verbose_name = u'Изменение параметров задачи'
                                     )
    old_assigned_to = models.ForeignKey('auth.User', related_name='old_responsible', null=True, blank = True, verbose_name = u'Переназначили с')
    new_assigned_to = models.ForeignKey('auth.User', related_name='new_responsible', null=True, blank = True, verbose_name = u'Переназначили на')
    old_status = models.CharField(
                                        max_length=20,
                                        null=True,
                                        blank=True,
                                        verbose_name=u'Статус изменился с'
                                     )
    new_status = models.CharField(
                                        max_length=20,
                                        null=True,
                                        blank=True,
                                        verbose_name=u'Статус изменился на'
                                     )



    def __str__(self):
        return 'id:' + str(self.pk) + '_' + self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'