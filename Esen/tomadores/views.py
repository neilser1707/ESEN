from rest_framework.views import APIView
from esen.mixins.permisos import AutorizacionMixin
from .serializers import Tomadores_Serializer, TomadoresAgentesSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from agentes.models import Agentes, Tomador_Agente
from .models import Tomadores
from django.db.models import Q

class AdministrarTomadores(APIView, AutorizacionMixin):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        agente = Agentes.objects.filter(
            Q(id=self.identificar(request=request))
        )
        if not agente.exists():
            return Response({"Response": "Usted no es agente"}, status=status.HTTP_403_FORBIDDEN)
        flag = True
        try:
            data = {
            'tomador': request.data['ci'],
            'tel_fijo': request.data['tel_fijo'],
            'movil': request.data['movil'],
            'localizacion': request.data['localizacion'],
            'direcc': request.data['direcc'],
            'fecha_modificacion': request.data['fecha'],
            'fecha_registro': request.data['fecha']
        }
        except:
            return Response({"Response": "Datos inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        agente = agente.first()
        data['agente'] = agente.id
        tomador = Tomadores.objects.filter(
            Q(ci=request.data['ci'])
        )
        if not tomador.exists():
            flag = False
            serializer_tomador = Tomadores_Serializer(data=request.data)
            if serializer_tomador.is_valid():
                serializer_tomador.save()
            else:
                return Response({"Response": serializer_tomador.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        if flag and tomador.first() in agente.tomadores.all():
            return Response({"Response": "El registro que se desea crear ya existe"}, 
                            status=status.HTTP_409_CONFLICT)      
        
        serializer = TomadoresAgentesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"Response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Response": "Registro creado"}, status=status.HTTP_201_CREATED)

    def put(self, request):
        agente = Agentes.objects.filter(
            Q(id=self.identificar(request=request))
        )
        if not agente.exists():
            return Response({"Response": "Usted no es agente"}, status=status.HTTP_403_FORBIDDEN)
        agente = agente.first()
        tomador = Tomadores.objects.filter(Q(ci=request.data['ci'])).first()
        if tomador in agente.tomadores.all():
            relacion = Tomador_Agente.objects.get(agente=agente, tomador=tomador)
            data = {
            'agente': agente.id,
            'tomador': request.data.get('ci', relacion.tomador),
            'tel_fijo': request.data.get('tel_fijo', relacion.tel_fijo),
            'movil': request.data.get('movil', relacion.movil),
            'localizacion': request.data.get('localizacion', relacion.localizacion),
            'direcc': request.data.get('direcc', relacion.direcc),
            'fecha_modificacion': request.data.get('fecha', relacion.fecha_modificacion),
            'fecha_registro': relacion.fecha_registro,
            }
            serializer = TomadoresAgentesSerializer(relacion,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Response": "Registro actualizado"}, status=status.HTTP_200_OK)
            else:
                return Response({"Response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Response": "Usted no trabaja con un tomador de ci: " + request.data['ci']}, status=status.HTTP_204_NO_CONTENT)
        
    def delete(self, request):
        agente = Agentes.objects.get(id=self.identificar(request=request))
        tomador = Tomadores.objects.filter(Q(ci=request.data['ci'])).first()
        if tomador in agente.tomadores.all():
            agente.tomadores.remove(tomador)
            tomadores = Tomador_Agente.objects.filter(Q(tomador_id=tomador.ci))
            if not tomadores.exists():
                tomador.delete()
            return Response({"Response": "Registro eliminado"}, status=status.HTTP_200_OK)
        else:
            return Response({"Response": "Usted no trabaja con un tomador de ci: " + request.data['ci']}, status=status.HTTP_204_NO_CONTENT)
        
class TomadoresView(APIView, AutorizacionMixin):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agente = Agentes.objects.get(id=self.identificar(request=request))
        tomadores = agente.tomadores.all()
        if not tomadores.exists():
            return Response({"Response": "No se encontraron tomadores"},
                             status=status.HTTP_204_NO_CONTENT)
        serializer = Tomadores_Serializer(tomadores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TomadorView(APIView, AutorizacionMixin):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    

    def get(self, request):
        agente = Agentes.objects.get(id=self.identificar(request=request))
        try:
            nombre = request.data['nombre']
        except:
            return Response({"Response": "Datos inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        tomadores = agente.tomadores.filter(
            Q(nombre=nombre)
        )
        if not tomadores.exists():
            return Response({"Response": "No se encontraron tomadores"},
                             status=status.HTTP_204_NO_CONTENT)
        relaciones = []
        lista_tomadores = list(tomadores)

        for r in lista_tomadores:
            relaciones.append(Tomador_Agente.objects.get(agente=agente, tomador=r))

        data = Tomadores_Serializer(tomadores, many=True).data
        data_tomadores_agente = TomadoresAgentesSerializer(relaciones, many=True).data

        for item1, item2 in zip(data, data_tomadores_agente):
            item1.update(item2)
            
        return Response(data, status=status.HTTP_200_OK)