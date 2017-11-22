from rest_framework import serializers
from .models import Task, Comment, task_statuses
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name')

class TaskShortSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ('id', 'author', 'assigned_to', 'title', 'created_date', 'last_update_date', 'status')

class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_date', 'change_state', 'old_assigned_to', 'new_assigned_to', 'old_status', 'new_status')

class TaskDetailSerializer(serializers.ModelSerializer):
    comments = CommentDetailSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ('id', 'author', 'assigned_to', 'title', 'text', 'created_date', 'status', 'comments')
