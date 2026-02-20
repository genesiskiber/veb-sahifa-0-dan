import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import HeroSlider, Category, Product, Order, OrderProduct
from .forms import ShippingAddressForm, ProductForm

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']      = 'ShopUz'
        context['sliders']    = HeroSlider.objects.filter(published=True)
        context['categories'] = Category.objects.all()
        context['products']   = Product.objects.filter(is_active=True).order_by('-id')[:9]
        return context


def about_view(request):
    return render(request, 'main/about.html', {'title': 'Biz haqimizda'})


def menu_view(request):
    return render(request, 'main/menu.html', {'title': 'Menyu'})


def book_view(request):
    return render(request, 'main/book.html', {'title': 'Kitoblar'})

class ProductListView(ListView):
    """
    Barcha mahsulotlar ro'yxati
    URL      : /products/
    Template : main/product_list.html
    Context  : products
    """
    model               = Product
    template_name       = 'main/product_list.html'
    context_object_name = 'products'
    paginate_by         = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).order_by('-id')

    
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__name=category)

       
        sort = self.request.GET.get('sort')
        if sort == 'asc':
            qs = qs.order_by('price')
        elif sort == 'desc':
            qs = qs.order_by('-price')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title']      = 'Mahsulotlar'
        return context


class ProductDetailView(DetailView):
    """
    Mahsulot batafsil sahifasi
    URL      : /product/<pk>/
    Template : main/product_detail.html
    Context  : product
    """
    model               = Product
    template_name       = 'main/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Yangi mahsulot qo'shish
    URL      : /product/add/
    Template : main/product_form.html
    """
    model         = Product
    form_class    = ProductForm
    template_name = 'main/product_form.html'
    success_url   = reverse_lazy('main:home')
    login_url     = 'main:login'

    def form_valid(self, form):
        messages.success(self.request, "Mahsulot muvaffaqiyatli qo'shildi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Xatolik! Maydonlarni to'g'ri to'ldiring.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Mahsulot qo'shish"
        context['btn']   = "Qo'shish"
        return context

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Mahsulotni tahrirlash
    URL      : /product/<pk>/update/
    Template : main/product_form.html
    """
    model         = Product
    form_class    = ProductForm
    template_name = 'main/product_form.html'
    login_url     = 'main:login'

    def get_success_url(self):
        return reverse_lazy('main:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Mahsulot muvaffaqiyatli yangilandi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Xatolik! Maydonlarni to'g'ri to'ldiring.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Mahsulotni tahrirlash"
        context['btn']   = "Saqlash"
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Mahsulotni o'chirish
    URL      : /product/<pk>/delete/
    Template : main/product_confirm_delete.html
    """
    model         = Product
    template_name = 'main/product_confirm_delete.html'
    success_url   = reverse_lazy('main:home')
    login_url     = 'main:login'

    def form_valid(self, form):
        messages.success(self.request, "Mahsulot o'chirildi!")
        return super().form_valid(form)


def product_search(request):
    """
    Mahsulot qidirish
    URL: /search/?q=iphone
    """
    query    = request.GET.get('q', '')
    products = Product.objects.filter(
        name__icontains=query,
        is_active=True
    ) if query else Product.objects.none()

    return render(request, 'main/search.html', {
        'products': products,
        'query':    query
    })

@login_required(login_url='main:login')
def cart_view(request):
    order = Order.objects.filter(
        user=request.user,
        status='pending'
    ).first()
    return render(request, 'main/cart.html', {'order': order})


@login_required(login_url='main:login')
def add_to_order(request, pk):
    product  = get_object_or_404(Product, pk=pk)
    order, _ = Order.objects.get_or_create(
        user=request.user,
        status='pending'
    )
    item, created = OrderProduct.objects.get_or_create(
        order=order,
        product=product
    )
    if not created:
        item.quantity += 1
    item.save()
    return JsonResponse({'success': True, 'quantity': item.quantity})


@login_required(login_url='main:login')
def remove_from_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order   = Order.objects.filter(user=request.user, status='pending').first()

    if order:
        item = OrderProduct.objects.filter(order=order, product=product).first()
        if item:
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()

    return JsonResponse({'success': True})

@login_required(login_url='main:login')
def payment(request):
    order = Order.objects.filter(user=request.user, status='pending').first()

    if not order:
        messages.error(request, "Savat bo'sh!")
        return redirect('main:home')

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping      = form.save(commit=False)
            shipping.user = request.user
            shipping.save()
            order.status  = 'paid'
            order.save()
            messages.success(request, "To'lov muvaffaqiyatli amalga oshirildi!")
            return redirect('main:success')
    else:
        form = ShippingAddressForm()

    return render(request, 'main/payment.html', {
        'order': order,
        'form':  form
    })


@login_required(login_url='main:login')
def success(request):
    return render(request, 'main/success.html')


def cancel(request):
    return render(request, 'main/cancel.html')


@csrf_exempt
def webhook_view(request):
    try:
        data = json.loads(request.body)
        
    except Exception:
        return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'ok'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            messages.error(request, "Bu email bilan foydalanuvchi topilmadi!")
            return redirect('main:login')

        user = authenticate(request, username=user_obj.username, password=password)
        if user:
            login(request, user)
            return redirect('main:home')

        messages.error(request, "Parol noto'g'ri!")

    return render(request, 'auth/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan!")
            return redirect('main:login')

        username = email.split('@')[0]
        user     = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        messages.success(request, "Xush kelibsiz!")
        return redirect('main:home')

    return redirect('main:login')

@login_required(login_url='main:login')
def logout_view(request):
    logout(request)
    return redirect('main:home')

@login_required(login_url='main:login')
def profile_view(request):
    orders = Order.objects.filter(
        user=request.user
    ).exclude(status='pending').order_by('-id')

    return render(request, 'main/profile.html', {'orders': orders})


@login_required(login_url='main:login')
def change_password_view(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        user         = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Parol muvaffaqiyatli o'zgartirildi!")
        return redirect('main:profile')

    return render(request, 'main/change_password.html')