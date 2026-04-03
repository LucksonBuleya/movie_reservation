from rest_framework.permissions import IsAuthenticated
from rest_framework import APIView
from rest_framework.response import Response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}! This is a protected view!"})