# cart/urls.py
from django.urls import path
from cart import views

urlpatterns = [
    path('api/checkout/', views.api_checkout, name='api_checkout'),
]