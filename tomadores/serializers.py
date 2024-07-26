from rest_framework import serializers
from .models import Tomadores
from agentes.models import Tomador_Agente

class Tomadores_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Tomadores
        fields = '__all__'

class TomadoresAgentesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tomador_Agente
        fields = '__all__'
        extra_kwargs = {'agente':{'write_only': True}, 'tomador':{'write_only': True}}