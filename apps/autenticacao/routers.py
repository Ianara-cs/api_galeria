from rest_framework.routers import DefaultRouter

from apps.autenticacao.viewsets import UsuarioViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)