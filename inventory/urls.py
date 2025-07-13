from django.urls import path
from . import views

urlpatterns = [
    # Category URLs
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),

    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier-list'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier-detail'),

    # Product URLs
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),

    # Stock Movement URLs
    path('stock-movements/', views.stock_movement_list, name='stock-movement-list'),
    path('stock-movements/<int:pk>/', views.stock_movement_detail, name='stock-movement-detail'),
    path('stock-audit/', views.stock_audit_logs, name='stock-audit'),

    
    # Creative features 
    path('low-stock/', views.low_stock_products, name='low-stock'),
    path('inventory/stats/', views.inventory_stats, name='inventory-stats'),

    # registration
    path('register/', views.register_user, name='register'),

]
