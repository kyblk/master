from django.shortcuts import render
from django.utils import timezone
from .models import Task

# Create your views here.
def post_list(request):
    tasks = Task.objects.all().order_by('-created_date')
    return render(request, 'tasks/post_list.html', {'tasks' : tasks})