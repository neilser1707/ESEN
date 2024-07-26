from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from agentes.models import User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import SegurosSerializer
from esen.mixins.permisos import AutorizacionMixin
from rest_framework import generics
from .models import Seguros


class SegurosAdministrar(APIView, AutorizacionMixin):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = self.identificar(request=request)
        objects = User.objects.filter(
            Q(id=user_id) & Q(is_superuser=1)
        )
        if not objects.exists():
            return Response({"error": "No autorizado para agregar seguros"},
                             status=status.HTTP_403_FORBIDDEN)
        serializer = SegurosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Response": "Seguro creado"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        user_id = self.identificar(request=request)
        objects = User.objects.filter(
            Q(id=user_id) & Q(is_superuser=1)
        )
        if not objects.exists():
            return Response({"error": "No autorizado para agregar seguros"},
                             status=status.HTTP_403_FORBIDDEN)
        instance = Seguros.objects.get(nombre=request.data['nombre'])
        serializer = SegurosSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Response": "Seguro actualizado"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = self.identificar(request=request)
        objects = User.objects.filter(
            Q(id=user_id) & Q(is_superuser=1)
        )
        if not objects.exists():
            return Response(
                {"error": "No autorizado para eliminar seguros"},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = Seguros.objects.get(nombre=request.data['nombre'])
        instance.delete()
        return Response({"Response": "Seguro eliminado"}, status=status.HTTP_204_NO_CONTENT)

class SegurosView(generics.ListAPIView):
    queryset = Seguros.objects.all()
    serializer_class = SegurosSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]