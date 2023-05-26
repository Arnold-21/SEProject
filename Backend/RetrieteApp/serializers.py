from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *

User = get_user_model()

#Custom token serializer to put the user_id, and role in the token, that's sent to frontend
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id
        token['role'] = user.role

        return token
    
#User serializer for getting the user details, and the id, for potential use on the frontend
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")

#Geolocation Serializer
class GeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = "__all__"

#Destination Serializer, with the location serialized for more detail, basically for get requests
class DestinationSerializer(serializers.ModelSerializer):
    location = GeolocationSerializer(read_only=True)
    
    class Meta:
        model = Destination
        fields = "__all__"

#Destination serializer for put requests, for easier use
class SimpleDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = "__all__"