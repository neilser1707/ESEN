from rest_framework import serializers
from .models import Seguros

class SegurosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguros
        fields = "__all__"
