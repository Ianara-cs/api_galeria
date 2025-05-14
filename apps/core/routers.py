from rest_framework.routers import DefaultRouter

from apps.core.viewsets import FotoViewSet

router = DefaultRouter()
router.register(r'fotos', FotoViewSet)