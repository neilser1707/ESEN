from django.db import models

class Tomadores(models.Model):
    ci = models.CharField(primary_key=True, max_length=11)
    nombre = models.CharField(max_length=100)
    apellido_1 = models.CharField(max_length=100)
    apellido_2 = models.CharField(max_length=100)
    
