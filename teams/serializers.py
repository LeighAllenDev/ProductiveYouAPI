from rest_framework import serializers
from .models import Team
from profiles.models import Profile

class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Profile.objects.all(), write_only=True, source='members'
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'members', 'member_ids']