from rest_framework.views import APIView
from esen.mixins.permisos import AutorizacionMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from agentes.models import Agentes, Tomador_Agente
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContratosSerializer
from .models import Contratos
from tomadores.views import TomadoresView, Tomador_Agente, Tomadores, TomadorView
from .mixins import Calculos

"""
    Este archivo views.py contiene 3 vistas basadas en clases:
     - AdministaraContratos:
       - Se utiliza para crear, actualizar y eliminar contratos
     - ContratosView:
       - Se utiliza para obtener los contratos vinculados a un agente
     - ContratoView:
       - Se utiliza para obtener la información asociada a un contrato específico
     - ContratoPago:
       - Se utiliza para obtener las tarifas y descuentos de un contarto en específico
"""

class AdministrarContratos(APIView, AutorizacionMixin):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        agente = Agentes.objects.get(id=self.identificar(request=request))
        tomador_agente = Tomador_Agente.objects.filter(
            Q(agente=agente.id) & Q(tomador=request.data['ci'])
            )
        if not tomador_agente.exists():
            return Response({"Response": "Usted trabaja con un tomador de ci: " + request.data['ci']}
                            , status=status.HTTP_403_FORBIDDEN
                            )
        periodo_pago = [3,6,12]
        request.data['tomadores'] = tomador_agente.first().id
        serializer = ContratosSerializer(data=request.data)
        if serializer.is_valid():
            if not int(request.data['periodo_pago']) in periodo_pago:
                return Response({"Response": "Debe pagar en un plazo establecido"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"Response": "Contrato creado"}, status=status.HTTP_201_CREATED)
        return Response({"Response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        agente = Agentes.objects.get(id=self.identificar(request=request))
        contrato = Contratos.objects.filter(
            Q(no_poliza=request.data['no_poliza'])
            )
        if not contrato.exists():
            return Response({"Response": "No existe un contrato de poliza: " + request.data['no_poliza']}
                            , status=status.HTTP_204_NO_CONTENT
                            )
        tomador_agente = Tomador_Agente.objects.filter(
            Q(tomador=contrato.first().tomadores.tomador.ci)
        ).first()
        if tomador_agente.agente.id != agente.id:
            return Response({"Response": "Usted no gestiona un contrato de poliza: " + request.data['no_poliza']}
                            , status=status.HTTP_403_FORBIDDEN
                            )
        periodo_pago = [3,6,12]
        fecha_inicio = contrato.first().fecha_inicio
        request.data['fecha_inicio'] = fecha_inicio
        serializer = ContratosSerializer(contrato.first(), data=request.data, partial=True)
        if serializer.is_valid():
            if not int(request.data['periodo_pago']) in periodo_pago:
                return Response({"Response": "Debe pagar en un plazo establecido"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"Response": "Contrato actualizado"}, status=status.HTTP_201_CREATED)
        return Response({"Response": serializer.errors}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request):
        agente = Agentes.objects.get(id=self.identificar(request=request))
        contrato = Contratos.objects.filter(
            Q(no_poliza=request.data['no_poliza'])
            )
        if not contrato.exists():
            return Response({"Response": "No existe un contrato de poliza: " + request.data['no_poliza']}
                            , status=status.HTTP_204_NO_CONTENT
                            )
        tomador_agente = Tomador_Agente.objects.filter(
            Q(tomador=contrato.first().tomadores.tomador.ci)
        ).first()
        if tomador_agente.agente.id != agente.id:
            return Response({"Response": "Usted no gestiona un contrato de poliza: " + request.data['no_poliza']}
                            , status=status.HTTP_403_FORBIDDEN
                            )
        contrato.delete()
        return Response({"Response": "Contrato eliminado"}, status=status.HTTP_200_OK)
    
class ContratosView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        aux = TomadoresView()
        response = aux.get(request=request)
        dict_tomadores = response.data
        for item in dict_tomadores:
            tomadores = Tomadores.objects.filter(
                Q(ci=item['ci'])
            ).first()
            tomador_agente = Tomador_Agente.objects.filter(
                Q(tomador=tomadores)
            ).first()
            contratos = Contratos.objects.filter(
                Q(tomadores=tomador_agente)
            )
        data = ContratosSerializer(contratos, many=True).data
        for data1, data2 in zip(dict_tomadores, data):
            data1.update(data2)
        data_final = dict_tomadores
        return Response(data_final, status=status.HTTP_200_OK)
    
class ContratoView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        aux = TomadorView()
        response = aux.get(request=request)
        dict_tomadores = response.data
        for item in dict_tomadores:
            tomadores = Tomadores.objects.filter(
                Q(ci=item['ci'])
            ).first()
            tomador_agente = Tomador_Agente.objects.filter(
                Q(tomador=tomadores)
            ).first()
            contratos = Contratos.objects.filter(
                Q(tomadores=tomador_agente)
            )
        data = ContratosSerializer(contratos, many=True).data

        for data1, data2 in zip(dict_tomadores, data):
            data1.update(data2)

        data_final = dict_tomadores
        return Response(data_final, status=status.HTTP_200_OK)

class ContratoPago(APIView, AutorizacionMixin):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agente = Agentes.objects.get(id=self.identificar(request=request))
        contrato = Contratos.objects.filter(
            Q(no_poliza=request.data['no_poliza'])
            )
        if not contrato.exists():
            return Response({"Response": "No existe un contrato de poliza: " + request.data['no_poliza']}
                            , status=status.HTTP_204_NO_CONTENT
                            )
        tomador_agente = Tomador_Agente.objects.filter(
            Q(tomador=contrato.first().tomadores.tomador.ci)
        ).first()
        if tomador_agente.agente.id != agente.id:
            return Response({"Response": "Usted no gestiona un contrato de poliza: " + request.data['no_poliza']}
                            , status=status.HTTP_403_FORBIDDEN
                            )
        calculos = Calculos()
        tarifa_muerte = calculos.clalular_tarifa_muerte(contrato=contrato)
        tarifa_incapacidad_temporal = calculos.calcular_tarifa_incapacidad_temporal(contrato=contrato)
        tarifa_incapacidad_permanente = calculos.calcular_tarifa_incapacidad_permanete(contrato=contrato)
        descuento = calculos.calcular_descuentos(contrato=contrato)

        tarifa_total = (
            tarifa_muerte + tarifa_incapacidad_permanente + tarifa_incapacidad_temporal - descuento
        )

        data = ContratosSerializer(contrato.first()).data
        data['tarifa_muerte'] = tarifa_muerte
        data['tarifa_incapacidad_temporal'] = tarifa_incapacidad_temporal
        data['tarifa_incapacidad_permanente'] = tarifa_incapacidad_permanente
        data['descuento'] = descuento
        data['tarifa_total'] = tarifa_total

        return Response(data, status=status.HTTP_200_OK)
