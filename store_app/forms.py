from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'color']
        widgets = {
            'color': forms.Select(choices=[
                ('Blue-white', 'Blue-white'),
                ('blue-burquoise', 'blue-burquoise'),
                ('pink-silver', 'pink-silver'),
                ('fillet', 'fillet'),
                ('purple-white', 'purple-white'),
                ('pearl-golden', 'pearl-golden'),
                ('blue-golden', 'blue-golden'),
            ])
        }

