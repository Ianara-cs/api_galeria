from rest_framework import serializers
from .models import Foto, Comentario, Curtida

class FotoSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Foto
    """
    curtido = serializers.SerializerMethodField()
    quantidade_curtidas = serializers.SerializerMethodField()
    
    class Meta:
        model = Foto
        fields = [
            'id', 
            'imagem', 
            'imagem_url', 
            'descricao', 
            'usuario_id', 
            'aprovada', 
            'data_envio', 
            'curtido', 
            'quantidade_curtidas']
        read_only_fields = ['aprovada', 'usuario_id', 'data_envio']
        
    def get_curtido(self, obj):
        user = self.context['request'].user
        return obj.curtida_set.filter(usuario_id=user).exists()
    
    def get_quantidade_curtidas(self, obj):
        return obj.curtida_set.filter(foto_id=obj).count()

    def create(self, validated_data):
        validated_data['usuario_id'] = self.context['request'].user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """
        Este método permite customizar o retorno ao usuário
        """
        retorno = super().to_representation(instance)
        retorno.pop('usuario_id')
        retorno['usuario'] = {
            "id": instance.usuario_id.id,
            "username": instance.usuario_id.username
        }
        return retorno

class CurtidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curtida
        fields = ['id', 'usuario_id', 'foto_id', 'data_criacao']
        read_only_fields = ['usuario_id', 'data_criacao']

    def validate(self, data):
        usuario = self.context['request'].user
        foto = data.get('foto_id')
        
        if not foto.aprovada:
            raise serializers.ValidationError("Não é permitido curtit em uma foto não aprovada.")
        
        if Curtida.objects.filter(usuario_id=usuario, foto_id=foto).exists():
            raise serializers.ValidationError("Você já curtiu essa foto.")
        return data

    def create(self, validated_data):
        return super().create(validated_data)
    
class ComentarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comentario
        fields = ['id', 'usuario_id', 'foto_id', 'texto', 'data_criacao']
        read_only_fields = ['usuario_id', 'data_criacao']
    
    def validate(self, attrs):
        foto = attrs.get('foto_id')
        if not foto.aprovada:
            raise serializers.ValidationError("Não é permitido comentar em uma foto não aprovada.")
        return attrs

    def create(self, validated_data):
        validated_data['usuario_id'] = self.context['request'].user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """
        Este método permite customizar o retorno ao usuário
        """
        retorno = super().to_representation(instance)
        retorno.pop('usuario_id')
        retorno['usuario'] = {
            "id": instance.usuario_id.id,
            "username": instance.usuario_id.username,
            "nome": instance.usuario_id.first_name
        }
        return retorno
