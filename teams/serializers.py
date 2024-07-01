from rest_framework import serializers
from .models import Team
from profiles.models import Profile

class TeamSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'users']
