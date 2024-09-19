from django import forms
from .models import Dish

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['category', 'name', 'description', 'price', 'url_img']

        widgets = {
            'url_img': forms.ClearableFileInput(attrs={'style': 'display:none;'}),
        }