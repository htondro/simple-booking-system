from django.http import HttpResponseBadRequest
from .serializers import OwnerSerializer, ReservationSerializer, RoomSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Room, Reservation
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = OwnerSerializer

    @action(detail=True, methods=['get'])
    def reserved(self, request, pk=None):
        owner = self.get_object()

        reserved = Reservation.objects.filter(
            room__owner=owner).prefetch_related('room')
        reserved_rooms = Room.objects.filter(
            pk__in=reserved.values_list('room', flat=True))

        room_serializer = RoomSerializer(
            reserved_rooms, many=True)
        context = {
            'owner': {
                'id': owner.pk,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'username': owner.username,
            },
            'rooms': room_serializer.data,
        }
        return render(request, "realtybooking/reserved.html", context)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().prefetch_related('room')
    serializer_class = ReservationSerializer

    @action(detail=False, methods=['post'])
    def available(self, request, pk=None):
        certain_date = datetime.strptime(
            request.data.get('date'), "%Y-%m-%d").date()

        if certain_date < timezone.now().date():
            return HttpResponseBadRequest('Date cannot be in the past')

        else:
            reserved_rooms = Reservation.objects.filter(
                Q(start_date=certain_date) | Q(end_date=certain_date) | Q(
                    start_date__lte=certain_date, end_date__gte=certain_date)
            ).values_list('room', flat=True)

            available_rooms = Room.objects.exclude(pk__in=reserved_rooms)

            rooms_serializer = RoomSerializer(available_rooms, many=True)

            return Response(rooms_serializer.data)

    def create(self, request, *args, **kwargs):
        start_date = datetime.strptime(
            request.data.get('start_date'), "%Y-%m-%d").date()
        end_date = datetime.strptime(
            request.data.get('end_date'), "%Y-%m-%d").date()
        room = Room.objects.get(pk=request.data.get('room'))

        intersecting_reservations = Reservation.objects.filter(
            start_date__gte=start_date, end_date__gte=end_date, start_date__lte=end_date, room=room)

        including_reservations = Reservation.objects.filter(
            start_date__lte=start_date, end_date__gte=end_date, room=room)

        included_reservations = Reservation.objects.filter(
            start_date__gte=start_date, end_date__lte=end_date, room=room)

        if intersecting_reservations.count():
            return HttpResponseBadRequest(
                'This reservation intersecting another reservation. Reservations\' PKs: {pk}'.format(
                    pk=list(intersecting_reservations.values_list(
                        'pk', flat=True))
                )
            )

        elif including_reservations.count():
            return HttpResponseBadRequest(
                'Another reservation includes this reservation. Reservations\' PKs: {pk}'.format(
                    pk=list(including_reservations.values_list(
                        'pk', flat=True))
                )
            )

        elif included_reservations.count():
            return HttpResponseBadRequest(
                'This reservation includes another reservation. Reservations\' PKs: {pk}'.format(
                    pk=list(included_reservations.values_list(
                        'pk', flat=True))
                )
            )

        elif start_date < timezone.now().date():
            return HttpResponseBadRequest('Start date cannot be in the past')
        elif end_date < start_date:
            return HttpResponseBadRequest(
                'End date cannot be less than start date')
        else:
            return super().create(request, *args, **kwargs)
