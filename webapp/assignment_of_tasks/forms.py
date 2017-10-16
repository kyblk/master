from django import forms

from .models import Task, Comment

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('assigned_to' ,'title', 'text', 'status')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)