from django.urls import path
from .views import (
    IndexView,
    about_view,
    menu_view,
    book_view,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    product_search,
    login_view,
    register_view,
    logout_view,
    profile_view,
    change_password_view,
    add_to_order,
    remove_from_order,
    cart_view,
    payment,
    success,
    cancel,
    webhook_view,
)

app_name = 'main'

urlpatterns = [
    path('',        IndexView.as_view(), name='home'),
    path('about/',  about_view,          name='about'),
    path('menu/',   menu_view,           name='menu'),
    path('book/',   book_view,           name='book'),

    path('products/',                   ProductListView.as_view(),   name='product_list'),
    path('product/<int:pk>/',           ProductDetailView.as_view(), name='product_detail'),
    path('product/add/',                ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/update/',    ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/',    ProductDeleteView.as_view(), name='product_delete'),
    path('search/',                     product_search,              name='product_search'),

    path('login/',           login_view,           name='login'),
    path('register/',        register_view,         name='register'),
    path('logout/',          logout_view,           name='logout'),
    path('profile/',         profile_view,          name='profile'),
    path('change-password/', change_password_view,  name='change_password'),

    path('cart/',                    cart_view,          name='cart'),
    path('order/add/<int:pk>/',      add_to_order,       name='add_to_order'),
    path('order/remove/<int:pk>/',   remove_from_order,  name='remove_from_order'),

    path('payment/', payment,      name='payment'),
    path('success/', success,      name='success'),
    path('cancel/',  cancel,       name='cancel'),
    path('webhook/', webhook_view, name='webhook_view'),
]