from rest_framework import serializers
from .models import Team
from profiles.models import Profile
from profiles.serializers import ProfileSerializer

class TeamSerializer(serializers.ModelSerializer):
    users = ProfileSerializer(many=True, read_only=True)
    user_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Profile.objects.all(), write_only=True, source='users'
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'users', 'user_ids']
