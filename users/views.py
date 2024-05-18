"""
Views for the users app.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    """
    serializer_class = UserSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update the authenticated user
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
