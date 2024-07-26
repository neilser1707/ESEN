from rest_framework import serializers
from .models import Contratos

class ContratosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contratos
        fields = '__all__'
        extra_kwargs = {'tomadores': {'write_only': True}, 'seguros': {'write_only': True}}