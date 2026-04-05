from rest_framework import viewsets
from .models import Theater, Seat
from .serializers import TheaterSerializer, SeatSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]