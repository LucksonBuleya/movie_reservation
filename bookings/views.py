from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Booking
from .serializer import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    Handles all booking operations:
    - Create booking
    - View bookings
    - Cancel booking (custom endpoint)
    """

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Users should ONLY SEE THEIR bookings
        """
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically attach logged-in user to booking
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Custom endpoint to cancel a booking
        URL: /api/bookings/bookings/{id}/cancel/
        """

        booking = self.get_object()

        # Already cancelled
        if booking.status == 'CANCELLED':
            return Response(
                {"error": "Booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cannot cancel after showtime starts
        if booking.showtime.start_time <= timezone.now():
            return Response(
                {"error": "Cannot cancel after the showtime has started."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Cancel booking
        booking.status = 'CANCELLED'
        booking.save()

        return Response({"message": "Booking cancelled successfully."})