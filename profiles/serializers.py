from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        return request.user == obj.owner

    def update(self, instance, validated_data):
        validated_data.pop('owner', None)  # Ensure owner is not updated
        return super().update(instance, validated_data)

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'username'
        ]
        read_only_fields = ['owner']
