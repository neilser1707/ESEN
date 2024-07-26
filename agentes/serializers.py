from rest_framework.serializers import ModelSerializer
from .models import Agentes

class Agentes_Serializer(ModelSerializer):

    class Meta:
        model = Agentes
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        agente = Agentes.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        agente.set_password(validated_data['password'])
        agente.save()
        return agente
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  
        instance.save()
        return instance
    
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        return token