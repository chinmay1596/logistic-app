from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from apps.support.models import Ticket, Chat
from .serializers import (TicketSerializer, TicketDetailSerializer,
                          ChatSerializer)
from rest_framework.response import Response
from apps.commons.mixins.viewset_mixins import ListCreateViewSetMixin, RetrieveViewSetMixin


class TicketCreateViewset(ListCreateViewSetMixin):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = []


class TicketDetailViewset(RetrieveViewSetMixin):
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailSerializer
