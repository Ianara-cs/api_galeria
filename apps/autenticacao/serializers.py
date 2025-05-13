from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
    
class AdminCreateUserSerializer(ModelSerializer):
    """
    Serializer utilizado para se criar e atualizar dados de um usuário
    """
    
    password = serializers.CharField(write_only=True)
    class Meta:
        fields = [
            "password",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
        ]
        model = User
        
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return email
        
    def validate_password(self, data):
        password_validation.validate_password(data, self.instance)
        data = make_password(data)
        return data
    
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
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