from django.db import models
from teams.models import Team

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TaskFile(models.Model):
    file = models.FileField(upload_to='task_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File: {self.file.name}"

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    description = models.TextField()
    is_urgent = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    due_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    files = models.ManyToManyField(TaskFile, related_name='tasks', blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return f"#{self.id} - Task: {self.task_name} | Urgent: {self.is_urgent}"
