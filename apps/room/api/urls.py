from django.urls import path
from .views import (
    RoomListAPIView,
    RoomDetailAPIView
)


urlpatterns = [
    path('api/rooms/', RoomListAPIView.as_view()),
    path('api/rooms/<int:pk>', RoomDetailAPIView.as_view())
]