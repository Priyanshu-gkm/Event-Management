from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Account
from accounts.serializers import AccountSerializer
from events_tickets.models import EventTicketType,Event,Photo,Ticket,TicketType
from events_tickets.serializers import EventSerializer,TicketSerializer,PhotoSerializer,TicketTypesSerializer,EventTicketTypesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView , ListAPIView , CreateAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from events_tickets.custom_permissions import IsOrganizer , isAttendee
    


class TicketTypeLC(ListCreateAPIView):
    serializer_class = TicketTypesSerializer
    queryset = TicketType.objects.all()
    permission_classes = [IsAuthenticated &  (IsAdminUser | IsOrganizer)]
    
    
class EventListCreate(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            # AllowAny for GET requests
            return [AllowAny()]
        elif self.request.method == 'POST':
            # IsAuthenticated for POST requests
            return [IsAuthenticated(),IsOrganizer()]
        return super().get_permissions()
    
    def get(self,request,*args,**kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        # self.permission_classes=[IsAuthenticated,IsOrganizer]
        event_data = request.data
        event_data['created_by'] = request.user.id
        serializer = self.get_serializer(data=event_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)