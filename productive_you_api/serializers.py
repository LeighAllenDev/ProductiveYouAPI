from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'content', 'image')

class CurrentUserSerializer(UserDetailsSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('pk', 'username', 'profile')
