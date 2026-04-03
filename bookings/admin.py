from django.contrib import admin
from .models import Booking, BookedSeat

admin.site.register(Booking)
admin.site.register(BookedSeat)