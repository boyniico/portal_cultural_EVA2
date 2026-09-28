# cart/views.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import F
from django.shortcuts import get_object_or_404

from music_catalog.models import Album
from books_catalog.models import Book

@require_POST
def api_checkout(request):
    try:
        data = json.loads(request.body)
        cart_items = data.get('cart', [])
        
        if not cart_items:
            return JsonResponse({'success': False, 'error': 'El carrito está vacío.'}, status=400)

        total_amount = 0

        for item in cart_items:
            item_id = item.get('id')
            item_type = item.get('type', '')
            quantity = item.get('quantity', 1)
            price = item.get('price', 0)

            total_amount += price * quantity

            # Identificar modelo correcto según el tipo de producto
            if 'music' in item_type or 'album' in item_type:
                producto = get_object_or_404(Album, id=item_id)
            elif 'book' in item_type:
                producto = get_object_or_404(Book, id=item_id)
            else:
                return JsonResponse({'success': False, 'error': f'Tipo desconocido: {item_type}'}, status=400)

            # Validar y descontar stock de forma segura
            if producto.stock >= quantity:
                producto.stock = F('stock') - quantity
                producto.save()
                producto.refresh_from_db()
            else:
                return JsonResponse({
                    'success': False, 
                    'error': f'Stock insuficiente para "{producto.title}". Quedan {producto.stock}.'
                }, status=400)

        order_num = abs(int(hash(str(cart_items)) % 900000 + 100000))

        return JsonResponse({
            'success': True,
            'order_num': order_num,
            'total': total_amount
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)