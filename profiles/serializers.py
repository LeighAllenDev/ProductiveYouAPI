from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')  # Add this field to get owner's username
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'owner_username', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner'
        ]
