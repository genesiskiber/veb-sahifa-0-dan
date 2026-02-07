from django.db import models

class HeroSlider(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
     
    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name='products')

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_delevry_pizzas","can")
        ]
