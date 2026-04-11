from django.db import models
from django.contrib.auth.models import User
from movies.models import Showtime
from theaters.models import Seat


class Booking(models.Model):
    """
    Represents a user's booking for a specific showtime.
    One booking can contain multiple seats.
    """

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    showtime = models.ForeignKey(
        Showtime,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} ({self.status})"


class BookedSeat(models.Model):
    """
    Represents a specific seat booked for a showtime.
    This is where we prevent double booking.
    """

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='booked_seats'
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE
    )

    showtime = models.ForeignKey(
        Showtime,
        on_delete=models.CASCADE
    )

    class Meta:
        # Prevent same seat being booked twice for same showtime
        constraints = [
            models.UniqueConstraint(
                fields=['seat', 'showtime'],
                name='unique_seat_per_showtime'
            )
        ]

    def __str__(self):
        return f"{self.seat} - {self.showtime} (Booking {self.booking.id})"