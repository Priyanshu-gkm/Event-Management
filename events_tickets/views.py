from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Account
from accounts.serializers import AccountSerializer
from events_tickets.models import EventTicketTypes,Event,Photo,Ticket,TicketTypes
from events_tickets.serializers import EventSerializer,TicketSerializer,PhotoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated , IsAdminUser


class EventLCAPIView(ListCreateAPIView):
    #queryset
    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            # If the user is an admin, return all events
            return Event.objects.all()
        else:
            # For non-admin users, return filtered events
            return Event.objects.filter(is_active=True)
        
    queryset=get_queryset()
    serializer_class = EventSerializer