from django.urls import path
from .views import (
    RoomListAPIView,
    RoomDetailAPIView,
    RoomAvailabilityRetrieveAPIView
)


urlpatterns = [
    path('api/rooms/', RoomListAPIView.as_view()),
    path('api/rooms/<int:pk>', RoomDetailAPIView.as_view()),
    path('api/rooms/<int:pk>/availability', RoomAvailabilityRetrieveAPIView.as_view()),
]