from django.urls import path
from .views import AdministrarTomadores, TomadoresView, TomadorView

urlpatterns = [
    path('administrar/', AdministrarTomadores.as_view()),
    path('', TomadoresView.as_view()),
    path('buscar/', TomadorView.as_view()),
]