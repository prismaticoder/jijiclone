from django.urls import path
from . import views

urlpatterns = [
    path('sellers', views.SignUp, name='seller-signup'),
    path('login', views.LoginView, name='seller-login'),
    path('sellers/<int:sellerId>/items', views.ItemsView.as_view(), name='item-list'),
    path('sellers/<int:sellerId>/items/<str:slug>', views.SingleItemView.as_view(), name='single-item'),
    path('items', views.GetAllItems.as_view(), name='get-all-items'),
    path('items/<str:slug>', views.GetSingleItem.as_view(), name='get-single-item'),
    path('items/<str:slug>/markInterest', views.MarkAsInterested.as_view(), name='mark-interest'),
]