from rest_framework.serializers import ModelSerializer
from apps.room.models import (
    Room,
    Order
)


class RoomListModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'type', 'capacity')
