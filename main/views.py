from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .models import HeroSlider, Category, Product
from .forms import ProductForm

def index(request: WSGIRequest):
    sliders = HeroSlider.objects.filter(published=True)
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)[:9]

    return render(request, 'index.html', {
        "title": "Alibaba",
        "sliders": sliders,
        "categories": categories,
        "products": products,
    })

@login_required(login_url='login')
@permission_required('main.add_product', raise_exception=True)
def add_product(request: WSGIRequest):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot qo‘shildi ✅")
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'main/add_product.html', {'form': form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/detail.html', {"product": product})


@login_required(login_url='login')
@permission_required('main.change_product', raise_exception=True)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot yangilandi ✏️")
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'main/update_product.html', {
        "product": product,
        "form": form
    })


@login_required(login_url='login')
@permission_required('main.delete_product', raise_exception=True)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Mahsulot o‘chirildi 🗑")
        return redirect('home')

    return render(request, 'main/delete_product.html', {
        "product": product
    })

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Xush kelibsiz 👋")
                return redirect('home')
            else:
                messages.error(request, "Parol noto‘g‘ri ❌")
        except User.DoesNotExist:
            messages.error(request, "Foydalanuvchi topilmadi ❌")

    return render(request, 'auth/login.html')


def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email band ❌")
            return redirect('login')

        username = email.split('@')[0]
        counter = 1
        base_username = username

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        parts = full_name.split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''
        user.save()

        login(request, user)
        messages.success(request, "Ro‘yxatdan o‘tdingiz 🎉")
        return redirect('home')

    return redirect('login')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz 👋")
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        messages.success(request, "Profil yangilandi ✅")
        return redirect('profile')

    return render(request, 'user/profile.html')


@login_required(login_url='login')
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, "Eski parol noto‘g‘ri ❌")
            return redirect('profile')

        if new_password != confirm_password:
            messages.error(request, "Parollar mos emas ❌")
            return redirect('profile')

        request.user.set_password(new_password)
        request.user.save()
        login(request, request.user)

        messages.success(request, "Parol o‘zgartirildi 🔐")
        return redirect('profile')

    return redirect('profile')
