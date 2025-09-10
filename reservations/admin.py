from django.contrib import admin

from reservations.models import Reservation


# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'email', 'people', 'start_date', 'end_date', 'status', 'notes', 'created_at')
    list_filter = ('name', 'surname', 'phone', 'email', 'people', 'start_date', 'end_date', 'status', 'notes', 'created_at')
    search_fields = ('name', 'surname', 'phone', 'email', 'people', 'start_date', 'end_date', 'status', 'notes', 'created_at')
    ordering = ('-created_at',)

