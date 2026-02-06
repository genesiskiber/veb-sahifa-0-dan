from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HeroSlider, Category, Product
from .forms import ProductForm


def index(request: WSGIRequest):
    sliders = HeroSlider.objects.filter(published=True)
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)[:9]
    context = {
        "title": "Alibaba",
        "sliders": sliders,
        "categories": categories,
        "products": products,
    }
    return render(request, 'index.html', context)

def add_product(request:WSGIRequest):
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        print(request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('home')

    form = ProductForm()
    context = {
        'form': form
    }   
    return render(request, "main/add_product.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product
    }
    return render(request, "main/detail.html", context)

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)

    form = ProductForm(instance=product)
    context = {
        "product": product,
        "form": form
    }
    return render(request, "main/update_product.html", context)

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('home')

    return render(request, 'main/delete_product.html', {
        'product': product,
        'title': f"{product.title} ni o'chirish"
    })

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Muvaffaqiyatli kirdingiz!")
                return redirect('home')
            else:
                messages.error(request, "Email yoki parol noto'g'ri!")
        except User.DoesNotExist:
            messages.error(request, "Bunday foydalanuvchi topilmadi!")
    
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan!")
            return redirect('login')
        
        username = email.split('@')[0]
        
        if User.objects.filter(username=username).exists():
            counter = 1
            while User.objects.filter(username=f"{username}{counter}").exists():
                counter += 1
            username = f"{username}{counter}"
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        name_parts = full_name.split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.save()
        
        messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
        login(request, user)
        return redirect('home')
    
    return redirect('login')

def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz!")
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    if request.method == 'POST':
        # Ma'lumotlarni yangilash
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Email tekshirish
        if email != request.user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Bu email allaqachon ishlatilmoqda!")
                return redirect('profile')
        
        # Ma'lumotlarni saqlash
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        
        messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
        return redirect('profile')
    
    context = {
        'title': 'My Profile'
    }
    return render(request, 'user/profile.html', context)

@login_required(login_url='login')
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Eski parolni tekshirish
        if not request.user.check_password(old_password):
            messages.error(request, "Eski parol noto'g'ri!")
            return redirect('profile')
        
        # Yangi parollar bir xilligini tekshirish
        if new_password != confirm_password:
            messages.error(request, "Yangi parollar mos kelmadi!")
            return redirect('profile')
        
        # Parolni yangilash
        request.user.set_password(new_password)
        request.user.save()
        
        # Parol o'zgargandan keyin qayta login qilish
        login(request, request.user)
        messages.success(request, "Parol muvaffaqiyatli o'zgartirildi!")
        return redirect('profile')
    
    return redirect('profile')