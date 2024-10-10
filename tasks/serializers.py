from rest_framework import serializers
from .models import Task, TaskFile, Category
from teams.models import Team
from teams.serializers import TeamSerializer

class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ['id', 'file', 'uploaded_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    files = TaskFileSerializer(many=True, read_only=True)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Task
        fields = [
            'id', 'task_name', 'description', 'is_urgent', 'completed',
            'due_date', 'category', 'files', 'team', 'owner'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            if instance.team:
                representation['team'] = TeamSerializer(instance.team, context={'request': request}).data
            if instance.files:
                representation['files'] = TaskFileSerializer(instance.files.all(), many=True, context={'request': request}).data
        return representation

    def create(self, validated_data):
        user = self.context['request'].user
        files_data = self.context['request'].FILES.getlist('files')
        validated_data.pop('owner', None)
        task = Task.objects.create(owner=user, **validated_data)

        for file_data in files_data:
            task_file = TaskFile.objects.create(file=file_data)
            task.files.add(task_file)

        return task

    def update(self, instance, validated_data):
        files_data = self.context['request'].FILES.getlist('files')
        instance.task_name = validated_data.get('task_name', instance.task_name)
        instance.description = validated_data.get('description', instance.description)
        instance.is_urgent = validated_data.get('is_urgent', instance.is_urgent)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.category = validated_data.get('category', instance.category)
        instance.team = validated_data.get('team', instance.team)
        instance.save()

        for file_data in files_data:
            task_file = TaskFile.objects.create(file=file_data)
            instance.files.add(task_file)

        return instance
