from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from apps.autenticacao.serializers import AdminCreateUserSerializer, ListUserSerializer
from common.permissions import IsAdminUser
from common.pagination import CustomQueryPagination
from .filters import UsuarioFilters

class UsuarioViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [IsAdminUser]
    filterset_class = UsuarioFilters
    pagination_class = CustomQueryPagination
    
    
    def get_serializer_class(self):
        """
        Dependendo do método, será disponibilidado um serializer específico    
        """
        serializer_class = super().get_serializer_class()
        if self.action in ['create', 'partial_update', 'put']:
            serializer_class = AdminCreateUserSerializer
        return serializer_class
    
    @action(detail=False, methods=["get"], url_path="me", permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retorna os dados do usuário autenticado
        """
        serializer = ListUserSerializer(request.user)
        return Response(serializer.data)