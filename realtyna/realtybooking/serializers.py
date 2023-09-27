from rest_framework import serializers
from .models import Room, Reservation
from django.contrib.auth.models import User


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['pk', 'owner', 'name', 'reservations']

    reservations = serializers.SerializerMethodField()

    def get_reservations(self, obj):
        reserved = Reservation.objects.filter(
            room=obj.pk).prefetch_related('room')
        return ReservationSerializer(reserved, many=True).data


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name']
