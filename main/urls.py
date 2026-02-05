from django.urls import path
from .views import index, add_product, product_detail, update_product, delete_product

urlpatterns = [
    path('', index, name='home'),
    path('add/', add_product, name='add_product'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('product/<int:pk>/update/', update_product, name='product_update'),
    path('product/<int:pk>/delete/', delete_product, name='product_delete'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
]