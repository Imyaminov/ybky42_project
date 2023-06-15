from datetime import datetime
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from apps.room.models import (
    Room,
    Order
)


class RoomListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'type', 'capacity')


class AvailableRoomTimeSlotsSerializer(serializers.Serializer):
    start = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    end = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
