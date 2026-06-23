# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('product/<int:product_id>/', views.product_detail, name='product_detail'), 
    
    # Cart Core URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Dynamic Plus/Minus Quantity URL
    path('cart/update/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
]