'''
    @author SABINA 
    @created 17/03/2024 5:30 PM
    @project Backend(MomentGram)
'''
from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name','created_at', 'updated_at']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'profile_picture']

