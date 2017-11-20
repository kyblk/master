from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.task_list, name='task_list'),
    url(r'^my_tasks/$', views.my_task_list, name='my_task_list'),
    url(r'^completed_tasks/$', views.completed_task_list, name='completed_task_list'),
    url(r'^task/(?P<pk>\d+)/$', views.task_detail, name='task_detail'),
    url(r'^task/new/$', views.task_new, name='task_new'),
    url(r'^task/(?P<pk>\d+)/edit/$', views.task_edit, name='task_edit'),
    url(r'^task/(?P<pk>\d+)/remove/$', views.task_remove, name='task_remove'),
    url(r'^task/(?P<pk>\d+)/comment/$', views.add_comment_to_task, name='add_comment_to_task'),
    url(r'^task/(?P<pk_task>\d+)/comment/(?P<pk_com>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^create_user/$', views.create_user, name='create_user'),



    url(r'^rest-api/task_list$', views.task_list_api, name='task_list_api'),
    url(r'^rest-api/task/(?P<pk>\d+)/$', views.task_detail_api, name='task_detail_api'),
]