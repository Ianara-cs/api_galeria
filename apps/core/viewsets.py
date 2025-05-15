from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Foto, Curtida, Comentario
from .filters import ComentarioFilters
from .serializers import FotoSerializer, CurtidaSerializer, ComentarioSerializer
from common.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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
        serializer.save(usuario_id=self.request.user)

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

class CurtidaViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Curtida.objects.all()
    serializer_class = CurtidaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario_id=self.request.user)
    
    @action(detail=False, methods=['delete'], url_path='foto/(?P<foto_id>[^/.]+)')
    def descurtir(self, request, foto_id=None):
        usuario = request.user
        curtida = Curtida.objects.filter(usuario_id=usuario, foto_id=foto_id).first()

        if curtida:
            curtida.delete()
            return Response({"detail": "Curtida removida."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Curtida não encontrada."}, status=status.HTTP_404_NOT_FOUND)

class ComentarioViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Comentario.objects.filter(foto_id__aprovada=True).order_by('-data_criacao')
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ComentarioFilters

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return Comentario.objects.all().order_by('-data_criacao')
        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario_id=self.request.user)
