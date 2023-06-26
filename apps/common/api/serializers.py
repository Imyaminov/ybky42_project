from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.common.models import User


class ResidentModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=False, required=True)

    class Meta:
        model = User
        fields = ("name",)

    def validate_name(self, name):
        if len(name) < 5 or len(name) > 30:
            raise ValidationError('Name must be between 5 to  30  characters long')
        if name.isdigit():
            raise ValidationError('This name is entirely numeric')
        return name
