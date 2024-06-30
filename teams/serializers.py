from rest_framework import serializers
from .models import Team
from profiles.models import Profile

class TeamSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), write_only=True, source='users')

    class Meta:
        model = Team
        fields = ['id', 'name', 'users']
