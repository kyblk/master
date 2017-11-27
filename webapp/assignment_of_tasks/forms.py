from django import forms
from django.contrib.auth.models import User
from .models import Task, Comment
from django.utils.encoding import smart_text
from django.shortcuts import redirect
from django.forms import ModelChoiceField, ModelMultipleChoiceField

class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())

class TaskForm(forms.ModelForm):
    assigned_to = UserFullnameChoiceField(queryset=User.objects.all())
    class Meta:
        model = Task
        fields = ('assigned_to', 'title', 'text', 'status')

    '''
    Изменяем английское название assigned_to. Т.к. поле переопределено, оно не берет русское название из модели
    '''

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].label = 'Назначить задачу на:'

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text','change_state')

class UpdateTask(forms.ModelForm):
    assigned_to = UserFullnameChoiceField(queryset=User.objects.all())
    class Meta:
        model = Task
        fields = ('assigned_to','status')

    def __init__(self, *args, **kwargs):
        super(UpdateTask, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].label = 'Назначить задачу на:'

    '''
    Сортировка статусов в форме по весу
    upd: сортируется модель, данная функция не нужна
    
    def __init__(self, *args, **kwargs):
        super(UpdateTask, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = self.fields['status'].queryset.order_by('sort')

    '''


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password'].label = 'Пароль:'
        self.fields['is_staff'].label = 'Администратор'
        self.fields['is_superuser'].widget = forms.HiddenInput()


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', )

    def __init__(self, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].help_text = None


