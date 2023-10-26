# event_manager/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Account
from accounts.serializers import AccountSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class AccountLCAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']
    
    
class AccountRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']
    
    

class LoginView(APIView):
    def post(self,request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            user = None
            try:
                user = Account.objects.get(username=username)
            except ObjectDoesNotExist:
                pass

            if not user:
                user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,
                                 'user_id': user.pk,
                                 'email': user.email
                                 }
                                , status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # Delete the user's authentication token
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
