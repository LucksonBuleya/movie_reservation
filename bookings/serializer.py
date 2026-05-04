from rest_framework import serializers
from .models import Booking, BookedSeat
from movies.models import Showtime
from theaters.models import Seat


class BookingSerializer(serializers.ModelSerializer):
    # Accepts a list of seat IDs from the client (write-only)
    seats = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Booking
        # total_price is computed automatically, not provided by user
        fields = ['id', 'showtime', 'seats', 'total_price', 'status', 'created_at']
        read_only_fields = ['total_price', 'status', 'created_at']

    def validate(self, data):
        """
        Custom validation to ensure:
        1. Seats belong to the correct theater
        2. Seats are not already booked for this showtime
        """
        showtime = data['showtime']
        seat_ids = data['seats']

        # Get all valid seats for the selected showtime's theater
        valid_seats = Seat.objects.filter(theater=showtime.theater)

        # Ensure each selected seat exists in this theater
        for seat_id in seat_ids:
            if not valid_seats.filter(id=seat_id).exists():
                raise serializers.ValidationError(
                    f"Seat {seat_id} does not belong to this theater."
                )

        # Check if any of the selected seats are already booked
        already_booked = BookedSeat.objects.filter(
            showtime=showtime,
            seat_id__in=seat_ids
        ).values_list('seat_id', flat=True)

        if already_booked:
            raise serializers.ValidationError(
                f"Seats already booked: {list(already_booked)}"
            )

        return data

    def create(self, validated_data):
        """
        Handles booking creation:
        - Calculates total price
        - Creates booking record
        - Creates associated booked seats
        """
        # Extract seat IDs from request data
        seat_ids = validated_data.pop('seats')
        showtime = validated_data['showtime']

        # Get currently authenticated user
        user = self.context['request'].user

        # Business Logic: Calculate total price automatically
        price_per_seat = showtime.price
        total_price = len(seat_ids) * price_per_seat

        # Create booking record
        booking = Booking.objects.create(
            user=user,
            showtime=showtime,
            total_price=total_price
        )

        # Create a BookedSeat entry for each selected seat
        for seat_id in seat_ids:
            BookedSeat.objects.create(
                booking=booking,
                seat_id=seat_id,
                showtime=showtime
            )

        return booking