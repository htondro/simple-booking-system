from django.contrib import admin
from .models import Room, Reservation
# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('pk', 'name', 'owner')
    search_fields = ('owner__username', 'owner__first_name',
                     'owner__last_name', 'owner__email')
    ordering = ('pk', 'name', 'owner')


admin.site.register(Room, RoomAdmin)


class ReservationAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('pk', 'room', 'start_date', 'end_date')
    search_fields = ('room__name', 'owner__username', 'owner__first_name',
                     'owner__last_name', 'owner__email', 'start_date', 'end_date')
    ordering = ('-start_date', 'end_date', 'room__name')


admin.site.register(Reservation, ReservationAdmin)
