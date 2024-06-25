# In your serializers.py
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.models import User

class CurrentUserSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
