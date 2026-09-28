from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from .models import Book

def catalog(request):
    query = request.GET.get('q', '')
    books = Book.objects.all().order_by('title')
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__name__icontains=query) | 
            Q(genre__name__icontains=query)
        )
    
    # Paginación (ej: 8 libros por página)
    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'books/catalog.html', {
        'page_obj': page_obj,
        'query': query
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

@never_cache
def catalog(request):
    query = request.GET.get('q', '')
    books = Book.objects.all().order_by('title')
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__name__icontains=query) | 
            Q(genre__name__icontains=query)
        )
    
    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'books/catalog.html', {
        'page_obj': page_obj,
        'query': query
    })

@never_cache
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})