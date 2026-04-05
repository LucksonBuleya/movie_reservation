from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TheaterViewSet, SeatViewSet

router = DefaultRouter()
router.register(r'theaters', TheaterViewSet)
router.register(r'seats', SeatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]