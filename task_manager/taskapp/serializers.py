from rest_framework import serializers
from .models import Task, TaskLogger


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('task_name', 'task_description', 'created_at', 'task_status', 'task_finished_date')


class TaskFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('task_status', 'task_finished_date')


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('task_name', 'task_description', 'task_status', 'task_finished_date')


class ChangeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('task_name',)
