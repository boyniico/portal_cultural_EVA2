from django.contrib import admin
from .models import Author, Genre, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'genre', 'price', 'stock')
    list_filter = ('genre', 'author')
    search_fields = ('title', 'author__name', 'genre__name')
    autocomplete_fields = ['author', 'genre']