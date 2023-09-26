from django.db import models
from django.conf import settings


# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=128, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'owner',)

    def __str__(self) -> str:
        return self.name


class Reservation(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['room', 'start_date'])
        ]

    def __str__(self) -> str:
        return "{room} - {start} - {end}".format(room=self.room.name, start=self.start_date.strftime('%Y %b %-d'), end=self.end_date.strftime('%Y %b %-d'))
