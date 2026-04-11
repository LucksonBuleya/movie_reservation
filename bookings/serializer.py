from rest_framework import serializers
from .models import BookedSeat, Booking
from theaters.models import Seat
from movies.models import Showtime

class BookingSerializer(serializers.ModelSerializer):
    # User will send a list of seat IDs
    seats = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'showtime', 'seats', 'total_price', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate(self, data):
        """
        This runs BEFORE creating the booking.
        Used to check if seats are already taken.
        """

        showtime = data['showtime']
        seat_ids = data['seats']

        # Get all seats from DB
        seats = Seat.objects.filter(id__in=seat_ids)

        # Check if all seats exist
        if len(seats) != len(seat_ids):
            raise serializers.ValidationError("One or more seats do not exist.")
        
        # Check if any seat is already booked for this showtime (CORE LOGIC)
        for seat in seats:
            if BookedSeat.objects.filter(seat=seat, showtime=showtime).exists():
                raise serializers.ValidationError(
                    f"Seat {seat} is already booked for this showtime."
                )            
        return data
    
    def create(self, validated_data):
        """
        This runs AFTER validation passes.
        We create the booking and link seats
        """
        seat_ids = validated_data.pop('seats')
        user = self.context['request'].user     #Get logged-in user (automatically)

        # Create booking first
        booking = Booking.objects.create(user=user, **validate_data)

        # Create BookedSeat entries for each seat
        for seat_id in seat_ids:
            BookedSeat.objects.create(
                booking=booking,
                seat_id=seat_id,
                showtime=booking.showtime
            )
        return booking