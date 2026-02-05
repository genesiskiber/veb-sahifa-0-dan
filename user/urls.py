from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('', views.register_login_view, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
]