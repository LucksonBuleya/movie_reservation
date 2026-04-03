from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

