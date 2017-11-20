#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task, Comment
from .forms import TaskForm, CommentForm, UpdateTask, UserForm

'''
API
'''
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import TaskShortSerializer, TaskDetailSerializer, CommentDetailSerializer
from rest_framework import serializers
import simplejson
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
            if comment.change_state == 'Y':
                updating_task(pk,request.user,upd_task.assigned_to,upd_task.status,comment.text)
            else:
                comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        c_form = CommentForm()
        u_task = UpdateTask(instance=task)
    return render(request, 'tasks/add_comment_to_task.html', {'c_form': c_form, 'upd_task': u_task})

def updating_task (pk,author,assigned_to,status,text):
    task = get_object_or_404(Task, pk=pk)
    comment = Comment()
    task.assigned_to = assigned_to
    task.status = status
    comment.task = task
    comment.author = author
    change_text = '<p><em><font size="2">Назначена на <b>%s</b> статус <b>[%s]</b> </b></em></p>' % (task.assigned_to.get_full_name(), task.get_status_display())
    comment.text = change_text + text
    comment.save()
    task.save(update_fields=['status', 'assigned_to',])

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

    '''elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)'''
    serializer = TaskShortSerializer()
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def task_detail_api(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        task = Task.objects.get(pk=pk)
        comments = Comment.objects.filter(task=task)
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer_task = TaskDetailSerializer(task)

        serializer_comment = CommentDetailSerializer(comments, many=True)
        serializer_comment = serializer_comment.data[:]

        #return JsonResponse(serializer_comment, safe=False)
        return  JsonResponse(serializer_task.data, safe=False)
    return 0