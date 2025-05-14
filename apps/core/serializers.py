from rest_framework import serializers
from .models import Foto

class FotoSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Foto
    """
    class Meta:
        model = Foto
        fields = ['id', 'imagem', 'descricao', 'usuario', 'aprovada', 'data_envio']
        read_only_fields = ['aprovada', 'usuario', 'data_envio']

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """
        Este método permite customizar o retorno ao usuário
        """
        retorno = super().to_representation(instance)
        retorno.pop('usuario')
        retorno['usuario'] = {
            "id": instance.usuario.id,
            "username": instance.usuario.username
        }
        return retorno
