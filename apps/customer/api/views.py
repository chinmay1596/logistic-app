from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.customer.models import Customer

from .serializers import ListCustomerSerializer
from rest_framework.response import Response

User = get_user_model()


class CustomerAPIView(CreateAPIView):
    serializer_class = ListCustomerSerializer

    def post(self, request, *args, **kwargs):
        serializer = ListCustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Customer add Successfully.",
                    "data": serializer.data

                }
            )
