from django.db import models
from profiles.models import Profile


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(Profile, related_name='teams', blank=True)

    def __str__(self):
        return self.name
