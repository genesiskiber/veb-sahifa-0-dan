from django import forms
from .models import Product, TableOrder, ShippingAddress
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'postal_code', 'country', 'phone']

class TableOrderForm(forms.ModelForm):
    class Meta:
        model = TableOrder
        fields = ['name', 'phone', 'people_count', 'date', 'time', 'note']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            "title": "nomi",
            "description": "Matni",
        }

        help_texts = {
            "title": "Some useful help text."
        }

        error_messages = {
            "title": {
                "max_length": "This writer's name is too long.",
                "required": "Ma'lumot kiritish shart."
            },
            "price": {
                "max_length": "This writer's name is too long.",
                "required": "Narx kiritish shart."
            },
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control"
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
        }