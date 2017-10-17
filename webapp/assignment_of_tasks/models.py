from django.db import models
from django.utils import timezone
from django import forms

class Task(models.Model):
    task_statuses = (
        ('new', 'Новая задача'),
        ('in_process', 'В процессе'),
        ('completed', 'Завершена'),
    )

    author = models.ForeignKey('auth.User', related_name='creator')
    assigned_to = models.ForeignKey('auth.User', related_name='responsible')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    last_update_date = models.DateTimeField(
            default=timezone.now)
    status =  models.CharField(
                                        max_length=20,
                                        choices=task_statuses,
                                        default='new'
                                     )

    def __str__(self):
        return self.title


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


    def __str__(self):
        return self.text