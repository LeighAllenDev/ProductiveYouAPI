from rest_framework import serializers
from .models import Task, Category, TaskFile
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from teams.models import Team
from teams.serializers import TeamSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ['id', 'file', 'uploaded_at']

class TaskSerializer(serializers.ModelSerializer):
    assigned_profiles = ProfileSerializer(many=True, read_only=True)
    assigned_profiles_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Profile.objects.all(),
        source='assigned_profiles'
    )
    files = TaskFileSerializer(many=True, read_only=True)
    files_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=TaskFile.objects.all(),
        source='files', required=False
    )
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Team.objects.all(), source='team'
    )

    class Meta:
        model = Task
        fields = [
            'id', 'task_name', 'description', 'is_urgent', 'due_date',
            'category', 'assigned_profiles', 'assigned_profiles_ids',
            'files', 'files_ids', 'team', 'team_id'
        ]
