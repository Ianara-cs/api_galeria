from django.contrib import admin
from django.urls import path, include
from apps.core.routers import router as router_core
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacao/', include('apps.autenticacao.urls')),
    path('core/', include(router_core.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
