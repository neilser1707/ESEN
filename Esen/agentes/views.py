from .serializers import Agentes_Serializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from esen.mixins.permisos import AutorizacionMixin
from seguros.models import Seguros
from .models import Agentes

class CrearCuenta(APIView):
    """
        Creación de agentes, por lógica de negocio esta vista no está protegida
    """
    def post(self, request):
        serializer = Agentes_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Datos inválidos"},status=status.HTTP_400_BAD_REQUEST)
    

class AdministarCuentas(APIView, AutorizacionMixin):
    """
        Esta vista es utilizada para adminstrar las cuentas de los agentes
        Todos los métodos de esta vista se encuentran protegido con simplejwt
        La clase AutorizacionMixin es una clase que con jwt identifica al agente en cuestión
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):

        """
            Validaciones para confirmar que el agente está intentando manipular su cuenta
            Y no una cuenta ajena
            Los datos son deserializados y si no presentan inconsistencia
            Un nuevo registro es creado y se informa
            De lo contrario se informa el error en cuestión
        """
        
        agente_id = self.identificar(request=request)
        agente = Agentes.objects.get(id=agente_id)
        try:
            if agente_id != int(request.data['id']):
                return Response({"Response": "No autorizado"},
                    status=status.HTTP_403_FORBIDDEN) 
        except KeyError as e:
            return Response({"Response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = Agentes_Serializer(agente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Response": "Actualización correcta"}, status=status.HTTP_200_OK)
        return Response({"error": "Datos inválidos"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):

        """
            Validaciones para confirmar que el agente está intentando eliminar su cuenta
            Y no una cuenta ajena
            Su cuenta es eliminada y se informa
            De lo contrario se informa el error en cuestión 
        """

        agente_id = self.identificar(request=request)
        try:
            if agente_id != int(request.data['id']):
                return Response({"Response": "No autorizado"},
                    status=status.HTTP_403_FORBIDDEN) 
        except KeyError as e:
            return Response({"Response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        Agentes.objects.get(id=agente_id).delete()
        return Response({"Response": "Registro eliminado"}, status=status.HTTP_204_NO_CONTENT)
    
class AdministrarSeguros(APIView, AutorizacionMixin):

    """
        Esta vista es utilizada para adminstrar las relaciones entre los agentes y los seguros
        Todos los métodos de esta vista se encuentran protegido con simplejwt
        La clase AutorizacionMixin es una clase que con ayuda de jwt identifica al agente en cuestión
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        """
            Agregación de vínculos entre el agente y los seguros diponibles
            La variable de tipo booleano se utiliza con el fin de devolver una respuesta que indique si
            La relación es recien o ya existía
        """

        try:
            seguros = request.data['seguros'] #En el json se debe recibir una lista de strings
        except KeyError as e:
            return Response({"Response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        agente = Agentes.objects.get(id=self.identificar(request=request))
        recien_asociados = False
        for data in seguros:
            try:
                seguro = Seguros.objects.get(nombre=data)
            except Seguros.DoesNotExist as e:
                return Response({"Response": str(e)},
                                 status=status.HTTP_400_BAD_REQUEST
                                )
            if seguro in agente.seguros.all():
                continue
            else:
                agente.seguros.add(seguro)
                recien_asociados = True

        if recien_asociados:
            return Response({"Response": "Registros asociados"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Response": "Tales registros ya se encontraban asociados"}, status=status.HTTP_200_OK)

    def delete(self, request):

        """
            Eliminación de vínculos entre el agente y los seguros diponibles
            La variable de tipo booleano se utiliza con el fin de devolver una respuesta que indique si
            La relación o relaciones fueron eliminadas o no
        """

        agente = Agentes.objects.get(id=self.identificar(request=request))
        try:
            seguros = request.data['seguros']
        except KeyError as e:
            return Response({"Response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        eliminado = False
        for data in seguros:
            try:
                seguro = Seguros.objects.get(nombre=data)
            except Seguros.DoesNotExist as e:
                return Response({"Response": str(e)},
                                 status=status.HTTP_400_BAD_REQUEST
                                )
            if seguro in agente.seguros.all():
                agente.seguros.remove(seguro)
                eliminado = True
            else:
                continue
        if eliminado:
            return Response({"Response": "Registro eliminado"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Datos inválidos"}, status=status.HTTP_400_BAD_REQUEST)