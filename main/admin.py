from django.contrib import admin
from .models import HeroSlider, Category, Product, TableOrder

admin.site.register(HeroSlider)
admin.site.register(Category)
class ProductAdmin(admin.ModelAdmin):
	search_fields = ['title']
admin.site.register(Product, ProductAdmin)
admin.site.register(TableOrder)
from .models import Order, OrderProduct
admin.site.register(Order)
admin.site.register(OrderProduct)