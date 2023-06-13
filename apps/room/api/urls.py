from django.urls import path
from .views import RoomListAPIView


urlpatterns = [
    path('api/rooms/', RoomListAPIView.as_view())
]