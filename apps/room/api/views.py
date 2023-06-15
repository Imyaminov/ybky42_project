from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView

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


class RoomAvailabilityAPIView(APIView):
    queryset = Room.objects.all()
    serializer_class = AvailableRoomTimeSlotsSerializer

    def get(self, request, *args, **kwargs):
        date_serializer = self.serializer_class(data=request.data)
        date_serializer.is_valid(raise_exception=True)
        date = date_serializer.validated_data.get('date', datetime.now())

        slots = self.serializer_class.room_available_slots(self.kwargs['pk'], date)

        serializers = self.serializer_class(data=slots, many=True)
        serializers.is_valid(raise_exception=True)
        return Response(data=serializers.data)
