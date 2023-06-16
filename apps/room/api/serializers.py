import pytz
from datetime import datetime, timedelta, time
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from apps.common.api.serializers import ResidentModelSerializer
from apps.common.models import User
from apps.room.models import (
    Room,
    Order,
    DATE_TIME_FORMAT
)


class RoomListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'type', 'capacity')


class AvailableRoomTimeSlotsSerializer(serializers.Serializer):
    start = serializers.DateTimeField(format=DATE_TIME_FORMAT)
    end = serializers.DateTimeField(format=DATE_TIME_FORMAT)

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


class DateField(serializers.Field):
    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, DATE_TIME_FORMAT)
        except ValueError:
            raise ValidationError({
                'success': False,
                'message': 'Invalid date format. Please provide date in the format "day-month-year hour:minute:second"'
            })

    def to_representation(self, value):
        return datetime.strftime(value, DATE_TIME_FORMAT)


class OrderRoomModelSerializer(serializers.ModelSerializer):
    resident = ResidentModelSerializer(required=True, many=False)
    start = DateField(required=True)
    end = DateField(required=True)

    class Meta():
        model = Order
        fields = ('resident', 'start', 'end')

    def create(self, validated_data):
        resident = self.validated_data.pop('resident')
        start, end = self.validated_data.pop('start'), self.validated_data.pop('end')
        self.check_availability(start, end)

        room = get_object_or_404(Room, pk=self.context['view'].kwargs.get('pk'))
        user = User.objects.get_or_create(username=resident['username'], phone_number=resident['phone_number'])

        order = Order.objects.create(resident=user[0], room=room, is_active=True, start=start, end=end)
        return order

    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')

        if start >= end:
            data = {
                'success': False,
                'message': 'start date cannot be greater or equal to end date'
            }
        elif start.hour < time(hour=9).hour or start.hour > time(hour=18).hour:
            data = {
                'success': False,
                'message': 'starting time must be between 9 am to 18 pm'
            }
        elif end.hour < time(hour=9).hour or end.hour > time(hour=18).hour:
            data = {
                'success': False,
                'message': 'end time must be between 9 am to 18 pm'
            }
        elif start < datetime.now() + timedelta(hours=1):
            data = {
                'success': False,
                'message': 'starting date and time must be at least one hour later from current time'
            }
        else:
            return attrs
        raise ValidationError(data)

    @staticmethod
    def check_availability(start, end):
        query = (
                (Q(start__lte=start) & Q(end__gte=start)) |
                (Q(start__lte=end) & Q(end__gte=end))
        )
        if Order.objects.filter(query).exists():
            raise ValidationError({
                'success': False,
                'message': 'The room is booked for the given time'
            })
