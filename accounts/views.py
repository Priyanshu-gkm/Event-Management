# event_manager/views.py
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Account
from accounts.serializers import AccountSerializer

class AccountAPIView(APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # permission_classes = [IsAdminUser]
    def get(self,request,pk=None):
        id = pk
        if id is not None:
            account = Account.objects.get(id=id)
            serializer = AccountSerializer(account)
            return Response(serializer.data)

        account = Account.objects.all()
        serializer = AccountSerializer(account, many=True)

        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
