from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Home & Auth views
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Product views
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Seller views
    path('seller/<username>/', views.seller_profile, name='seller_profile'),
    
    # Cart views
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    
    # Checkout & Order views
    path('checkout/', views.checkout, name='checkout'),
    path('order/process/', views.process_order, name='process_order'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<str:order_id>/', views.order_detail, name='order_detail'),
    
    # Review views
    path('review/add/<int:product_id>/', views.add_review, name='add_review'),
    
    # Wishlist views
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
