from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from apps.room.api.serializers import RoomListModelSerializer
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
