#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task, Comment, task_statuses
from .forms import TaskForm, CommentForm, UpdateTask, UserForm
import simplejson
'''
API
'''
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import TaskShortSerializer, TaskDetailSerializer, CommentDetailSerializer
from rest_framework import serializers
import json
'''
'''

def task_list(request):
    tasks = Task.objects.all().order_by('-created_date')
    return render(request, 'tasks/task_list.html', {'tasks' : tasks})

@login_required
def my_task_list(request):
    tasks = Task.objects.all().order_by('-created_date')
    return render(request, 'tasks/my_task_list.html', {'tasks' : tasks})

@login_required
def completed_task_list(request):
    tasks = Task.objects.all().order_by('-created_date')
    return render(request, 'tasks/completed_task_list.html', {'tasks' : tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_new(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.created_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_edit.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.created_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form})

@login_required
def task_remove(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')

@login_required
def add_comment_to_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        c_form = CommentForm(request.POST)
        u_task = UpdateTask(request.POST, instance=task)
        if c_form.is_valid():
            comment = c_form.save(commit=False)
            upd_task = u_task.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.created_date = timezone.now()
            if comment.change_state == 'Y':
                updating_task(pk,request.user,upd_task.assigned_to,upd_task.status,comment.text)
            else:
                comment.save()
                task.last_update_date = timezone.now()
                task.save(update_fields=['last_update_date'])
            return redirect('task_detail', pk=task.pk)
    else:
        c_form = CommentForm()
        u_task = UpdateTask(instance=task)
    return render(request, 'tasks/add_comment_to_task.html', {'c_form': c_form, 'upd_task': u_task})

def updating_task (pk,author,assigned_to,status,text):
    task = get_object_or_404(Task, pk=pk)
    comment = Comment()
    #Пишем историю в поля коммента.
    comment.change_state = "Y"
    comment.old_assigned_to = task.assigned_to
    comment.new_assigned_to = assigned_to
    comment.old_status = task.status
    comment.new_status = status
    ###
    task.assigned_to = assigned_to
    task.status = status
    task.last_update_date = timezone.now()
    comment.task = task
    comment.author = author
    #change_text = '<p><em><font size="2">Назначена на <b>%s</b> статус <b>[%s]</b> </b></em></p>' % (task.assigned_to.get_full_name(), task.get_status_display())
    comment.text = text
    comment.save()
    task.save(update_fields=['status', 'assigned_to','last_update_date'])

@login_required
def comment_remove(request, pk_task, pk_com):
    comment = get_object_or_404(Comment, pk=pk_com)
    if comment.author == request.user:
        comment.delete()
    return redirect('task_detail', pk=pk_task)

@login_required
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            # redirect, or however you want to get to the main view
            return redirect('task_list')
    else:
        form = UserForm()

    return render(request, 'tasks/create_user.html', {'form': form})

'''
API methods
'''
@csrf_exempt
def task_list_api(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskShortSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    serializer = TaskShortSerializer()
    return JsonResponse(serializer.errors, status=400)

@login_required
def my_task_list_api(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskShortSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    serializer = TaskShortSerializer()
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def task_detail_api(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'not found'})

    if request.method == 'GET':
        json_task_detail = TaskDetailSerializer(task)
        return JsonResponse(json_task_detail.data)


'''
            import requests
            import json
            a = requests.post("http://127.0.0.1:8000/api/login/", data={"username": "testapi", "password": "111"})
            c = a.cookies
            r = requests.post("http://127.0.0.1:8000/api/task/18/comment/", 
            data=json.dumps({'text' : "111" , 'change_state': "N", "assigned_to": "mech", "status" : "in_process"}), cookies=secure_cookie)
'''
@csrf_exempt
def add_comment_to_task_api(request, pk):
    if request.method == 'POST':
        json_string = request.body.decode()
        json_string = json.loads(json_string)
        comment = CommentForm(json_string)
        if comment.is_valid():
            task = get_object_or_404(Task, pk=pk)
            comment = comment.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.created_date = timezone.now()
            if json_string["change_state"] == "Y":
                assigned_to = get_object_or_404(User, username=json_string["assigned_to"])
                status = json_string["status"]
                updating_task(pk, request.user, assigned_to, status, comment.text)
                print('Added comment with update')
            else:
                comment.save()
                task.last_update_date = timezone.now()
                task.save(update_fields=['last_update_date'])
                print('Added comment without update')
        else:
            print('Not valid comment')
        return HttpResponse()

'''
Не разобрался как серилизовать not model object - Tuple (task_statuses), чтобы в json отдавался сразу русское название статуса
Поэтому статусы (значение на русском языке) мы будем получать с сервера отдельным запросом
'''
@csrf_exempt
def get_statuses(request):
    if request.method == 'GET':
        dictionary = simplejson.dumps(task_statuses)
        return JsonResponse(dictionary, safe=False)