from django.urls import path
from . import views

urlpatterns = [
    path('sellers', views.SignUp, name='seller-signup'),
    path('sellers/<int:sellerId>/items', views.ItemsView, name='item-list'),
    path('sellers/<int:sellerId>/items/<str:slug>', views.SingleItemView, name='single-item'),
]