from django.urls import path
from .views import (
    index, 
    add_product, 
    product_detail, 
    update_product, 
    delete_product,
    login_view,
    register_view,
    logout_view,
    profile_view,
    change_password_view
)

urlpatterns = [
    path('', index, name='home'),
    path('add/', add_product, name='add_product'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('product/<int:pk>/update/', update_product, name='product_update'),
    path('product/<int:pk>/delete/', delete_product, name='product_delete'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password_view, name='change_password'),
]