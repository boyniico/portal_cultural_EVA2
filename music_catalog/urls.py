from django.urls import path
from music_catalog import views

urlpatterns = [
    path('catalog/', views.catalog, name="music_catalog"),
    path('catalog/<int:album_id>/', views.music_detail, name='music_detail'),
]
