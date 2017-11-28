#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

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
    percent_value = (
        (0, 0),
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (60, 60),
        (70, 70),
        (80, 80),
        (90, 90),
        (100, 100),
    )
    author = models.ForeignKey('auth.User', related_name='creator', verbose_name=u'Автор')
    assigned_to = models.ForeignKey('auth.User', related_name='responsible', verbose_name=u'Назначена')
    title = models.CharField(max_length=200, verbose_name=u'Тема')
    text = models.TextField(verbose_name=u'Текст')
    created_date = models.DateTimeField(
            default=timezone.now, verbose_name=u'Дата создания')
    last_update_date = models.DateTimeField(
            default=timezone.now, verbose_name=u'Дата последней активности')
    status = models.ForeignKey('assignment_of_tasks.Statuses', on_delete=models.CASCADE, verbose_name=u'Статус')
    percent = models.IntegerField(
        default=0,
        choices=percent_value,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        verbose_name=u'Процент выполнения'
    )

    def __str__(self):
        return 'id:' + str(self.pk) + '  ' + self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class Comment(models.Model):
    task = models.ForeignKey('assignment_of_tasks.Task', related_name='comments', verbose_name=u'Комментарий к задаче:')
    author = models.ForeignKey('auth.User', related_name='participant', verbose_name=u'Автор')
    text = models.TextField(verbose_name=u'Текст')
    created_date = models.DateTimeField(default=timezone.now, verbose_name=u'Дата создания')
    change_state = models.BooleanField(verbose_name = u'Изменение параметров задачи')
    change_values = models.ForeignKey('assignment_of_tasks.History_changed', on_delete=models.CASCADE, null=True, blank=True, related_name='history', verbose_name=u'Какие изменения сделал этот комментарий')


    def __str__(self):
        return 'id:' + str(self.pk)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class History_changed(models.Model):
    old_assigned_to = models.CharField(
                                        max_length=200,
                                        null=True,
                                        blank=True,
                                        verbose_name = u'Переназначили с',
                                     )
    new_assigned_to = models.CharField(
                                        max_length=200,
                                        null=True,
                                        blank=True,
                                        verbose_name = u'Переназначили на',
                                     )
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
    old_percent = models.IntegerField(
                                        null=True,
                                        blank=True,
                                        verbose_name=u'Процент выполнения изменен с'
    )
    new_percent = models.IntegerField(
                                        null=True,
                                        blank=True,
                                        verbose_name=u'Процент выполнения изменен на'
    )

    def __str__(self):
        return 'id: ' + str(self.pk)

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'История'