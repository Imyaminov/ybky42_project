from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
)
from apps.room.paginations import RoomListPageNumberPagination
from apps.room.models import (
    Room, Order
)
from apps.room.api.serializers import (
    RoomListModelSerializer, AvailableRoomTimeSlotsSerializer, OrderRoomModelSerializer,
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

    def retrieve(self, request, *args, **kwargs):
        try:
            room = self.queryset.get(id=self.kwargs['pk'])
        except Room.DoesNotExist:
            return Response(
                data={"error": "topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(room)
        return Response(serializer.data)


class RoomAvailabilityAPIView(APIView):
    queryset = Room.objects.all()
    serializer_class = AvailableRoomTimeSlotsSerializer

    def get(self, request, *args, **kwargs):
        date = self.request.data.get('date', datetime.now())
        if not isinstance(date, datetime):
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return Response(
                    data={
                        'success': False,
                        'message': 'Invalid date format. Please provide date in the format year-month-day'
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        serializers = self.serializer_class(
            data=self.serializer_class.room_available_slots(room_id=self.kwargs['pk'], date=date),
            many=True
        )
        serializers.is_valid(raise_exception=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)


class OrderRoomCreateApiView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderRoomModelSerializer
