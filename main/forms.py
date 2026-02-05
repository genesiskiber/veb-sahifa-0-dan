from django import forms
from .models import Product

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