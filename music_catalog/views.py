from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from .models import Album

def catalog(request):
    query = request.GET.get('q', '')
    albums = Album.objects.all().order_by('title')
    
    if query:
        albums = albums.filter(
            Q(title__icontains=query) | 
            Q(artist__name__icontains=query) | 
            Q(genre__name__icontains=query)
        )
    
    # Paginación (ej: 8 álbumes por página)
    paginator = Paginator(albums, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'music/catalog.html', {
        'page_obj': page_obj,
        'query': query
    })

def music_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/music_detail.html', {'album': album})

@never_cache
def catalog(request):
    query = request.GET.get('q', '')
    albums = Album.objects.all().order_by('title')
    
    if query:
        albums = albums.filter(
            Q(title__icontains=query) | 
            Q(artist__name__icontains=query) | 
            Q(genre__name__icontains=query)
        )
    
    paginator = Paginator(albums, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'music/catalog.html', {
        'page_obj': page_obj,
        'query': query
    })

@never_cache
def music_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/music_detail.html', {'album': album})