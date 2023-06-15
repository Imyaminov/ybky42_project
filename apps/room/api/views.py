import pytz
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from apps.room.api.serializers import (
    RoomListModelSerializer, AvailableRoomTimeSlotsSerializer,
)
from apps.room.paginations import RoomListPageNumberPagination
from apps.room.models import (
    Room,
    Order
)


class RoomListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListModelSerializer
    pagination_class = RoomListPageNumberPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('type',)

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return self.queryset.filter(name__icontains=query)
        return self.queryset


class RoomDetailAPIView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListModelSerializer


class RoomAvailabilityRetrieveAPIView(RetrieveAPIView):
    queryset = Room.objects.all()

    def retrieve(self, request, *args, **kwargs):
        date = self.request.data['date'] if self.request.data else datetime.now()

        if self.request.data:
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                data = {
                    'success': False,
                    'message': 'Invalid date format. Please provide date in the format year-month-day'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        start_time = date.replace(hour=9, minute=0, second=0, tzinfo=pytz.utc)
        end_time = date.replace(hour=18, minute=0, second=0, tzinfo=pytz.utc)

        room_orders = Order.objects.filter(
            start__year=date.year,
            start__day=date.day
        ).filter(room__id=self.kwargs['pk']).values('start', 'end').order_by("start")

        available_slots = []
        if room_orders:
            # time slots before first order
            if start_time < room_orders[0]['start']:
                available_slots.append({
                    'start': start_time,
                    'end': room_orders[0]['start']
                })
            # time slots between orders
            for idx in range(len(room_orders)-1):
                if room_orders[idx]['end'] < room_orders[idx+1]['start']:
                    available_slots.append({
                        'start': room_orders[idx]['end'],
                        'end': room_orders[idx+1]['start'],
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
        serializers = AvailableRoomTimeSlotsSerializer(data=available_slots, many=True)
        serializers.is_valid(raise_exception=True)
        return Response(data=serializers.data)
