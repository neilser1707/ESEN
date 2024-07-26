from django.db import models
from seguros.models import Seguros
from agentes.models import Tomador_Agente

class Contratos(models.Model):

    """
        Modelo creado con el objetivo de almacenar la información necesaria para la creación 
        De un contrato de Vida por parte de cierto tomador

        Nota: Esta aplicación se encuentra en extensión y desarrollo por lo que aunque el modelo 
        Contrato solo funcione para Vida, a futuro mediante la herencia uno a uno, se reflejarán 
        Cambios en torno a este modelo
    """

    no_poliza = models.IntegerField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    periodo_pago = models.IntegerField()
    valor_muerte = models.IntegerField()
    valor_incapacidad_temporal = models.IntegerField()
    valor_incapacidad_permanente = models.IntegerField()
    tipo_oficio = models.IntegerField()
    seguros = models.ForeignKey(Seguros, on_delete=models.CASCADE)
    tomadores = models.ForeignKey(Tomador_Agente, on_delete=models.CASCADE)
    
class ReglasAños(models.Model):
    #Contiene los datos necesarios para fijar normas respecto a los años que tiene la persona
    id = models.AutoField(primary_key=True)
    rango_años = models.FloatField()
    porcentaje = models.FloatField()

class TiposOficios(models.Model):
    #Contiene los datos necesarios para fijar normas respecto al oficio que ocupa la persona
    id = models.AutoField(primary_key=True)
    tipo = models.IntegerField()
    porcenntaje = models.FloatField()
    costo_diario = models.FloatField()

class Descuentos(models.Model):
    #Contiene los datos necesarios para fijar normas respecto a los años que tiene la persona ligada
    #a cierto contrato
    id = models.AutoField(primary_key=True)
    años = models.IntegerField()
    porcenntaje = models.FloatField()