from rest_framework.routers import DefaultRouter

from apps.core.viewsets import FotoViewSet, CurtidaViewSet, ComentarioViewSet

router = DefaultRouter()
router.register(r'fotos', FotoViewSet)
router.register(r'curtidas', CurtidaViewSet)
router.register(r'comentarios', ComentarioViewSet)
