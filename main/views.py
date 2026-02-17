
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .forms import ShippingAddressForm, ProductForm, TableOrderForm
from .models import HeroSlider, Category, Product, Order, OrderProduct

@login_required(login_url='login')
def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(title__icontains=query) if query else []
    return render(request, 'main/search.html', {'products': products, 'query': query})

@login_required(login_url='login')
def cart_view(request):
    order = Order.objects.filter(user=request.user, status='pending').first()
    return render(request, 'main/cart.html', {'order': order})

# Payment view
@login_required(login_url='login')
def payment(request): 
    order = Order.objects.filter(user=request.user, status='pending').first()
    if not order:
        messages.error(request, "Savat bo'sh!")
        return redirect('home')
    # Payment logic (mock)
    # Example: redirect to payment gateway
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()
            # Payment logic (mock)
            return redirect('success')
    else:
        form = ShippingAddressForm()
    return render(request, 'main/payment.html', {'order': order, 'form': form})

# Success view
def success(request):
    messages.success(request, "To'lov muvaffaqiyatli amalga oshirildi!")
    return render(request, 'main/success.html')

# Cancel view
def cancel(request):
    messages.error(request, "To'lov bekor qilindi.")
    return render(request, 'main/cancel.html')

# Webhook view
@csrf_exempt
def webhook_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # Process webhook data (mock)
        # Example: update order status
        return JsonResponse({'status': 'received'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse

from .models import HeroSlider, Category, Product, Order, OrderProduct
from .forms import ProductForm

@login_required(login_url='login')
def add_to_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order, created = Order.objects.get_or_create(user=request.user, status='pending')
    item, created = OrderProduct.objects.get_or_create(order=order, product=product)
    item.quantity += 1
    item.save()
    return JsonResponse({'success': True, 'quantity': item.quantity})

@login_required(login_url='login')
def remove_from_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order = Order.objects.filter(user=request.user, status='pending').first()
    if order:
        item = OrderProduct.objects.filter(order=order, product=product).first()
        if item:
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
    return JsonResponse({'success': True})

def index(request):
    sliders = HeroSlider.objects.filter(published=True)
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)[:9]

    return render(request, 'index.html', {
        'title': 'Alibaba',
        'sliders': sliders,
        'categories': categories,
        'products': products,
    })


def about_view(request):
    return render(request, 'about.html', {
        'title': 'About Us'
    })


def menu_view(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    return render(request, 'menu.html', {
        'title': 'Menu',
        'categories': categories,
        'products': products,
    })


from .forms import TableOrderForm

def book_view(request):
    if request.method == 'POST':
        form = TableOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Stol buyurtmangiz qabul qilindi ✅")
            return redirect('home')
    else:
        form = TableOrderForm()
    return render(request, 'book.html', {
        'title': 'Book a Table',
        'form': form
    })

@login_required(login_url='login')
@permission_required('main.add_product', login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot qo‘shildi ✅")
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'main/add_product.html', {
        'form': form
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/detail.html', {
        'product': product
    })


@login_required(login_url='login')
@permission_required('main.change_product', login_url='login')
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot yangilandi ✏️")
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'main/update_product.html', {
        'form': form,
        'product': product
    })


@login_required(login_url='login')
@permission_required('main.delete_product', login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Mahsulot o‘chirildi 🗑")
        if request.user.is_superuser:
            return redirect('home')
        else:
            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return render(request, 'main/delete_product.html', {
        'product': product
    })

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            messages.error(request, "Foydalanuvchi topilmadi ❌")
            return redirect('login')

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user:
            login(request, user)
            messages.success(request, "Xush kelibsiz 👋")
            return redirect('home')

        messages.error(request, "Parol noto‘g‘ri ❌")

    return render(request, 'auth/login.html')


def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email band ❌")
            return redirect('login')

        base_username = email.split('@')[0]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if full_name:
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
        email = request.POST.get('email')

        if User.objects.exclude(pk=request.user.pk).filter(email=email).exists():
            messages.error(request, "Bu email band ❌")
            return redirect('profile')

        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = email
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
        update_session_auth_hash(request, request.user)

        messages.success(request, "Parol o‘zgartirildi 🔐")
        return redirect('profile')

    return redirect('profile')
