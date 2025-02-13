from rest_framework import serializers
from .models import Task, TaskFile, Category
from teams.models import Team
from teams.serializers import TeamSerializer

class TaskFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = TaskFile
        fields = ['id', 'file', 'file_url', 'uploaded_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url) if request else f"{settings.MEDIA_URL}{obj.file}"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    task_files = TaskFileSerializer(many=True, read_only=True, source="files")
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True)

    class Meta:
        model = Task
        fields = [
            'id', 'task_name', 'description', 'is_urgent', 'completed',
            'due_date', 'category', 'task_files', 'team', 'owner'
        ]

    def to_representation(self, instance):
        """
        Override to_representation to serialize category and team using their 
        respective serializers.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')

        if request:
            if instance.category:
                representation['category'] = CategorySerializer(instance.category, context={'request': request}).data
            if instance.team:
                representation['team'] = TeamSerializer(instance.team, context={'request': request}).data
            if instance.files.exists():
                representation['files'] = TaskFileSerializer(instance.files.all(), many=True, context={'request': request}).data

        return representation

    def create(self, validated_data):
        user = self.context['request'].user
        files_data = self.context['request'].FILES.getlist('files') if self.context['request'].FILES else []
        validated_data.pop('owner', None)
        task = Task.objects.create(owner=user, **validated_data)

        for file_data in files_data:
            task_file = TaskFile.objects.create(file=file_data)
            task.files.add(task_file)

        return task

    def update(self, instance, validated_data):
        files_data = self.context['request'].FILES.getlist('files') if self.context['request'].FILES else []
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