from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer

class SignUpView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]