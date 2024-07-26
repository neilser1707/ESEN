from django.db import models
from django.contrib.auth.models import User
from seguros.models import Seguros
from tomadores.models import Tomadores

class Agentes(User):

    """
        Herencia concreta del modelo User, sin embargo dadas ciertas necesidades propias del
        Sistema se crea este modelo para las relaciones debidas
    """

    seguros = models.ManyToManyField(Seguros, related_name="agente")
    tomadores = models.ManyToManyField(Tomadores, through='Tomador_Agente')

class Tomador_Agente(models.Model):

    """
        Este modelo funciona como modelo pivote entre los agentes y los tomadores, al mismo tiempo
        Incluye información propia entre el tomador y el agente (Estos modelos poseen
        Relación Many to Many)
    """

    agente = models.ForeignKey(Agentes, on_delete=models.CASCADE)
    tomador = models.ForeignKey(Tomadores, on_delete=models.CASCADE)
    tel_fijo = models.IntegerField()
    movil = models.IntegerField()
    direcc = models.CharField(max_length=200)
    localizacion = models.TextField()
    fecha_modificacion = models.DateTimeField()
    fecha_registro = models.DateTimeField()
    