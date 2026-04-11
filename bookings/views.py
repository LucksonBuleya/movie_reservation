from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializer import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    Handles all booking operations:
    - Create booking
    - View bookings
    - Update / cancel booking
    """

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Users should ONLY SEE THIER bookings
        """
        return Booking.objects.filter(user=self.request.user) #User Isolation
    
    def perform_create(self, serializer):
        """
        Automatically attach logged-in user to booking
        """
        serializer.save(user=self.request.user)  #Auto User Assignment
        
    