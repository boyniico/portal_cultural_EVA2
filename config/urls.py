from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('music/', include('music_catalog.urls')),
    path('books/', include('books_catalog.urls')),
    path('', include('cart.urls')),
]

# Esto permite servir las imágenes de la carpeta media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)