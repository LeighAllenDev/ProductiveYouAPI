from django.db import models
from profiles.models import Profile


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(Profile, related_name='teams')

    def __str__(self):
        return self.name