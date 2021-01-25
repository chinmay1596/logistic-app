from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'gender', 'phone', 'driving_licence', 'image')
