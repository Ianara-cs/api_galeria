from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Foto, Curtida, Comentario
from .filters import ComentarioFilters, FotosFilters
from .serializers import FotoSerializer, CurtidaSerializer, ComentarioSerializer
from common.permissions import IsAdminUser, IsOwnerOrReadOnly
from common.pagination import CustomQueryPagination
from common.storage import upload_imagem_firebase
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.conf import settings
import uuid
from firebase_admin import storage

class FotoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Foto.objects.all().order_by('-data_envio')
    serializer_class = FotoSerializer
    filterset_class = FotosFilters
    pagination_class = CustomQueryPagination

    def get_permissions(self):
        if self.action in ['aprovar', 'reprovar']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset
        return Foto.objects.filter(aprovada=True).order_by('-data_envio')

    def perform_create(self, serializer):
        serializer.save(usuario_id=self.request.user)
        
    def _set_aprovada(self, aprovada: bool):
        foto = self.get_object()
        foto.aprovada = aprovada
        foto.save()
        return Response({'status': f'foto {"aprovada" if aprovada else "reprovada"}'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def aprovar(self, request, pk=None):
        return self._set_aprovada(True)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def reprovar(self, request, pk=None):
        return self._set_aprovada(False)
    
    
    @action(detail=False, methods=['post'], url_path='upload-multiplas')
    def upload_multiplas(self, request):
        """
            Multiplos Uploados de fotos
        """
        imagens = request.FILES.getlist('imagens')
        descricao = request.data.get('descricao', '')

        if not imagens:
            return Response({'erro': 'Nenhuma imagem enviada.'}, status=status.HTTP_400_BAD_REQUEST)

        fotos_criadas = []

        if settings.USE_FIREBASE_STORAGE:
            # Firebase: produção
            with transaction.atomic():
                for imagem in imagens:
                    imagem_url = upload_imagem_firebase(imagem, settings.FIREBASE_BUCKET_NAME)
                    foto = Foto.objects.create(
                        imagem_url=imagem_url,
                        descricao=descricao,
                        usuario_id=request.user
                    )
                    fotos_criadas.append(FotoSerializer(foto, context={'request': request}).data)

        else:
            # Local: desenvolvimento
            with transaction.atomic():
                for imagem in imagens:
                    serializer = self.get_serializer(
                        data={
                            'imagem': imagem,
                            'descricao': descricao
                        },
                        context={'request': request}
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save(usuario_id=request.user)
                    fotos_criadas.append(serializer.data)

        return Response(fotos_criadas, status=status.HTTP_201_CREATED)


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
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Comentario.objects.filter(foto_id__aprovada=True).order_by('-data_criacao')
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_class = ComentarioFilters

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action in ['update', 'partial_update']:
            return queryset.filter(usuario_id=user)
        if user.is_staff:
            return Comentario.objects.all().order_by('-data_criacao')
        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario_id=self.request.user)
