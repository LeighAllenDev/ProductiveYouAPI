from rest_framework import serializers
from .models import Task, TaskFile, Category
from profiles.serializers import ProfileSerializer
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
    assigned_profiles = ProfileSerializer(many=True, read_only=True, context={'request': serializers.CurrentUserDefault()})
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'task_name', 'description', 'is_urgent', 'completed',
            'due_date', 'category', 'assigned_profiles', 'files', 'team', 'owner'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            # Serialize assigned profiles using ProfileSerializer
            representation['assigned_profiles'] = ProfileSerializer(
                instance.assigned_profiles.all(), many=True, context={'request': request}
            ).data
            # Serialize team using TeamSerializer
            if instance.team:
                representation['team'] = TeamSerializer(instance.team, context={'request': request}).data
        return representation

    def create(self, validated_data):
        user = self.context['request'].user  # Get the current user from context
        files_data = self.context['request'].FILES.getlist('files')  # Get files from request
        task = Task.objects.create(owner=user, **validated_data)  # Create task with owner
        for file_data in files_data:
            TaskFile.objects.create(task=task, file=file_data)  # Add files to task
        return task

    def update(self, instance, validated_data):
        files_data = self.context['request'].FILES.getlist('files')  # Get files from request
        instance.task_name = validated_data.get('task_name', instance.task_name)
        instance.description = validated_data.get('description', instance.description)
        instance.is_urgent = validated_data.get('is_urgent', instance.is_urgent)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        existing_files = {file.id: file for file in instance.files.all()}
        for file_data in files_data:
            file_id = file_data.get('id')
            if file_id in existing_files:
                existing_file = existing_files.pop(file_id)
                existing_file.file = file_data.get('file', existing_file.file)
                existing_file.save()
            else:
                TaskFile.objects.create(task=instance, file=file_data)
        for file in existing_files.values():
            file.delete()
        return instance
