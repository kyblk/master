from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.task_list, name='task_list'),
    url(r'^task/(?P<pk>\d+)/$', views.task_detail, name='task_detail'),
    url(r'^task/new/$', views.task_new, name='task_new'),
    url(r'^task/(?P<pk>\d+)/edit/$', views.task_edit, name='task_edit'),
    url(r'^task/(?P<pk>\d+)/remove/$', views.task_remove, name='task_remove'),
    url(r'^task/(?P<pk>\d+)/comment/$', views.add_comment_to_task, name='add_comment_to_task'),
]