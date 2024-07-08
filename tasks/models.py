from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
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
    task_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    is_urgent = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    due_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    assigned_profiles = models.ManyToManyField(Profile, related_name='tasks', blank=True)
    files = models.ManyToManyField(TaskFile, related_name='tasks', blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', default=1)

    def __str__(self):
        return f"#{self.id} - Task: {self.task_name} | Urgent: {self.is_urgent}"

    def save(self, *args, **kwargs):
        if not self.owner_id:
            # Set owner to current user if not already set
            self.owner = kwargs.pop('user', None)
        super(Task, self).save(*args, **kwargs)
