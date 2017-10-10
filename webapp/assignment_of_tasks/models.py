from django.db import models
from django.utils import timezone

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


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
# Create your models here.
