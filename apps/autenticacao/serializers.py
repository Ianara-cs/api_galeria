from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
    
class AdminCreateUserSerializer(ModelSerializer):
    """
    Serializer utilizado para se criar e atualizar dados de um usuário
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "password",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
        ]

    def validate_email(self, email):
        user_qs = User.objects.filter(email=email)
        if self.instance:
            user_qs = user_qs.exclude(pk=self.instance.pk)  # ignora o próprio usuário
        if user_qs.exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return email

    def validate_password(self, password):
        password_validation.validate_password(password, self.instance)
        return make_password(password)

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = self.validate_password(validated_data['password'])
        else:
            raise serializers.ValidationError({"password": "Senha é obrigatória para criação de usuário."})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        
        if instance.is_superuser and not request_user.is_superuser:
            raise serializers.ValidationError("Você não tem permissão para editar um superusuário.")

        if 'password' in validated_data:
            validated_data['password'] = self.validate_password(validated_data['password'])
        return super().update(instance, validated_data)

class ListUserSerializer(ModelSerializer):
    """
    Serializer utilizado para listagem geral  e específica de usuários
    """
    class Meta:
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
        ]
        model = User