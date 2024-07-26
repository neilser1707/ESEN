from django.urls import path
from .views import SegurosView, SegurosAdministrar

urlpatterns = [
    path('administrar/', SegurosAdministrar.as_view()),
    path('', SegurosView.as_view()),
]