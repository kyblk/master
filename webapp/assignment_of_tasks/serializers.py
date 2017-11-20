from rest_framework import serializers
from .models import Task, Comment
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TaskShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'author', 'assigned_to', 'title', 'created_date', 'status')

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'author', 'assigned_to', 'title', 'text', 'created_date', 'status')

class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_date')



    '''def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance'''