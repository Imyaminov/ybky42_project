from django.db import models
from apps.common.models import User
from helpers.models import TimeStampedModel

FOCUS, TEAM, CONFERENCE = (
    'focus',
    'team',
    'conference'
)


class Room(TimeStampedModel):
    ROOM_TYPES = (
        (FOCUS, FOCUS),
        (TEAM, TEAM),
        (CONFERENCE, CONFERENCE),
    )

    name = models.CharField(verbose_name='Room Name', max_length=256)
    type = models.CharField(verbose_name='Room Type', max_length=10, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    resident = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)

    start = models.DateTimeField()
    end = models.DateTimeField()

