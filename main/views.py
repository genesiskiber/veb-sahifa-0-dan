from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404
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

    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES, instance=Product)
        if form.is_valid():
            Product= form
            return redirect('product_detail', pk=Product.pk)

    form = ProductForm(instance=Product)
    context = {
        "product": Product,
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
        'title': f"{product.title} ni o‘chirish"
    })
