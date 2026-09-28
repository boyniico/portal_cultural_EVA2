from django.contrib import admin
from .models import Artist, Genre, Album

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "year", "genre", "stock", "price")
    search_fields = ("title", "artist__name", "genre__name")
    list_filter = ("year", "genre", "stock")
    autocomplete_fields = ['artist', 'genre']