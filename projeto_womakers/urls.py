"""
URL configuration for projeto_womakers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cadastro.views import inicio, cadastro, logout_user, verificar_cadastro, excluir_usuario
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', inicio, name='home'),
    path('cadastro/', cadastro, name='cadastro'),
    path('verificar-cadastro/', verificar_cadastro, name='verificar_cadastro'),
    path('logout/', logout_user, name='logout'),
    path('excluir_usuario/<int:usuario_id>/', excluir_usuario, name='excluir_usuario'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('rest_api.urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
