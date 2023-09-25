from tkinter import CASCADE
from django.db import models
from django.conf import settings
from datetime import timezone
from django.forms import ValidationError
# Create your models here.


def validate_start_date(value):
    if value < timezone.now().date():
        raise ValidationError("Start date cannot be in the past")


def validate_end_date(self, value):
    data = self.get_initial()
    if value < data.start_date:
        raise ValidationError('End date cannot be less than start date')


class Room(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Reservation(models.Model):
    start_date = models.DateTimeField(validators=[validate_start_date])
    end_date = models.DateTimeField(validators=[validate_end_date])
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{room} - {start} - {end}".format(room=self.room.name, start=self.start_date.strftime('%Y %b %-d - %-I %p'), end=self.end_date.strftime('%Y %b %-d - %-I %p'))
