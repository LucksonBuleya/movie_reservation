from rest_framework import serializers
from .models import Booking, BookedSeat
from theaters.models import Seat


class BookingSerializer(serializers.ModelSerializer):
    # Input: list of seat IDs
    seats = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    # Output fields
    movie = serializers.CharField(source='showtime.movie.title', read_only=True)
    showtime_display = serializers.DateTimeField(
        source='showtime.start_time', read_only=True
    )
    seats_display = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'showtime',  # REQUIRED for POST
            'movie',
            'showtime_display',
            'seats',
            'seats_display',
            'total_price',
            'status',
            'created_at'
        ]
        read_only_fields = [
            'movie',
            'showtime_display',
            'seats_display',
            'total_price',
            'status',
            'created_at'
        ]

    def validate(self, data):
        """
        Ensure:
        - Seats belong to theater
        - Seats are not already booked
        """
        showtime = data['showtime']
        seat_ids = data['seats']

        valid_seats = Seat.objects.filter(theater=showtime.theater)

        for seat_id in seat_ids:
            if not valid_seats.filter(id=seat_id).exists():
                raise serializers.ValidationError(
                    f"Seat {seat_id} does not belong to this theater."
                )

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
        Create booking + booked seats + auto price
        """
        seat_ids = validated_data.pop('seats')
        showtime = validated_data['showtime']
        user = self.context['request'].user

        total_price = len(seat_ids) * showtime.price

        booking = Booking.objects.create(
            user=user,
            showtime=showtime,
            total_price=total_price
        )

        for seat_id in seat_ids:
            BookedSeat.objects.create(
                booking=booking,
                seat_id=seat_id,
                showtime=showtime
            )

        return booking

    def get_seats_display(self, obj):
        """
        Return seats like A1, A2
        """
        return [
            f"{seat.seat.row}{seat.seat.number}"
            for seat in obj.booked_seats.all()
        ]