from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.response import Response
from apps.commons.mixins.viewset_mixins import RetrieveViewSetMixin

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = TokenObtainPairSerializer


class UserRetrieveAPIView(RetrieveViewSetMixin):
    queryset = User
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
