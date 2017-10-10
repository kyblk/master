from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Task

# Create your views here.
def post_list(request):
    tasks = Task.objects.all().order_by('-created_date')
    return render(request, 'tasks/post_list.html', {'tasks' : tasks})

def post_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})