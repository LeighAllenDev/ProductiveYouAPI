from rest_framework import serializers
from .models import Task, TaskFile, Category
from profiles.serializers import ProfileSerializer  # Import ProfileSerializer if needed
from teams.serializers import TeamSerializer  # Import TeamSerializer from your teams app


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ['id', 'file', 'uploaded_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    files = TaskFileSerializer(many=True, read_only=True)
    assigned_profiles = ProfileSerializer(many=True, read_only=True)
    team = TeamSerializer(read_only=True) 

    class Meta:
        model = Task
        fields = [
            'id', 'task_name', 'description', 'is_urgent', 'completed',
            'due_date', 'category', 'assigned_profiles', 'files', 'team'
        ]
