from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse


# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


# User Login View
class LoginAPIView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                "status": status.HTTP_200_OK,
                "message": "success",
                "data": {
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                },

            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid username or password",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


# User Profile Picture View
class UserProfilePictureView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    # Saving the profile picture of the requesting user
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user_id=user)

    # Retrieving only the profile picture of the requesting user
    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user_id=user)
