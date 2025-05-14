from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Foto
from .serializers import FotoSerializer
from common.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class FotoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Foto.objects.all().order_by('-data_envio')
    serializer_class = FotoSerializer

    def get_permissions(self):
        if self.action in ['aprovar', 'reprovar']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Foto.objects.all().order_by('-data_envio')
        return Foto.objects.filter(aprovada=True).order_by('-data_envio')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def aprovar(self, request, pk=None):
        foto = self.get_object()
        foto.aprovada = True
        foto.save()
        return Response({'status': 'foto aprovada'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def reprovar(self, request, pk=None):
        foto = self.get_object()
        foto.aprovada = False
        foto.save()
        return Response({'status': 'foto reprovada'}, status=status.HTTP_200_OK)
