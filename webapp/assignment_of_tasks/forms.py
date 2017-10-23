from django import forms
from django.contrib.auth.models import User
from .models import Task, Comment
from django.utils.encoding import smart_text
from django.forms import ModelChoiceField, ModelMultipleChoiceField

class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())

class TaskForm(forms.ModelForm):
    assigned_to = UserFullnameChoiceField(queryset=User.objects.all())
    class Meta:
        model = Task
        fields = ('assigned_to', 'title', 'text', 'status')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text','change_state')

class UpdateTask(forms.ModelForm):
    assigned_to = UserFullnameChoiceField(queryset=User.objects.all())
    class Meta:
        model = Task
        fields = ('assigned_to','status')

