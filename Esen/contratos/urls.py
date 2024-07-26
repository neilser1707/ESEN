from django.urls import path
from .views import AdministrarContratos, ContratosView, ContratoView, ContratoPago

urlpatterns = [
    # administrar/: Se utiliza en la manipulación de contratos
    path('administrar/', AdministrarContratos.as_view()),
    # /: Se utiliza para obtener todos los contratos vinculados a un agente
    path('', ContratosView.as_view()),
    # buscar/: Se utiliza para obtener un contrato en específico
    path('buscar/', ContratoView.as_view()),
    # pago/: Se utiliza para saber cuanto debe pagar una persona por cierto contrato
    path('pago/', ContratoPago.as_view()),
]