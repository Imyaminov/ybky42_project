import pytz
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

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

    @staticmethod
    def room_available_slots(room_id, date):
        room = get_object_or_404(Room, pk=room_id)
        room_orders = Order.objects.filter(
            start__year=date.year,
            start__day=date.day
        ).filter(room=room).values('start', 'end').order_by("start")

        start_time = date.replace(hour=9, minute=0, second=0, tzinfo=pytz.utc)
        end_time = date.replace(hour=18, minute=0, second=0, tzinfo=pytz.utc)

        available_slots = []
        if room_orders:
            # time slots before first order
            if start_time < room_orders[0]['start']:
                available_slots.append({
                    'start': start_time,
                    'end': room_orders[0]['start']
                })
            # time slots between orders
            for idx in range(len(room_orders) - 1):
                if room_orders[idx]['end'] < room_orders[idx + 1]['start']:
                    available_slots.append({
                        'start': room_orders[idx]['end'],
                        'end': room_orders[idx + 1]['start'],
                    })
            # time slots after last order
            if end_time > room_orders.last()['end']:
                available_slots.append({
                    'start': room_orders.last()['end'],
                    'end': end_time,
                })
        else:
            available_slots.append({
                'start': start_time,
                'end': end_time
            })

        return available_slots
