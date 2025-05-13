from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User
from apps.autenticacao.serializers import AdminCreateUserSerializer, ListUserSerializer
from common.permissions import IsAdminUser

class UsuarioViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        """
        Dependendo do método, será disponibilidado um serializer específico    
        """
        serializer_class = super().get_serializer_class()
        if self.action in ['create', 'partial_update', 'put']:
            serializer_class = AdminCreateUserSerializer
        return serializer_class