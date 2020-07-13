from django.urls import path
from . import views

urlpatterns = [
    path('sellers', views.signUp, name='seller-signup'),
    path('sellers/<int:sellerId>/items', views.itemsView, name='item-list'),
]