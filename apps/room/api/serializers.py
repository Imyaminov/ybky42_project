import pytz
from datetime import datetime
from rest_framework import serializers
from apps.room.models import (
    Room,
    Order
)


class RoomListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'type', 'capacity')


class DateField(serializers.Field):
    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            raise serializers.ValidationError(
                'Invalid date format. Please provide date in the format year-month-day'
            )

    def to_representation(self, value):
        return value.strftime("%Y-%m-%d")


class AvailableRoomTimeSlotsSerializer(serializers.Serializer):
    start = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False)
    end = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False)

    def __init__(self, *args, **kwargs):
        super(AvailableRoomTimeSlotsSerializer, self).__init__(*args, **kwargs)
        self.fields['date'] = DateField(required=False)

    @staticmethod
    def room_available_slots(room_id, date):
        start_time = date.replace(hour=9, minute=0, second=0, tzinfo=pytz.utc)
        end_time = date.replace(hour=18, minute=0, second=0, tzinfo=pytz.utc)

        room_orders = Order.objects.filter(
            start__year=date.year,
            start__day=date.day
        ).filter(room__id=room_id).values('start', 'end').order_by("start")

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
