from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ServerSerializer
from rest_framework.response import Response
from .models import Server
# Create your views here.


class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')
        quantity = request.query_params.get("quantity")
        by_user = request.query_params.get('by_user') == 'True'

        if category:
            self.queryset = self.queryset.filter(category__name=category)
    
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)
        
        if quantity:
            self.queryset = self.queryset[: int(quantity)]

 
        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)