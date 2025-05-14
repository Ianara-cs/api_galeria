from django.contrib import admin
from django.urls import path, include
from apps.core.routers import router as router_core

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacao/', include('apps.autenticacao.urls')),
    path('core/', include(router_core.urls)),
]
