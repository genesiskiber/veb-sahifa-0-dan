from django.shortcuts import render, redirect

def register_login_view(request):
    return render(request, 'register/index.html')

def register_user(request):
    # hozircha bitta sahifaga qaytaramiz
    return redirect('register:home')

def login_user(request):
    # hozircha bitta sahifaga qaytaramiz
    return redirect('register:home')
