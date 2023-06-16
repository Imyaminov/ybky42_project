from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.common.models import User


class ResidentModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=False, required=True)
    phone_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number')

    def validate_username(self, username):
        if len(username) < 5 or len(username) > 30:
            raise ValidationError('Username must be between 5 to  30  characters long')
        if username.isdigit():
            raise ValidationError('This username is entirely numeric')
        return username
