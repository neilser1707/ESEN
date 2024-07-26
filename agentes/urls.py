from django.urls import path
from .views import CrearCuenta, AdministarCuentas, AdministrarSeguros

urlpatterns = [
    
    # administrar/ : Se utiliza en la manipulación de cuentas de agentes
    path('administrar/', AdministarCuentas.as_view(), name='administrar_cuenta'),
    # crear/ : Esta funcionalidad es independiente pues no es protegida
    path('crear/', CrearCuenta.as_view(), name='crear_cuenta'),
    # seguros/ : Se utiliza para agregar o eliminar relaciones del tipo agente-seguro
    path('seguros/', AdministrarSeguros.as_view(), name='seguros'),

]